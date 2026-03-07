"""Root CLI wiring for qso-auth."""

from __future__ import annotations

import argparse
import sys
from typing import Callable, Protocol, cast

from . import creds, persona, provider


class _RegisterCLI(Protocol):
    def __call__(self, sp: argparse._SubParsersAction[argparse.ArgumentParser]) -> None: ...


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="qso-auth",
        description="Persona and credential management for qso-graph MCP servers",
    )
    parser.add_argument(
        "--version", action="version",
        version=f"%(prog)s {__import__('qso_graph_auth').__version__}",
    )

    subparsers = parser.add_subparsers(dest="command")

    if hasattr(persona, "register_cli"):
        cast(_RegisterCLI, getattr(persona, "register_cli"))(subparsers)
    if hasattr(provider, "register_cli"):
        cast(_RegisterCLI, getattr(provider, "register_cli"))(subparsers)
    if hasattr(creds, "register_cli"):
        cast(_RegisterCLI, getattr(creds, "register_cli"))(subparsers)

    return parser


def main(argv: list[str] | None = None) -> int:
    args_in = sys.argv[1:] if argv is None else argv
    parser = build_parser()

    if not args_in:
        parser.print_help()
        return 0

    args = parser.parse_args(args_in)
    func = cast(Callable[[argparse.Namespace], int] | None, getattr(args, "func", None))
    if func is not None:
        return func(args)

    parser.print_help()
    return 2
