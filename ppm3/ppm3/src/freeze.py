from .decorators import operation_termination
from .manager import Manager


class Freeze:
    """
    A class to handle the freezing process of a Python project.
    """

    def __init__(self) -> None:
        """
        Initialize the Freeze class with a Manager instance.
        """
        self.manager: Manager = Manager()

    @operation_termination
    def freeze(self) -> None:
        """
        Perform the freezing process by:
        1. Checking file existence.
        2. Creating a virtual environment.
        3. Freezing the requirements.
        """
        # Check if the necessary files exist
        self.manager.check_file_existence()

        # Create a virtual environment
        self.manager.create_virtualenv()

        # Freeze the requirements into a file
        self.manager.freeze_requirements()
