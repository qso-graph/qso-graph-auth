# qso-graph-auth

[![PyPI](https://img.shields.io/pypi/v/qso-graph-auth)](https://pypi.org/project/qso-graph-auth/)
[![Python](https://img.shields.io/pypi/pyversions/qso-graph-auth)](https://pypi.org/project/qso-graph-auth/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Persona and credential management for [qso-graph](https://qso-graph.io) MCP servers.

Provides a shared identity layer so that authenticated MCP servers (eqsl-mcp, qrz-mcp, lotw-mcp, hamqth-mcp) can retrieve credentials from the OS keyring without embedding secrets in configuration files.

## Install

```bash
pip install qso-graph-auth
```

## Quick Start

```bash
# Create a persona
qso-auth persona add --name default --callsign YOUR_CALL --start 2020-01-01

# Enable providers
qso-auth provider enable default eqsl
qso-auth provider enable default qrz
qso-auth provider enable default lotw
qso-auth provider enable default hamqth
qso-auth provider enable default qrz_logbook

# Set credentials (stored in OS keyring)
qso-auth creds set default eqsl --username YOUR_CALL --password YOUR_PASS
qso-auth creds set default qrz --username YOUR_CALL --password YOUR_PASS
qso-auth creds set default lotw --username YOUR_CALL --password YOUR_PASS
qso-auth creds set default hamqth --username YOUR_CALL --password YOUR_PASS
qso-auth creds set default qrz_logbook --username YOUR_CALL --api-key YOUR_API_KEY

# Check credential health
qso-auth creds doctor
```

## Providers

| Provider | Auth Type | Description |
|----------|-----------|-------------|
| eqsl | username + password | eQSL.cc electronic QSL |
| lotw | username + password | ARRL Logbook of The World |
| qrz | username + password | QRZ.com XML subscription |
| qrz_logbook | username + API key | QRZ.com Logbook API |
| hamqth | username + password | HamQTH.com callsign lookup |

## Security

- Credentials are stored **only** in the OS keyring (macOS Keychain, GNOME Keyring, Windows Credential Locker)
- Credentials are **never** written to config files, logs, tool results, or error messages
- The persona index (`~/.config/adif-mcp/personas.json`) stores only non-secret metadata (callsign, provider names)
- All external connections use HTTPS only

## For MCP Server Authors

```python
from qso_graph_auth.identity import PersonaManager

pm = PersonaManager()
username, secret = pm.require("default", "eqsl")
```

The `require()` method raises typed exceptions (`PersonaNotFound`, `ProviderRefMissing`, `SecretMissing`) with actionable error messages pointing users to the correct `qso-auth creds set` command.

## CLI Reference

```
qso-auth persona add      Create a new persona
qso-auth persona list     List all personas
qso-auth persona show     Show persona details
qso-auth persona remove   Remove a persona
qso-auth provider list    List supported providers
qso-auth provider enable  Enable a provider for a persona
qso-auth provider disable Disable a provider for a persona
qso-auth creds set        Save credentials to OS keyring
qso-auth creds get        Show redacted credentials
qso-auth creds delete     Delete stored credentials
qso-auth creds doctor     Check credential health
qso-auth creds reset      Factory reset (delete all)
```

## Part of QSO-Graph

This package is part of the [qso-graph](https://github.com/qso-graph) MCP server suite for amateur radio. See [qso-graph.io](https://qso-graph.io) for documentation.

## License

[GPLv3](LICENSE)
