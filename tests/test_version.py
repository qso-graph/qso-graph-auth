"""__version__ is the installed distribution's version, not a second copy of it."""

from importlib.metadata import version

import qso_graph_auth


def test_version_matches_distribution():
    assert qso_graph_auth.__version__ == version("qso-graph-auth")
