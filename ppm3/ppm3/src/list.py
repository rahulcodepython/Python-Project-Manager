from .decorators import operation_termination
from .default import PPM_Default
import subprocess


class List:
    def __init__(self):
        self.ppm = PPM_Default()

    @operation_termination
    def list(self):
        self.ppm.check_configuration_file_file()
        self.ppm.create_virtualenv()
        try:
            subprocess.run(
                self.ppm.generate_script(["pip list"]),
                shell=True,
            )
        except (KeyboardInterrupt, SystemExit):
            ...
