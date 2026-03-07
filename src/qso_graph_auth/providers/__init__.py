"""Provider package exports and shared types."""

from __future__ import annotations

from typing import Literal

ProviderKey = Literal["lotw", "eqsl", "qrz", "qrz_logbook", "hamqth"]

__all__ = ["ProviderKey"]
