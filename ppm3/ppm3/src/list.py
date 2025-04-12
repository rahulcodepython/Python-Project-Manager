from .decorators import operation_termination
from .manager import Manager
import subprocess


class List:
    def __init__(self):
        self.manager = Manager()

    @operation_termination
    def list(self):
        self.manager.check_file_existence()
        subprocess.run(
            self.manager.generate_script(["python -m pip list"]),
            shell=True,
        )
