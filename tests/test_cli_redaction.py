"""qso-auth never prints a stored secret, or any part of one (Security Framework guarantee #1).

Found by CodeQL py/clear-text-logging-sensitive-data: `creds get --raw` printed the stored JSON, and
the redacted view kept a secret's first two characters.
"""

import pytest

from qso_graph_auth.cli import creds
from qso_graph_auth.cli.root import build_parser
from qso_graph_auth.credentials import Credentials

SECRETS = {"password": "hunter2-correct-horse", "api_key": "QRZ-ABCDEF-123456"}


def test_redacted_shows_no_part_of_a_secret():
    out = creds._redacted(Credentials(username="KI7MT", **SECRETS))
    assert out["username"] == "KI7MT"
    for field, secret in SECRETS.items():
        assert out[field] == "•••"
        assert secret[:2] not in out[field]


def test_creds_get_has_no_raw_option():
    with pytest.raises(SystemExit):
        build_parser().parse_args(["creds", "get", "ki7mt", "qrz", "--raw"])


def test_creds_get_prints_only_redacted(monkeypatch, capsys):
    monkeypatch.setattr(creds, "get_creds", lambda persona, provider: Credentials(username="KI7MT", **SECRETS))
    args = build_parser().parse_args(["creds", "get", "ki7mt", "qrz"])
    assert args.func(args) == 0
    printed = capsys.readouterr().out
    for secret in SECRETS.values():
        assert secret[:2] not in printed
