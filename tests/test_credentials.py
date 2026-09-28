"""Tests for PersonaManager.require() secret selection.

set-credential accepts --username, --password and --api-key for every
provider. When both a password and an api_key were stored, require() used to
return the password unconditionally, so a logbook API key was silently
replaced by a password and QRZ answered "invalid api key".

These tests use a fake persona store and a patched keyring lookup; no keyring
or network access is needed.
"""

from types import SimpleNamespace
from unittest import mock

import pytest

from qso_graph_auth.credentials import Credentials
from qso_graph_auth.identity.errors import SecretMissing
from qso_graph_auth.identity.manager import PersonaManager

PROVIDERS = ("qrz", "qrz_logbook", "eqsl", "lotw", "hamqth")


class _FakeStore:
    """Just enough of PersonaStore for require(): get(name) -> persona."""

    def get(self, name):
        if name != "default":
            return None
        return SimpleNamespace(providers={p: object() for p in PROVIDERS})


def _require(provider, password=None, api_key=None, prefer=None, username="W1AW"):
    creds = Credentials(username=username, password=password, api_key=api_key)
    with mock.patch("qso_graph_auth.identity.manager.get_creds", return_value=creds):
        return PersonaManager(store=_FakeStore()).require(
            "default", provider, prefer=prefer
        )


def test_qrz_logbook_prefers_api_key_when_both_are_stored():
    """The reported bug: a stored password must not replace the logbook key."""
    assert _require("qrz_logbook", password="pw", api_key="KEY") == ("W1AW", "KEY")


def test_qrz_logbook_falls_back_to_password_when_no_api_key():
    """Unchanged behaviour for entries that only have a password."""
    assert _require("qrz_logbook", password="pw") == ("W1AW", "pw")


def test_qrz_logbook_uses_api_key_alone():
    assert _require("qrz_logbook", api_key="KEY") == ("W1AW", "KEY")


@pytest.mark.parametrize("provider", ["qrz", "eqsl", "lotw", "hamqth"])
def test_other_providers_keep_password_first(provider):
    """Providers outside API_KEY_FIRST behave exactly as before."""
    assert _require(provider, password="pw", api_key="KEY") == ("W1AW", "pw")


def test_provider_lookup_is_case_insensitive():
    assert _require("QRZ_LOGBOOK", password="pw", api_key="KEY")[1] == "KEY"


def test_prefer_overrides_the_provider_default():
    assert _require("qrz_logbook", password="pw", api_key="KEY", prefer="password")[1] == "pw"
    assert _require("qrz", password="pw", api_key="KEY", prefer="api_key")[1] == "KEY"


def test_prefer_falls_back_to_the_other_secret():
    assert _require("qrz", api_key="KEY", prefer="password")[1] == "KEY"
    assert _require("qrz_logbook", password="pw", prefer="api_key")[1] == "pw"


def test_invalid_prefer_is_rejected():
    with pytest.raises(ValueError):
        _require("qrz", password="pw", prefer="token")


def test_missing_secret_still_raises():
    with pytest.raises(SecretMissing):
        _require("qrz_logbook")


def test_missing_username_still_raises():
    with pytest.raises(SecretMissing):
        _require("qrz_logbook", api_key="KEY", username=None)
