"""Persistence layer for personas (JSON index).

This module is intentionally ignorant of secrets. It only manages the persona
index (non-secret fields) and leaves credential storage to the secrets backend.
"""

from __future__ import annotations

import builtins
import json
from datetime import date
from pathlib import Path
from typing import Any, TypedDict, cast

from qso_graph_auth.paths import personas_index_path

from .models import Persona, ProviderRef

# ---------- JSON helpers ----------


class _PersonaJSON(TypedDict, total=False):
    name: str
    callsign: str
    start: str | None
    end: str | None
    providers: dict[str, ProviderRef]


def _to_date(s: str | None) -> date | None:
    """Parse YYYY-MM-DD or return None."""
    if not s:
        return None
    return date.fromisoformat(s)


def _dumps(obj: Any) -> str:
    """Stable JSON for on-disk file (pretty + sorted)."""
    return json.dumps(obj, indent=2, sort_keys=True)


# ---------- Store ----------


class PersonaStore:
    """Loads/saves the persona index JSON and provides CRUD helpers."""

    def __init__(self, index_path: Path | None = None) -> None:
        self.index_path = index_path or personas_index_path()
        self._personas: dict[str, Persona] = {}
        self._mtime: float = 0.0
        self._load()

    def _load(self) -> None:
        self._personas = {}
        if not self.index_path.exists():
            self.index_path.parent.mkdir(parents=True, exist_ok=True)
            self.index_path.write_text(_dumps({"personas": {}}), encoding="utf-8")
            self._mtime = self.index_path.stat().st_mtime
            return

        self._mtime = self.index_path.stat().st_mtime
        data: dict[str, Any] = json.loads(self.index_path.read_text(encoding="utf-8"))
        raw = cast(dict[str, _PersonaJSON], data.get("personas", {}))

        for name, rec in raw.items():
            start = _to_date(rec.get("start"))
            end = _to_date(rec.get("end"))
            providers_raw = rec.get("providers")
            providers_map: dict[str, ProviderRef] = (
                dict(providers_raw) if providers_raw else {}
            )
            self._personas[name] = Persona(
                name=rec.get("name", name),
                callsign=rec["callsign"],
                start=start,
                end=end,
                providers=providers_map,
            )

    def _refresh(self) -> None:
        try:
            mtime = self.index_path.stat().st_mtime
        except OSError:
            return
        if mtime != self._mtime:
            self._load()

    def _save(self) -> None:
        out: dict[str, _PersonaJSON] = {}
        for name, p in self._personas.items():
            out[name] = {
                "name": p.name,
                "callsign": p.callsign,
                "start": p.start.isoformat() if p.start else None,
                "end": p.end.isoformat() if p.end else None,
                "providers": p.providers,
            }
        self.index_path.write_text(_dumps({"personas": out}), encoding="utf-8")

    def list(self) -> builtins.list[Persona]:
        self._refresh()
        return [self._personas[k] for k in sorted(self._personas)]

    def get(self, name: str) -> Persona | None:
        self._refresh()
        p = self._personas.get(name)
        if p is not None:
            return p
        name_lower = name.lower()
        for key, persona in self._personas.items():
            if key.lower() == name_lower:
                return persona
        return None

    def upsert(
        self,
        *,
        name: str,
        callsign: str,
        start: date | None,
        end: date | None,
    ) -> Persona:
        if start and end and end < start:
            raise ValueError("end date cannot be earlier than start date")

        name = name.lower()
        callsign_norm = callsign.upper()

        existing = self._personas.get(name)
        if existing:
            existing.callsign = callsign_norm
            existing.start = start
            existing.end = end
            self._save()
            return existing

        p = Persona(
            name=name,
            callsign=callsign_norm,
            start=start,
            end=end,
            providers={},
        )
        self._personas[name] = p
        self._save()
        return p

    def remove(self, name: str) -> bool:
        if name in self._personas:
            del self._personas[name]
            self._save()
            return True
        return False

    def set_provider_ref(
        self,
        *,
        persona: str,
        provider: str,
        username: str,
    ) -> Persona:
        p = self._personas.get(persona)
        if not p:
            raise KeyError(f"Persona not found: {persona}")
        key = provider.lower()
        p.providers[key] = {"username": username}
        self._save()
        return p

    def remove_provider_ref(self, *, persona: str, provider: str) -> bool:
        p = self._personas.get(persona)
        if not p:
            raise KeyError(f"Persona not found: {persona}")
        key = provider.lower()
        if key in p.providers:
            del p.providers[key]
            self._save()
            return True
        return False
