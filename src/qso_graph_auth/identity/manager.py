"""PersonaManager facade for identity operations."""

from __future__ import annotations

from qso_graph_auth.credentials import get_creds

from .errors import PersonaNotFound, ProviderRefMissing, SecretMissing
from .models import Persona
from .store import PersonaStore

# Providers that authenticate with an API key rather than a password. For
# these, a stored api_key wins over a stored password, so a password saved
# alongside the key (set-credential accepts both for every provider) is never
# sent as the key. Every other provider keeps the historical order: password
# first, api_key as the fallback.
API_KEY_FIRST: frozenset[str] = frozenset({"qrz_logbook"})


class PersonaManager:
    """High-level API for personas + credentials (no network I/O)."""

    def __init__(self, store: PersonaStore | None = None) -> None:
        self.store: PersonaStore = store or PersonaStore()

    # -------- Persona lookups --------

    def get_persona(self, name: str) -> Persona | None:
        return self.store.get(name)

    def get_provider_username(self, persona: str, provider: str) -> str | None:
        p = self.get_persona(persona)
        if p is None:
            return None
        if provider.lower() not in p.providers:
            return None
        creds = get_creds(persona, provider)
        return creds.username if creds else None

    # -------- Strict API --------

    def require(
        self, persona: str, provider: str, prefer: str | None = None,
    ) -> tuple[str, str]:
        """Return (username, secret) from the OS keyring.

        When both a password and an api_key are stored, ``prefer`` picks which
        one is returned: ``"password"`` or ``"api_key"``. Left as None, the
        provider decides (api_key first for providers in ``API_KEY_FIRST``,
        password first otherwise). The other value is used as a fallback if the
        preferred one is not stored.
        """
        if prefer not in (None, "password", "api_key"):
            raise ValueError(f"prefer must be 'password' or 'api_key', got {prefer!r}")

        p = self.get_persona(persona)
        if p is None:
            raise PersonaNotFound(persona, provider, f"No such persona: '{persona}'")

        if provider.lower() not in p.providers:
            raise ProviderRefMissing(
                persona, provider, f"Persona '{persona}' has no '{provider}' ref"
            )

        creds = get_creds(persona, provider)
        if not creds:
            raise SecretMissing(
                persona, provider,
                f"Missing credentials for {provider} on persona '{persona}' "
                f"(run: qso-auth creds set {persona} {provider})"
            )

        username = creds.username
        if not username:
            raise SecretMissing(
                persona, provider,
                f"No username for {provider} on persona '{persona}' "
                f"(run: qso-auth creds set {persona} {provider})"
            )

        if prefer is None:
            prefer = "api_key" if provider.lower() in API_KEY_FIRST else "password"
        if prefer == "api_key":
            secret = creds.api_key or creds.password
        else:
            secret = creds.password or creds.api_key
        if not secret:
            raise SecretMissing(
                persona, provider,
                f"No password/api_key for {provider} on persona '{persona}' "
                f"(run: qso-auth creds set {persona} {provider})"
            )
        return username, secret

    # -------- Display helpers --------

    @staticmethod
    def mask_username(u: str) -> str:
        if not u:
            return ""
        if len(u) <= 2:
            return u[0] + "*" * (len(u) - 1)
        return f"{u[0]}***{u[-1]}"
