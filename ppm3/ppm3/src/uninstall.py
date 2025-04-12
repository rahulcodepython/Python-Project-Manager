import sys
from typing import List
from .decorators import operation_termination
from .manager import Manager


class Uninstall:
    """
    A class to handle the uninstallation of packages using the Manager class.
    """

    def __init__(self) -> None:
        """
        Initializes the Uninstall class with a Manager instance.
        """
        self.manager: Manager = Manager()

    @operation_termination
    def uninstall(self, packages: List[str]) -> None:
        """
        Uninstalls the specified packages.

        Args:
            packages (List[str]): A list of package names to uninstall.

        Raises:
            SystemExit: If no packages are provided.
        """
        # Ensure the configuration file exists
        self.manager.check_file_existence()

        # Check if the packages list is empty
        if not packages:
            print("No packages provided. Please provide a list of packages to uninstall.")
            sys.exit(0)

        # Set the packages to be uninstalled
        self.manager.packages = packages

        # Perform the uninstallation process
        self.manager.uninstall_packages()

        # Update the list of installed pip packages
        self.manager.get_pip_packages()

        # Create and write the updated configuration file
        self.manager.create_write_configuration_file()
