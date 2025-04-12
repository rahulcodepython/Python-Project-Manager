from .manager import Manager


class Outdated:
    """
    A class to handle outdated package operations using the Manager class.
    """

    def __init__(self) -> None:
        """
        Initialize the Outdated class with a Manager instance.
        """
        self.manager: Manager = Manager()

    def outdated(self) -> None:
        """
        Check for outdated packages and display them.
        """
        # Ensure the required files exist
        self._check_file_existence()

        # Check if the virtual environment is already created
        self.manager.create_virtualenv()

        # Display outdated packages
        self._show_outdated_packages()

    def _check_file_existence(self) -> None:
        """
        Wrapper for checking file existence using the Manager instance.
        """
        self.manager.check_file_existence()

    def _show_outdated_packages(self) -> None:
        """
        Wrapper for showing outdated packages using the Manager instance.
        """
        self.manager.show_outdated_packages()
