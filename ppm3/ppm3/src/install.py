from typing import List
from .decorators import operation_termination
from .manager import Manager


class Install:
    """
    A class to handle the installation process of packages using a Manager instance.
    """

    def __init__(self) -> None:
        """
        Initialize the class named 'Install' with a Manager instance.
        """
        self.manager: Manager = Manager()

    @operation_termination
    def install(self, packages: List[str] | None = None) -> None:
        """
        Install the specified packages or the default packages from the configuration.

        Args:
            packages ([List[str]] | None): A list of package names to install. If None, 
                                            installs packages from the configuration.
        """
        # Ensure the required files exist
        self.manager.check_file_existence()

        # Check if the virtual environment is already created
        self.manager.create_virtualenv()

        # Determine the packages to install
        if packages is None or packages.__len__() == 0:
            self._install_from_config()
        else:
            self.manager.packages = packages

        # Perform the installation process
        self._perform_installation()

    def _install_from_config(self) -> None:
        """
        Load packages from the configuration.
        """
        self.manager.packages = self.manager.config.get("packages", [])

    def _perform_installation(self) -> None:
        """
        Install the packages, retrieve installed pip packages, and write the configuration file.
        """
        self.manager.install_packages()
        self.manager.get_pip_packages()
        self.manager.create_write_configuration_file()
