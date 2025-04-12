from .manager import Manager


class Update:
    """
    A class to handle the update process for packages.

    Attributes:
        manager (Manager): An instance of the Manager class to handle package operations.
    """

    def __init__(self) -> None:
        """
        Initializes the Update class by creating an instance of the Manager class.
        """
        self.manager: Manager = Manager()

    def update(self, packages: list[str] | None) -> None:
        """
        Updates the packages by checking file existence, parsing outdated packages,
        installing packages, and writing configuration files.

        Args:
            packages (list[str] | None): A list of package names to update. If None, outdated packages are parsed.
        """
        # Ensure the required file exists
        self.manager.check_file_existence()

        # Check if the virtual environment is already created
        self.manager.create_virtualenv()

        # Determine the packages to update
        if packages is None or packages.__len__() == 0:
            self.manager.parse_outdated_packages()
        else:
            self.manager.packages = packages

        # Perform the update process
        self._perform_update()

    def _perform_update(self) -> None:
        """
        Performs the update process by installing packages, retrieving pip packages,
        and creating a configuration file.
        """
        self.manager.update_install_packages()
        self.manager.get_pip_packages()
        self.manager.create_write_configuration_file()
