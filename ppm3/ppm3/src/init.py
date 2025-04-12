# from .default import PPM_Default
from .decorators import operation_termination
from .manager import Manager
import sys


class Init:
    def __init__(self) -> None:
        self.manager = Manager()

    @operation_termination
    def init(self, set_default: bool = False) -> None:
        if self.manager.configuration_file_exists:
            print(f"{self.meta_data_file_name} already exists. \nPPM is initialized in your project. \nTo reconfigure PPM you need to remove the {self.meta_data_file_name} file.")
            sys.exit(0)

        (
            self.manager.configure_project_by_user_input()
            if not set_default
            else print("Default values are selected.\n")
        )
        self.manager.create_env_file()
        self.manager.create_project_folder_files()
        self.manager.create_virtualenv()
        self.manager.install_packages()
        self.manager.get_pip_packages()
        self.manager.create_write_configuration_file()
        self.manager.console_write_instructions()  # Uncommented to print instructions


# ppm run
