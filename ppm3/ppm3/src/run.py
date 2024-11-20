import subprocess
import sys
from .default import PPM_Default


class Run:
    def __init__(self) -> None:
        self.ppm = PPM_Default()
        self.script = ""

    def create_script(self):
        run_script = ""

        with open(self.ppm.meta_data_file_name, "r") as file:
            contents = file.readlines()
            line = contents[contents.index("[command]\n") + 1]
            line_content = line.split(" = ")

            if "run" in line_content:
                run_script = line_content[1].replace("\n", "").replace('"', "")
            else:
                self.ppm.animation.stop(
                    "No run command found in the configuration file"
                )
                sys.exit(0)

        self.script = self.ppm.generate_script([run_script])

    def interpret_code(self):
        try:
            subprocess.run(self.script, shell=True)
        except (KeyboardInterrupt, SystemExit):
            ...

    def run(self):
        self.ppm.check_configuration_file_file()
        self.create_script()
        self.interpret_code()
