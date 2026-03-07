"""Identity namespace (personas, credential orchestration)."""

from __future__ import annotations

from .errors import CredentialError, PersonaNotFound, ProviderRefMissing, SecretMissing
from .manager import PersonaManager
from .models import Persona, ProviderRef
from .store import PersonaStore

__all__ = [
    "CredentialError",
    "Persona",
    "PersonaManager",
    "PersonaNotFound",
    "PersonaStore",
    "ProviderRef",
    "ProviderRefMissing",
    "SecretMissing",
]
