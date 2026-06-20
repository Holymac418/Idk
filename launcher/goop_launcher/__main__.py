"""``python3 -m goop_launcher`` entry point.

Routes to the GTK GUI by default, or to one of the CLI subcommands:

    python3 -m goop_launcher diagnose
    python3 -m goop_launcher version

This keeps the launcher usable on a headless box for diagnostics while still
behaving like a Winlator-style launcher when run interactively.
"""

from __future__ import annotations

import argparse
import sys

from . import __version__


def _cmd_version(_args) -> int:
    print(__version__)
    return 0


def _cmd_diagnose(_args) -> int:
    from . import checks

    diag = checks.run_all()
    print(diag.summary())
    return 0 if diag.launchable else 1


def _cmd_gui(_args) -> int:
    from . import app

    return app.main()


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="winlator-goop", description="Winlator Goop Mod")
    p.add_argument("--version", action="store_true", help="Print version and exit.")
    sub = p.add_subparsers(dest="command")

    sub.add_parser("version", help="Print version.").set_defaults(func=_cmd_version)
    d = sub.add_parser("diagnose", help="Run system guards and print a report.")
    d.set_defaults(func=_cmd_diagnose)

    g = sub.add_parser("gui", help="Open the GTK launcher window (default).")
    g.set_defaults(func=_cmd_gui)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()

    if argv is None:
        argv = sys.argv[1:]
    if argv and argv[0] == "--version":
        print(__version__)
        return 0

    args = parser.parse_args(argv)
    if getattr(args, "version", False) and not hasattr(args, "func"):
        print(__version__)
        return 0

    if not hasattr(args, "func"):
        return _cmd_gui(args)

    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
