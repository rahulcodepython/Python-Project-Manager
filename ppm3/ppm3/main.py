import argparse
from .src import Init, Install, Uninstall, Run, AddEnv, List, Freeze

# Define the version
VERSION = "0.0.9"


def main():
    parser = argparse.ArgumentParser(prog="ppm")
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
        help="show the version of ppm and exit",
    )

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
    uninstall_parser.add_argument(
        "-d", action="store_true", help="uninstall packages with dependencies"
    )
    uninstall_parser.set_defaults(func=Uninstall().uninstall)

    # Run command to run the code
    run_parser = subparsers.add_parser("run", help="run the project")
    run_parser.add_argument("script", nargs="+", help="Script to run in the project")
    run_parser.set_defaults(func=Run().run)

    # Add_Environment command to add environment file
    add_env_parser = subparsers.add_parser("add_env", help="add environment file")
    add_env_parser.add_argument(
        "values", nargs="*", help="Values to add in environment file"
    )
    add_env_parser.set_defaults(func=AddEnv().add_env)

    list_parser = subparsers.add_parser("list", help="list all the packages")
    list_parser.set_defaults(func=List().list)

    freeze_parser = subparsers.add_parser(
        "freeze", help="Generate requirements.txt file"
    )
    freeze_parser.set_defaults(func=Freeze().freeze)

    args = parser.parse_args()

    if args.command == "init":
        args.func(args.d)  # Pass the `-d` argument as `True` or `False`
    elif args.command == "install":
        args.func(args.packages)
    elif args.command == "uninstall":
        args.func(args.d, args.packages)
    elif args.command == "add_env":
        args.func(args.values)
    elif args.command == "run":
        args.func(args.script)
    elif args.command == "list":
        args.func()
    elif args.command == "freeze":
        args.func()
    else:
        parser.print_help()
