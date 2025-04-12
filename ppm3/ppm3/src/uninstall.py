from .decorators import operation_termination
from .manager import Manager
import sys


class Uninstall:
    def __init__(self) -> None:
        self.manager = Manager()

    @operation_termination
    def uninstall(self, packages: list[str]) -> None:
        self.manager.check_file_existence()

        if packages.__len__() == 0:
            print("No packages provided. Please provide a list of packages to install.")
            sys.exit(0)

        self.manager.packages = packages
        self.manager.uninstall_packages()
        self.manager.get_pip_packages()
        self.manager.create_write_configuration_file()
