from .default import PPM_Default
import os


class AddEnv:
    def __init__(self) -> None:
        self.ppm = PPM_Default()

    def create_env_file(self, values):
        if os.path.isfile(
            self.ppm.environment_variable_path + self.ppm.environment_variable_name
        ):
            override_env_file: bool = (
                self.ppm.ask_choice_question(
                    f"{self.ppm.environment_variable_name} file already exists.",
                    ["Overwrite", "Keep as it is"],
                )
                == "Overwrite"
            )

            if override_env_file:
                with open(
                    self.ppm.environment_variable_path
                    + self.ppm.environment_variable_name,
                    "w",
                ) as file:
                    index = 0
                    while index + 1 < len(values):
                        file.write(f'{values[index]}="{values[index+1]}"\n')
                        index += 2
                print(f"{self.ppm.environment_variable_name} file is overwritten.\n")

            else:
                print(f"{self.ppm.environment_variable_name} file is untouched.\n")

        else:
            self.ppm.agree_to_create_env_file = (
                self.ppm.ask_choice_question(
                    f"Are you sure you want to add {self.ppm.environment_variable_name} file?",
                    ["Yes", "No"],
                )
                == "Yes"
            )

            if self.ppm.agree_to_create_env_file:
                self.ppm.create_folders(self.ppm.environment_variable_path)

                with open(
                    self.ppm.environment_variable_path
                    + self.ppm.environment_variable_name,
                    "w",
                ) as file:
                    index = 0
                    while index + 1 < len(values):
                        file.write(f'{values[index]}="{values[index+1]}"\n')
                        index += 2
                print(f"{self.ppm.environment_variable_name} file is created.\n")

    def add_env(self, values):
        self.create_env_file(values)
