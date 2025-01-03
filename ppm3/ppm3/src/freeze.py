from .decorators import operation_termination
from .default import PPM_Default
import subprocess


class Freeze:
    def __init__(self):
        self.ppm = PPM_Default()

    @operation_termination
    def freeze(self):
        self.ppm.check_configuration_file_file()
        self.ppm.create_virtualenv()
        try:
            result = subprocess.run(
                self.ppm.generate_script(["pip freeze > requirements.txt"]),
                shell=True,
            )
            if result.returncode == 0:
                print("requirements.txt file generated successfully")
        except (KeyboardInterrupt, SystemExit):
            ...
