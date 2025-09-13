import sys
import argparse
from . import __version__
from .main import run_interactive
from .setup import run_first_time_setup


def build_parser():
    p = argparse.ArgumentParser(
        prog="xodex",
        description="Xodex – utilitários de automação/IA para devs.",
    )
    p.add_argument("-V", "--version", action="store_true", help="Exibe a versão e sai")

    sub = p.add_subparsers(dest="cmd")

    sp = sub.add_parser(
        "setup", aliases=["config"], help="Configura o Xodex (primeiro uso)"
    )
    sp.set_defaults(func=lambda _args: run_first_time_setup())

    return p


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv

    if not argv:
        return run_interactive()

    parser = build_parser()
    args = parser.parse_args(argv)

    if getattr(args, "version", False):
        print(__version__)
        return 0

    if hasattr(args, "func"):
        return args.func(args)

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
