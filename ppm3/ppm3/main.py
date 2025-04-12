import argparse
from .src import Init, List, Freeze, Install, Run, Outdated, Update, Uninstall
from .src.constraints import VERSION

# Define the version
version: str = VERSION


def main() -> None:
    """
    Entry point for the ppm CLI tool.
    Parses command-line arguments and executes the corresponding functionality.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(prog="ppm")
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"The version of ppm is {version}",
        help="Show the version of ppm and exit",
    )

    subparsers: argparse._SubParsersAction = parser.add_subparsers(
        dest="command")

    # Init command with -y flag
    def _add_init_parser(subparsers: argparse._SubParsersAction) -> None:
        init_parser: argparse.ArgumentParser = subparsers.add_parser(
            "init", help="Initializes a new project"
        )
        init_parser.add_argument(
            "-y", action="store_true", help="Accept default configuration"
        )
        init_parser.set_defaults(func=Init().init)

    # Install command with multiple arguments support
    def _add_install_parser(subparsers: argparse._SubParsersAction) -> None:
        install_parser: argparse.ArgumentParser = subparsers.add_parser(
            "install", help="Install packages in the project"
        )
        install_parser.add_argument(
            "packages", nargs="*", help="Packages to install"
        )
        install_parser.set_defaults(func=Install().install)

    # Uninstall command with multiple arguments support
    def _add_uninstall_parser(subparsers: argparse._SubParsersAction) -> None:
        uninstall_parser: argparse.ArgumentParser = subparsers.add_parser(
            "uninstall", help="Uninstall packages in the project"
        )
        uninstall_parser.add_argument(
            "packages", nargs="*", help="Packages to uninstall"
        )
        uninstall_parser.set_defaults(func=Uninstall().uninstall)

    # Run command to run the code
    def _add_run_parser(subparsers: argparse._SubParsersAction) -> None:
        run_parser: argparse.ArgumentParser = subparsers.add_parser(
            "run", help="Run the project"
        )
        run_parser.add_argument(
            "script", nargs="*", help="Script to run in the project"
        )
        run_parser.set_defaults(func=Run().run)

    # List command to list all packages
    def _add_list_parser(subparsers: argparse._SubParsersAction) -> None:
        list_parser: argparse.ArgumentParser = subparsers.add_parser(
            "list", help="List all the packages"
        )
        list_parser.set_defaults(func=List().list)

    # Freeze command to generate requirements.txt
    def _add_freeze_parser(subparsers: argparse._SubParsersAction) -> None:
        freeze_parser: argparse.ArgumentParser = subparsers.add_parser(
            "freeze", help="Generate requirements.txt file"
        )
        freeze_parser.set_defaults(func=Freeze().freeze)

    # Outdated command to show outdated packages
    def _add_outdated_parser(subparsers: argparse._SubParsersAction) -> None:
        outdated_parser: argparse.ArgumentParser = subparsers.add_parser(
            "outdated", help="Show outdated packages"
        )
        outdated_parser.set_defaults(func=Outdated().outdated)

    # Update command to update packages
    def _add_update_parser(subparsers: argparse._SubParsersAction) -> None:
        update_parser: argparse.ArgumentParser = subparsers.add_parser(
            "update", help="Update packages in the project"
        )
        update_parser.add_argument(
            "packages", nargs="*", help="Packages to update"
        )
        update_parser.set_defaults(func=Update().update)

    # Add all parsers
    _add_init_parser(subparsers)
    _add_install_parser(subparsers)
    _add_uninstall_parser(subparsers)
    _add_run_parser(subparsers)
    _add_list_parser(subparsers)
    _add_freeze_parser(subparsers)
    _add_outdated_parser(subparsers)
    _add_update_parser(subparsers)

    # Parse arguments
    args: argparse.Namespace = parser.parse_args()

    # Execute the appropriate function based on the command
    if args.command in {"init", "install", "update", "uninstall", "run"}:
        _execute_command_with_args(args)
    elif args.command in {"list", "freeze", "outdated"}:
        args.func()
    else:
        parser.print_help()


def _execute_command_with_args(args: argparse.Namespace) -> None:
    """
    Helper function to execute commands that require arguments.
    """
    if args.command == "init":
        args.func(args.y)  # Pass the `-y` argument as `True` or `False`
    elif args.command in {"install", "update", "uninstall"}:
        args.func(args.packages)
    elif args.command == "run":
        args.func(args.script)


if __name__ == "__main__":
    main()
