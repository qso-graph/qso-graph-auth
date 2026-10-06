# Changelog

All notable changes to `qso-graph-auth` are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.4] — 2026-10-06

- PyPI: the Documentation link goes to this package's own page, https://qso-graph.io/servers/qso-graph-auth/ (qso-graph/.github#15).
- CI: the release flow (qso-graph/.github TEMPLATES.md). Work lands on `develop`; a release is a
  PR from `develop` into `main`, and merging it publishes to PyPI and the MCP Registry, verifies both
  and tags the release. CI runs on `develop` too, and PRs into `main` must come from `develop` or a
  `security/` branch.

## [0.1.3] — 2026-10-04

### Security

- **`qso-auth creds get` no longer shows any part of a secret.** The redacted view printed the
  first two characters of a password or API key; it now shows only that one is stored (`•••`).
- **`qso-auth creds get --raw` is removed.** It printed the stored password or API key in full.
  Credentials are never printed (Security Framework guarantee #1); to see a stored secret, open
  your operating system's keychain. Both found by CodeQL `py/clear-text-logging-sensitive-data`.

### Fixed

- `qso-auth --version` reported 0.1.0; `__version__` now matches the package version.

## [0.1.2] — 2026-09-28

### Fixed

- **`require()` sent the password as an API key.** With both a password and an `api_key`
  stored, it returned the password. For `qrz_logbook`, which authenticates with an API key,
  that meant the password was sent as the key, and QRZ echoes a rejected key back in its
  error. Providers in `API_KEY_FIRST` (`qrz_logbook`) now return the `api_key` first, falling
  back to the password; other providers are unchanged. A caller can also choose with
  `require(..., prefer="password" | "api_key")`.
  Contributed by [@ssamjung2](https://github.com/ssamjung2)
  ([qso-graph/qrz-mcp#10](https://github.com/qso-graph/qrz-mcp/issues/10)).

## [0.1.1] and earlier

See the git history.
