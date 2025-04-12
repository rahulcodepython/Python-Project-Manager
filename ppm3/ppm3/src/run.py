from .manager import Manager
import subprocess
from typing import List, Optional


class Run:
    """
    A class to handle the execution of scripts using the Manager class.
    """

    def __init__(self) -> None:
        """
        Initializes the Run class and sets up the Manager instance.
        """
        self.manager: Manager = Manager()

    def run(self, scripts: Optional[List[str]]) -> None:
        """
        Executes the given scripts using the Manager's configuration.

        Args:
            scripts (Optional[List[str]]): A list of script names to run. If empty, the default "run" command is used.
        """
        # Ensure the required file exists
        self.manager.check_file_existence()

        # Determine the command to execute
        command: Optional[str] = self._get_command(scripts)

        # Generate the script to execute
        script: str = self.manager.generate_script([command])

        # Execute the script and handle the result
        self._execute_script(script)

    def _get_command(self, scripts: Optional[List[str]]) -> Optional[str]:
        """
        Retrieves the command to execute based on the provided scripts.

        Args:
            scripts (Optional[List[str]]): A list of script names.

        Returns:
            Optional[str]: The command to execute.
        """
        return self.manager.config["commands"].get(
            "run" if not scripts else scripts[0], None
        )

    def _execute_script(self, script: str) -> None:
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
