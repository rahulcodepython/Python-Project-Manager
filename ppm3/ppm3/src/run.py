import subprocess
import sys
from .default import PPM_Default


class Run:
    def __init__(self) -> None:
        self.ppm = PPM_Default()
        self.script = ""

    def create_script(self, script):
        run_script = ""

        # Read the configuration file
        with open(self.ppm.meta_data_file_name, "r") as file:
            contents = file.readlines()
            try:
                command_start = contents.index("[command]\n") + 1
                for line_content in contents[command_start:]:
                    if line_content == '\n':
                        break  # Stop at an empty line

                    key, value = line_content.strip().split(" = ")
                    command_value = value.replace('"', "").strip()

                    if len(script) == 0 and key == "run":
                        if len(command_value) == 0:
                            print("No command to run")
                            raise ValueError()
                        run_script = command_value
                        break
                    elif script and key == script[0]:
                        if len(command_value) == 0:
                            print("No command to run")
                            raise ValueError()
                        run_script = command_value
                        break
                else:
                    sys.exit(0)
            
            except ValueError:
                sys.exit(0)

        self.script = run_script

    def interpret_code(self):
        try:
            subprocess.run(self.script, shell=True)
        except (KeyboardInterrupt, SystemExit):
            ...

    def run(self, script):
        self.ppm.check_configuration_file_file()
        self.create_script(script)
        self.interpret_code()
