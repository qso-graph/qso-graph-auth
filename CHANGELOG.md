# Changelog

All notable changes to `qso-graph-auth` are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] — 2026-10-26

### Changed

- **Python 3.11 is the minimum.** 3.10 reached end of life in October 2026
  ([PEP 619](https://peps.python.org/pep-0619/)), so it gets no further security
  releases on any platform. On Windows it was worse than unsupported: `uv`'s 3.10
  is built against OpenSSL 1.1.1w, end of life since September 2023, so HTTPS
  from this server ran over an unmaintained TLS library. `certifi` does not help
  with that — it supplies the root store, not the implementation.

  3.10 support was already nominal. This package has linted with
  `ruff target-version = "py311"` and type-checked with `mypy python_version =
  "3.11"` for some time, so nothing ever verified the 3.10 claim.

  `uv.lock` is regenerated and the diff is large, but **nothing is upgraded** —
  it is the 3.10 resolution branch disappearing. Packages that carried two pins,
  one per Python branch, now carry the single 3.11+ pin they already resolved to.
  An install on 3.11 or later is unchanged.

## [0.1.7] — 2026-10-26

- Move every Node 20 action to its first Node 24 major
- The locked-dependency audit blocked every release
- A release is a workflow, not a merge — and carry develop's gate fix across

## [0.1.6] — 2026-10-11

- **ruff and mypy run in CI** (qso-graph-devel#66), as a job the `ci-all-green` gate requires.
  Settings follow `adif-mcp`, the reference for every qso-graph Python repo, rather than a style of
  this repo's own. They run once rather than per Python version: both read the source, and neither
  answer changes with the interpreter.
- `mypy` was already clean across all seventeen source files. `ruff` found one unused import:
  `identity/manager.py` named `ProviderRef`, which the package re-exports from
  `identity/__init__.py` and this module never uses.
- `E501` is deferred rather than adopted (qso-graph-devel#70): what it reports in these repos are
  widths, not defects, and some lines are long because they name a publisher's field exactly.
- **The published contact is `maintainers@qso-graph.io`** (qso-graph-devel#69). The `authors` field
  carried a personal address, and that field is what PyPI shows on the package page. The project
  has had outside contributions; a project address is the fitting route for them.

## [0.1.5] — 2026-10-08

- `__version__` is read from the installed package's metadata, so `pyproject.toml` is the only place the version is written. 0.1.4 reported itself as 0.1.3 because the two copies disagreed.

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
