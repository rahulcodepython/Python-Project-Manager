import subprocess
from .decorators import operation_termination
from .manager import Manager


class List:
    """
    A class to handle listing installed Python packages using pip.
    """

    def __init__(self) -> None:
        """
        Initialize the List class with a Manager instance.
        """
        self.manager: Manager = Manager()

    @operation_termination
    def list(self) -> None:
        """
        List all installed Python packages using pip.

        This method checks for the existence of the required file
        and then executes a pip list command using a generated script.
        """
        # Ensure the required file exists
        self.manager.check_file_existence()

        # Generate the script for the pip list command
        script: str = self.manager.generate_script(["python -m pip list"])

        # Execute the script using subprocess
        subprocess.run(script, shell=True)
