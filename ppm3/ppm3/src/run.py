from .manager import Manager
import subprocess


class Run:
    def __init__(self):
        self.manager = Manager()

    def run(self, scripts) -> None:
        self.manager.check_file_existence()

        command = self.manager.config["commands"].get(
            "run" if not scripts else scripts[0], None)
        script = self.manager.generate_script([command])

        result = subprocess.run(
            script, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            print(result.stdout, end="")
        else:
            print(result.stderr, end="")
