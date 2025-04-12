import argparse
# from .src import Init, Install, Uninstall, Run, AddEnv, List, Freeze
from .src import Init, List, Freeze, Install, Run, Outdated, Update, Uninstall
from .src.constraints import VERSION

# Define the version
version = VERSION


def main():
    parser = argparse.ArgumentParser(prog="ppm")
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"The version of ppm is {version}",
        help="show the version of ppm and exit",
    )

    subparsers = parser.add_subparsers(dest="command")

    # Init command with -d flag
    init_parser = subparsers.add_parser(
        "init", help="Initializes a new project")
    init_parser.add_argument(
        "-y", action="store_true", help="Accept default configuration"
    )
    init_parser.set_defaults(func=Init().init)

    # Install command with multiple arguments support
    install_parser = subparsers.add_parser(
        "install", help="install packages in the project"
    )
    install_parser.add_argument(
        "packages", nargs="*", help="Packages to install")
    install_parser.set_defaults(func=Install().install)

    # Uninstall command with multiple arguments support
    uninstall_parser = subparsers.add_parser(
        "uninstall", help="install packages in the project"
    )
    uninstall_parser.add_argument(
        "packages", nargs="*", help="Packages to uninstall")
    uninstall_parser.set_defaults(func=Uninstall().uninstall)

    # Run command to run the code
    run_parser = subparsers.add_parser("run", help="run the project")
    run_parser.add_argument("script", nargs="*",
                            help="Script to run in the project")
    run_parser.set_defaults(func=Run().run)

    list_parser = subparsers.add_parser("list", help="list all the packages")
    list_parser.set_defaults(func=List().list)

    freeze_parser = subparsers.add_parser(
        "freeze", help="Generate requirements.txt file"
    )
    freeze_parser.set_defaults(func=Freeze().freeze)

    outdated_parser = subparsers.add_parser(
        "outdated", help="Show outdated packages")
    outdated_parser.set_defaults(func=Outdated().outdated)

    update_parser = subparsers.add_parser(
        "update", help="update packages in the project"
    )
    update_parser.add_argument(
        "packages", nargs="*", help="Packages to update")
    update_parser.set_defaults(func=Update().update)

    args = parser.parse_args()

    if args.command == "init":
        args.func(args.y)  # Pass the `-d` argument as `True` or `False`
    elif args.command == "install":
        args.func(args.packages)
    elif args.command == "update":
        args.func(args.packages)
    elif args.command == "uninstall":
        args.func(args.packages)
    elif args.command == "run":
        args.func(args.script)
    elif args.command == "list" or args.command == "freeze" or args.command == "outdated":
        args.func()
    else:
        parser.print_help()
