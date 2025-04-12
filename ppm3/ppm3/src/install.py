import sys
from typing import List, Optional
from .decorators import operation_termination
from .manager import Manager


class Install:
    """
    A class to handle the installation process of packages using a Manager instance.
    """

    def __init__(self) -> None:
        """
        Initialize the Install class with a Manager instance.
        """
        self.manager: Manager = Manager()

    @operation_termination
    def install(self, packages: Optional[List[str]] = None) -> None:
        """
        Install the specified packages or the default packages from the configuration.

        Args:
            packages (Optional[List[str]]): A list of package names to install. If None, 
                                            installs packages from the configuration.
        """
        # Ensure the required files exist
        self.manager.check_file_existence()

        # Determine the packages to install
        if packages is None:
            self._install_from_config()
        else:
            self.manager.packages = packages

        # Perform the installation process
        self._perform_installation()

    def _install_from_config(self) -> None:
        """
        Set up the virtual environment and load packages from the configuration.
        """
        self.manager.create_virtualenv()
        self.manager.packages = self.manager.config.get("packages", [])

    def _perform_installation(self) -> None:
        """
        Install the packages, retrieve installed pip packages, and write the configuration file.
        """
        self.manager.install_packages()
        self.manager.get_pip_packages()
        self.manager.create_write_configuration_file()
