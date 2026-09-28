# Changelog

All notable changes to `qso-graph-auth` are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
