from .manager import Manager
import subprocess
from typing import List


class Run:
    """
    A class to handle the execution of scripts using the Manager class.
    """

    def __init__(self) -> None:
        """
        Initializes the Run class and sets up the Manager instance.
        """
        self.manager: Manager = Manager()

    def run(self, scripts: List[str] | None) -> None:
        """
        Executes the given scripts using the Manager's configuration.

        Args:
            scripts (List[str] | None): A list of script names to run. If empty, the default "run" command is used.
        """
        # Ensure the required file exists
        self.manager.check_file_existence()

        # Determine the command to execute
        command: str | None = self._get_command(scripts)

        # If no command is found in the configuration, notify the user and exit the method
        if command is None:
            print("No command found to execute.")
            return

        # Generate the script to execute
        script: str = self.manager.generate_script([command])

        # Execute the script and handle the result
        self._execute_script(script)

    def _get_command(self, scripts: List[str] | None) -> str | None:
        """
        Retrieves the command to execute based on the provided scripts.

        Args:
            scripts (List[str] | None): A list of script names.

        Returns:
            [str] | None: The command to execute.
        """
        return self.manager.config["commands"].get(
            "run" if not scripts else scripts[0], None
        )

    @staticmethod
    def _execute_script(script: str) -> None:
        """
        Executes the given script and prints the output or error.

        Args:
            script (str): The script to execute.
        """
        result: subprocess.CompletedProcess = subprocess.run(
            script, shell=True, capture_output=True, text=True
        )

        if result.returncode == 0:
            print(result.stdout, end="")
        else:
            print(result.stderr, end="")
