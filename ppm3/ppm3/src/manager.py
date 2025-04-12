import subprocess
import platform
import inquirer
import sys
import os
from ruamel.yaml import YAML
from .loading import Loading
from typing import List
from .constraints import VERSION, DEFAULT_DESCRIPTION, MAIN_FILE_NAME, MAIN_FILE_SOURCE, LICENSES, META_DATA_FILE_NAME, VIRTUAL_ENV_NAME, ENVIRONMENT_FILE_NAME, ROOT_PATH
from .decorators import operation_termination, loading_animation


class Manager:
    def __init__(self):
        self.pwd: str = os.getcwd()
        self.folder_name: str = os.path.basename(self.pwd)
        self.project_name: str = self.folder_name.lower()
        self.version: str = VERSION
        self.description: str = DEFAULT_DESCRIPTION
        self.main_file_name: str = MAIN_FILE_NAME
        self.source_folder_path: str = ROOT_PATH + MAIN_FILE_SOURCE
        self.main_file_path: str = self.source_folder_path + self.main_file_name
        self.git_init: bool = False
        self.git_repository: str = ""
        self.author: str = ""
        self.license: str = LICENSES
        self.python_version: str = sys.version.split(" ")[0]
        self.meta_data_file_name: str = META_DATA_FILE_NAME
        self.configuration_file_exists: bool = os.path.exists(
            self.meta_data_file_name)
        self.root_path: str = ROOT_PATH
        self.virtual_env_name: str = VIRTUAL_ENV_NAME
        self.environment_variable_name: str = ENVIRONMENT_FILE_NAME
        self.environment_variable_path: str = self.root_path + \
            self.environment_variable_name
        self.virtual_environment_activate_path = (
            os.path.join(self.virtual_env_name, "Scripts", "activate")
            if os.name == "nt"
            else os.path.join(self.virtual_env_name, "bin", "activate")
        )
        self.packages: List[str] = []
        self.config: dict = {
            "project": {
                "name": self.project_name,
                "version": self.version,
                "description": self.description,
                "main_file": self.main_file_name,
                "git_repository": self.git_repository,
                "author": self.author,
                "license": self.license,
            },
            "python_version": self.python_version,
            "environment": {
                "environment_name": self.virtual_env_name,
                "virtual_environment_activate_path": self.virtual_environment_activate_path,
            },
            "environment_variable": {
                "environment_variable_name": self.environment_variable_name,
                "environment_variable_path": self.environment_variable_name,
            },
            "commands": {
                "run": "python src/main.py"
            },
            "packages": self.packages,
        }
        self.animation = Loading()
        self.yaml = YAML()

    @operation_termination
    def choice_based_question(self, question: str, choices: List[str]) -> str:
        question = [
            inquirer.List(
                "choice",
                message=question,
                choices=choices,
                carousel=True,  # Allows navigation through choices in a loop
            )
        ]
        answer = inquirer.prompt(question)

        if answer is None:
            raise KeyboardInterrupt

        return answer["choice"]

    def check_file_existence(self):
        if self.configuration_file_exists:
            info = self.read_config()
            self.project_name = info["project"]["name"]
            self.version = info["project"]["version"]
            self.description = info["project"]["description"]
            self.main_file_name = info["project"]["main_file"]
            self.git_repository = info["project"]["git_repository"]
            self.author = info["project"]["author"]
            self.license = info["project"]["license"]
            self.packages = info["packages"]
            self.python_version = info["python_version"]
            self.virtual_env_name = info["environment"]["environment_name"]
            self.virtual_environment_activate_path = info["environment"]["virtual_environment_activate_path"]
            self.environment_variable_name = info["environment_variable"]["environment_variable_name"]
            self.config = info
        else:
            print(
                f"{self.meta_data_file_name} file not found. \nPPM is not initialized in your project.")
            sys.exit(0)

    def get_user_input(self, prompt: str, default: str) -> str:
        return input(f"{prompt} ({default}) ") or default

    def create_env_file(self) -> None:
        if os.path.isfile(self.environment_variable_path):
            override_env_file: bool = (
                self.choice_based_question(
                    f"{self.environment_variable_name} file already exists.",
                    ["Overwrite", "Keep as it is"],
                )
                == "Overwrite"
            )

            if override_env_file:
                with open(self.environment_variable_path, "w") as file:
                    file.write("")
                print(f"{self.environment_variable_name} file is overwritten.\n")

            else:
                print(f"{self.environment_variable_name} file is untouched.\n")

        else:
            with open(self.environment_variable_path, "w") as file:
                file.write("")
            print(f"{self.environment_variable_name} file is created.\n")

    def create_folders(self, path: str) -> None:
        folder_path = path.split("/")
        current_path = self.root_path
        for folder in folder_path:
            current_path += folder + "/"

            if not os.path.exists(current_path):
                os.makedirs(current_path, exist_ok=True)
        current_path = current_path[:-1]

    def create_project_folder_files(self) -> None:
        self.create_folders(self.source_folder_path)

        if os.path.exists(self.main_file_path):
            agree_to_override_main_file: bool = (
                self.choice_based_question(
                    f"Do you want to override {self.main_file_name} file?", [
                        "Yes", "No"]
                )
                == "Yes"
            )

            if not agree_to_override_main_file:
                print(f"{self.main_file_name} file is untouched.\n")
                return

        self.animation.start(
            f"Creating src folder and {self.main_file_name} file")

        with open(self.main_file_path, "w") as file:
            file.write(
                f"""def main() -> None:
    print('Hello, World!')
                
if __name__ == '__main__':
    main()
"""
            )
        self.animation.stop()
        print("src folder created. \n")

    @loading_animation(message="Creating virtual environment")
    def create_virtualenv(self) -> None:
        if not os.path.exists(self.virtual_env_name):
            subprocess.run(
                [sys.executable, "-m", "venv", self.virtual_env_name]
            )

    def generate_script(self, script: list[str]) -> str:
        if platform.system() == "Windows":
            return f"{self.virtual_environment_activate_path} && " + " && ".join(script)
        else:
            shell = os.getenv("SHELL", "/bin/bash")
            if "zsh" in shell:
                return (
                    f"zsh -c 'source {self.virtual_environment_activate_path} && "
                    + " && ".join(script)
                    + "'"
                )
            else:
                return (
                    f"bash -c 'source {self.virtual_environment_activate_path} && "
                    + " && ".join(script)
                    + "'"
                )

    def install_packages(self) -> None:
        command = self.generate_script(["python -m pip install --upgrade pip"])

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print("Failed to upgrade pip:", result.stderr)
            sys.exit(1)
        else:
            print(result.stdout)

        script: str = self.generate_script(
            ["python -m pip install --no-cache-dir " + " ".join(self.packages)]
        )

        result = subprocess.run(
            script, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            print("Failed to install packages:", result.stderr)
            sys.exit(1)
        else:
            print(result.stdout)

    def uninstall_packages(self) -> None:
        script: str = self.generate_script(
            ["python -m pip uninstall -y " +
                " ".join(self.packages)]
        )

        result = subprocess.run(
            script, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            print("Failed to uninstall packages:", result.stderr)
            sys.exit(1)
        else:
            print(result.stdout)

    @loading_animation(message="Listing dependencies")
    def get_pip_packages(self) -> None:
        command = self.generate_script(["python -m pip list --format=freeze"])

        result = subprocess.run(command, shell=True,
                                capture_output=True, text=True)

        # Each line is already in 'package==version' format
        output = [line for line in result.stdout.split(
            '\n') if len(line.strip()) > 0]
        self.config["packages"] = output

    @loading_animation(message="Creating configuration file")
    def create_write_configuration_file(self,) -> None:
        # Proper list indentation
        self.yaml.indent(mapping=2, sequence=4, offset=2)
        self.yaml.default_flow_style = False

        with open(self.meta_data_file_name, "w") as file:
            self.yaml.dump(self.config, file)

        print(f"\n\n{self.meta_data_file_name} file is created.", end="")

    def configure_project_by_user_input(self) -> None:
        print(f"""This utility will walk you through creating a {self.meta_data_file_name} file.
It only covers the most common items and meta data of the project.
        """
              )
        print("Press ^C at any time to quit.")
        print("Press Enter to use the default value. \n")

        self.project_name = self.get_user_input(
            "project name", self.project_name
        )
        self.version = self.get_user_input(
            "version", self.version)
        self.description = self.get_user_input(
            "description", self.description
        )
        self.main_file_name = self.get_user_input(
            "entry point", self.main_file_name
        )
        self.author = self.get_user_input(
            "author", self.author)
        self.license = self.get_user_input(
            "license", self.license)

        print("")
        github_conf = self.choice_based_question(
            "Do you want to add github configuration?",
            ["Yes", "No"],
        )
        if github_conf == "Yes":
            self.git_init = True
            self.git_repository = self.get_user_input(
                "github repository name", self.git_repository
            )

    def console_write_instructions(self) -> None:
        print(f"{self.project_name} project is created in {self.pwd}.\n")
        print(
            "This python project is built on python version",
            self.python_version,
            ".\n",
        )
        print("Congratulations! Your project is ready to go.\n")
        print("To install the dependencies, use the command 'ppm install'\n")
        print("To uninstall the dependencies, use the command 'ppm uninstall'\n")

        print("To run the project, use the command 'ppm run'\n")
        print(
            f"main.py file is created in src folder ({self.main_file_path}). You can start coding in main.py file.\n"
        )
        print("Happy coding!")

    def read_config(self):
        with open(self.meta_data_file_name, 'r') as file:
            return self.yaml.load(file)

    def freeze_requirements(self) -> None:
        with open("requirements.txt", "w") as file:
            for package in self.packages:
                file.write(f"{package}\n")

        print("requirements.txt file generated successfully\n")

    def show_outdated_packages(self) -> None:
        command = self.generate_script(["python -m pip list --outdated"])

        result = subprocess.run(command, shell=True,
                                capture_output=True, text=True)

        if result.stdout:
            print(result.stdout)
        else:
            print("No outdated packages found.")

    def parse_outdated_packages(self) -> None:
        command = self.generate_script(["python -m pip list --outdated"])

        result = subprocess.run(command, shell=True,
                                capture_output=True, text=True)

        outputs = result.stdout.splitlines()[2:]
        outputs = [f"{line.split()[0]}=={line.split()[1]}" for line in outputs]
        self.packages = outputs
