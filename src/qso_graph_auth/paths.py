"""Cross-platform config path resolver for qso-graph-auth.

Uses the same config directory as adif-mcp (~/.config/adif-mcp/) for
backwards compatibility with existing persona indexes.
"""

from __future__ import annotations

import os
from pathlib import Path

# Config folder name — keep "adif-mcp" for backwards compat with existing
# personas.json files. Users who already have credentials set up should not
# need to re-create their persona index.
_PROJECT_NAME = "adif-mcp"


def _os_config_root() -> Path:
    xdg = os.environ.get("XDG_CONFIG_HOME")
    if xdg:
        return Path(xdg)

    if os.name == "nt":
        base = os.environ.get("APPDATA")
        if base:
            return Path(base)
        return Path.home() / "AppData" / "Roaming"

    return Path.home() / ".config"


def config_dir() -> Path:
    """Resolve and create the per-user config directory."""
    root = _os_config_root() / _PROJECT_NAME
    root.mkdir(parents=True, exist_ok=True)
    return root


def config_path(filename: str) -> Path:
    """Resolve a file under the config directory."""
    p = config_dir() / filename
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def personas_index_path() -> Path:
    """Resolve the personas index file path."""
    return config_path("personas.json")
