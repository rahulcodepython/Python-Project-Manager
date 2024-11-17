import argparse
from .src import Init, Install, Uninstall


def main():
    parser = argparse.ArgumentParser(prog="ppm")
    subparsers = parser.add_subparsers(dest="command")

    # Init command with -d flag
    init_parser = subparsers.add_parser("init", help="initializes a new project")
    init_parser.add_argument(
        "-d", action="store_true", help="enable default configuration"
    )
    init_parser.set_defaults(func=Init().init)

    # Install command with multiple arguments support
    install_parser = subparsers.add_parser(
        "install", help="install packages in the project"
    )
    install_parser.add_argument("packages", nargs="*", help="Packages to install")
    install_parser.set_defaults(func=Install().install)

    # Uninstall command with multiple arguments support
    uninstall_parser = subparsers.add_parser(
        "uninstall", help="install packages in the project"
    )
    uninstall_parser.add_argument("packages", nargs="*", help="Packages to uninstall")
    uninstall_parser.set_defaults(func=Uninstall().uninstall)

    args = parser.parse_args()

    if args.command == "init":
        args.func(args.d)  # Pass the `-d` argument as `True` or `False`
    elif args.command == "install":
        args.func(args.packages)
    elif args.command == "uninstall":
        args.func(args.packages)
    else:
        parser.print_help()
