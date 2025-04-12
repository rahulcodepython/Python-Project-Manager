import sys
from .decorators import operation_termination
from .manager import Manager


class Init:
    """
    A class to initialize and configure the project using PPM (Python Project Manager).
    """

    def __init__(self) -> None:
        """
        Initializes the Init class with a Manager instance.
        """
        self.manager: Manager = Manager()

    @operation_termination
    def init(self, set_default: bool = False) -> None:
        """
        Initializes the project by creating necessary configurations and files.

        Args:
            set_default (bool): If True, uses default configuration values. Defaults to False.
        """
        if self.manager.configuration_file_exists:
            self._handle_existing_configuration()
            return

        if set_default:
            print("Default values are selected.\n")
        else:
            self.manager.configure_project_by_user_input()

        self._setup_project()

    def _handle_existing_configuration(self) -> None:
        """
        Handles the case where a configuration file already exists.
        """
        print(
            f"{self.meta_data_file_name} already exists.\n"
            f"PPM is initialized in your project.\n"
            f"To reconfigure PPM, you need to remove the {self.meta_data_file_name} file."
        )
        sys.exit(0)

    def _setup_project(self) -> None:
        """
        Sets up the project by creating necessary files, virtual environment, and installing packages.
        """
        self.manager.create_env_file()
        self.manager.create_project_folder_files()
        self.manager.create_virtualenv()
        self.manager.install_packages()
        self.manager.get_pip_packages()
        self.manager.create_write_configuration_file()
        self.manager.console_write_instructions()  # Prints instructions to the console
