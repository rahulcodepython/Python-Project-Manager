import subprocess
import platform
import inquirer
import sys
import os
from ruamel.yaml import YAML
from typing import List, Dict
from .loading import Loading
from .constraints import (
    VERSION, DEFAULT_DESCRIPTION, MAIN_FILE_NAME, MAIN_FILE_SOURCE, LICENSES,
    META_DATA_FILE_NAME, VIRTUAL_ENV_NAME, ENVIRONMENT_FILE_NAME, ROOT_PATH
)
from .decorators import operation_termination, loading_animation


class Manager:
    """
    Manager class to handle project initialization, configuration, and package management.
    """

    def __init__(self) -> None:
        # Paths and project metadata
        self.pwd: str = os.getcwd()
        self.folder_name: str = os.path.basename(self.pwd)
        self.project_name: str = self.folder_name.lower()
        self.version: str = VERSION
        self.description: str = DEFAULT_DESCRIPTION
        self.main_file_name: str = MAIN_FILE_NAME
        self.source_folder_path: str = os.path.join(
            ROOT_PATH, MAIN_FILE_SOURCE)
        self.main_file_path: str = os.path.join(
            self.source_folder_path, self.main_file_name)
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
        self.environment_variable_path: str = os.path.join(
            self.root_path, self.environment_variable_name)
        self.virtual_environment_activate_path: str = (
            os.path.join(self.virtual_env_name, "Scripts", "activate")
            if os.name == "nt"
            else os.path.join(self.virtual_env_name, "bin", "activate")
        )
        self.packages: List[str] = []
        self.config: Dict = self._initialize_config()
        self.animation: Loading = Loading()
        self.yaml: YAML = YAML()

    def _initialize_config(self) -> Dict:
        """
        Initialize the default configuration dictionary.
        """
        return {
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

    @operation_termination
    def choice_based_question(self, question: str, choices: List[str]) -> str:
        """
        Prompt the user with a choice-based question.
        """
        question_prompt = [
            inquirer.List(
                "choice",
                message=question,
                choices=choices,
                carousel=True,  # Allows navigation through choices in a loop
            )
        ]
        answer = inquirer.prompt(question_prompt)

        if answer is None:
            raise KeyboardInterrupt

        return answer["choice"]

    def check_file_existence(self) -> None:
        """
        Check if the configuration file exists and load its content.
        """
        if self.configuration_file_exists:
            info = self.read_config()
            self._update_config_from_file(info)
        else:
            print(
                f"{self.meta_data_file_name} file not found. \nPPM is not initialized in your project.")
            sys.exit(0)

    def _update_config_from_file(self, info: Dict) -> None:
        """
        Update the configuration from the loaded file.
        """
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

    def get_user_input(self, prompt: str, default: str) -> str:
        """
        Get user input with a default value.
        """
        return input(f"{prompt} ({default}) ") or default

    def create_env_file(self) -> None:
        """
        Create or overwrite the environment file.
        """
        if os.path.isfile(self.environment_variable_path):
            override_env_file = self.choice_based_question(
                f"{self.environment_variable_name} file already exists.",
                ["Overwrite", "Keep as it is"],
            ) == "Overwrite"

            if override_env_file:
                self._write_empty_file(self.environment_variable_path)
                print(f"{self.environment_variable_name} file is overwritten.\n")
            else:
                print(f"{self.environment_variable_name} file is untouched.\n")
        else:
            self._write_empty_file(self.environment_variable_path)
            print(f"{self.environment_variable_name} file is created.\n")

    @staticmethod
    def _write_empty_file(path: str) -> None:
        """
        Write an empty file at the specified path.
        """
        with open(path, "w") as file:
            file.write("")

    def create_folders(self, path: str) -> None:
        """
        Create folders recursively based on the given path.
        """
        os.makedirs(path, exist_ok=True)

    def create_project_folder_files(self) -> None:
        """
        Create the source folder and main file for the project.
        """
        self.create_folders(self.source_folder_path)

        if os.path.exists(self.main_file_path):
            agree_to_override_main_file = self.choice_based_question(
                f"Do you want to override {self.main_file_name} file?", [
                    "Yes", "No"]
            ) == "Yes"

            if not agree_to_override_main_file:
                print(f"{self.main_file_name} file is untouched.\n")
                return

        self.animation.start(
            f"Creating src folder and {self.main_file_name} file")
        self._write_main_file()
        self.animation.stop()
        print("src folder created. \n")

    def _write_main_file(self) -> None:
        """
        Write the default content to the main file.
        """
        with open(self.main_file_path, "w") as file:
            file.write(
                """def main() -> None:
    print('Hello, World!')

if __name__ == '__main__':
    main()
"""
            )

    @loading_animation(message="Creating virtual environment")
    def create_virtualenv(self) -> None:
        """
        Create a virtual environment for the project.
        """
        if not os.path.exists(self.virtual_env_name):
            subprocess.run(
                [sys.executable, "-m", "venv", self.virtual_env_name])

    def generate_script(self, script: List[str]) -> str:
        """
        Generate a shell script to run commands in the virtual environment.
        """
        if platform.system() == "Windows":
            return f"{self.virtual_environment_activate_path} && " + " && ".join(script)
        shell = os.getenv("SHELL", "/bin/bash")
        shell_type = "zsh" if "zsh" in shell else "bash"
        return f"{shell_type} -c 'source {self.virtual_environment_activate_path} && " + " && ".join(script) + "'"

    def install_packages(self) -> None:
        """
        Install packages in the virtual environment.
        """
        self._run_command(
            ["python -m pip install --upgrade pip"], "Failed to upgrade pip")
        self._run_command(
            [f"python -m pip install --no-cache-dir {' '.join(self.packages)}"],
            "Failed to install packages"
        )

    def uninstall_packages(self) -> None:
        """
        Uninstall packages from the virtual environment.
        """
        self._run_command(
            [f"python -m pip uninstall -y {' '.join(self.packages)}"],
            "Failed to uninstall packages"
        )

    def _run_command(self, commands: List[str], error_message: str) -> None:
        """
        Run a shell command and handle errors.
        """
        command = self.generate_script(commands)
        result = subprocess.run(command, shell=True,
                                capture_output=True, text=True)

        if result.returncode != 0:
            print(f"{error_message}:", result.stderr)
            sys.exit(1)
        else:
            print(result.stdout)

    @loading_animation(message="Listing dependencies")
    def get_pip_packages(self) -> None:
        """
        List installed pip packages and update the configuration.
        """
        command = self.generate_script(["python -m pip list --format=freeze"])
        result = subprocess.run(command, shell=True,
                                capture_output=True, text=True)
        self.config["packages"] = [line.strip()
                                   for line in result.stdout.splitlines() if line.strip()]

    @loading_animation(message="Creating configuration file")
    def create_write_configuration_file(self) -> None:
        """
        Create and write the configuration file.
        """
        self.yaml.indent(mapping=2, sequence=4, offset=2)
        self.yaml.default_flow_style = False

        with open(self.meta_data_file_name, "w") as file:
            self.yaml.dump(self.config, file)

        print(f"\n\n{self.meta_data_file_name} file is created.", end="")

    def configure_project_by_user_input(self) -> None:
        """
        Configure the project by prompting the user for input.
        """
        print(f"""This utility will walk you through creating a {self.meta_data_file_name} file.
It only covers the most common items and meta data of the project.
        """)
        print("Press ^C at any time to quit.")
        print("Press Enter to use the default value. \n")

        self.project_name = self.get_user_input(
            "project name", self.project_name)
        self.version = self.get_user_input("version", self.version)
        self.description = self.get_user_input("description", self.description)
        self.main_file_name = self.get_user_input(
            "entry point", self.main_file_name)
        self.author = self.get_user_input("author", self.author)
        self.license = self.get_user_input("license", self.license)

        print("")
        github_conf = self.choice_based_question(
            "Do you want to add github configuration?",
            ["Yes", "No"],
        )
        if github_conf == "Yes":
            self.git_init = True
            self.git_repository = self.get_user_input(
                "github repository name", self.git_repository)

    def console_write_instructions(self) -> None:
        """
        Print instructions for using the project.
        """
        print(f"{self.project_name} project is created in {self.pwd}.\n")
        print(
            f"This python project is built on python version {self.python_version}.\n")
        print("Congratulations! Your project is ready to go.\n")
        print("To install the dependencies, use the command 'ppm install'\n")
        print("To uninstall the dependencies, use the command 'ppm uninstall'\n")
        print("To run the project, use the command 'ppm run'\n")
        print(
            f"main.py file is created in src folder ({self.main_file_path}). You can start coding in main.py file.\n")
        print("Happy coding!")

    def read_config(self) -> Dict:
        """
        Read the configuration file and return its content.
        """
        with open(self.meta_data_file_name, 'r') as file:
            return self.yaml.load(file)

    def freeze_requirements(self) -> None:
        """
        Generate a requirements.txt file from the installed packages.
        """
        with open("requirements.txt", "w") as file:
            file.writelines(f"{package}\n" for package in self.packages)

        print("requirements.txt file generated successfully\n")

    def show_outdated_packages(self) -> None:
        """
        Show a list of outdated packages.
        """
        command = self.generate_script(["python -m pip list --outdated"])
        result = subprocess.run(command, shell=True,
                                capture_output=True, text=True)

        if result.stdout:
            print(result.stdout)
        else:
            print("No outdated packages found.")

    def parse_outdated_packages(self) -> None:
        """
        Parse outdated packages and update the package list.
        """
        command = self.generate_script(["python -m pip list --outdated"])
        result = subprocess.run(command, shell=True,
                                capture_output=True, text=True)

        outputs = result.stdout.splitlines()[2:]
        self.packages = [
            f"{line.split()[0]}=={line.split()[1]}" for line in outputs]
