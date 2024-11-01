import argparse
from .src import Init


def main():
    parser = argparse.ArgumentParser(prog="ppm")
    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser(
        "init", help="Initializes a new project")
    init_parser.set_defaults(func=Init().init)

    args = parser.parse_args()

    if args.command:
        args.func()
    else:
        parser.print_help()
