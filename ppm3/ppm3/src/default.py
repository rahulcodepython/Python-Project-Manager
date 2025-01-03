import subprocess
import platform
import inquirer
import sys
import os
import json
from .loading import Loading
from typing import List, Literal
from colorama import Fore, Style


class PPM_Default:
    def __init__(self):
        self.usage_of_ppm: Literal[
            "as a project manager", "as a dependency manager"
        ] = "as a project manager"
        self.current_working_directory: str = os.getcwd()
        self.current_folder_name: str = os.path.basename(self.current_working_directory)
        self.project_name: str = self.current_folder_name.lower()
        self.version: str = "1.0.0"
        self.description: str = ""
        self.entry_point: str = "main.py"
        self.entry_point_path: str = f"./src/"
        self.git_init: bool = False
        self.git_repository: str = ""
        self.author: str = ""
        self.license: str = "ISC"
        self.agree_to_create_env_file: bool = True
        self.python_version: str = sys.version.split(" ")[0]
        self.meta_data_file_name: str = "ppm.toml"
        self.configuration_file_exists: bool = os.path.exists(self.meta_data_file_name)
        self.virtual_environment_name: str = ".venv"
        self.environment_variable_name: str = ".env"
        self.environment_variable_path: str = f"./"
        self.virtual_environment_activate_path = (
            os.path.join(self.virtual_environment_name, "Scripts", "activate")
            if os.name == "nt"
            else os.path.join(self.virtual_environment_name, "bin", "activate")
        )
        self.packages: List[str] = []
        self.package_dependency: dict = {}
        self.animation = Loading()

    # @operation_termination
    def ask_choice_question(self, question: str, choices: List[str]) -> str:
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

    def check_configuration_file_file(self) -> None:
        if not self.configuration_file_exists:
            self.animation.stop()
            print(
                f"{self.meta_data_file_name} file not found. Please run 'ppm init' command to create {self.meta_data_file_name} file."
            )
            sys.exit(0)

    def valided_user_input(self, prompt: str, default: str) -> str:
        return input(f"{prompt} ({default}) ") or default

    def get_package_name_for_installation(self) -> None:
        print(
            "\nEnter the name of the packages you want to install in the project like (<package_name>==<version>) or (<package_name>)."
        )
        package_name: str = input("Packages (press Enter to end): ")
        if package_name:
            self.packages += package_name.split(" ")

        print("")

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

    def create_virtualenv(self) -> None:
        if not os.path.exists(self.virtual_environment_name):
            subprocess.run(
                [sys.executable, "-m", "venv", self.virtual_environment_name]
            )

    def create_folders(self, path: str) -> None:
        folder_path = path.split("/")
        current_path = "./"
        for folder in folder_path:
            current_path += folder + "/"

            if not os.path.exists(current_path):
                os.makedirs(current_path, exist_ok=True)
        current_path = current_path[:-1]

    def create_env_file(self) -> None:
        if os.path.isfile(
            self.environment_variable_path + self.environment_variable_name
        ):
            override_env_file: bool = (
                self.ask_choice_question(
                    f"{self.environment_variable_name} file already exists.",
                    ["Overwrite", "Keep as it is"],
                )
                == "Overwrite"
            )

            if override_env_file:
                with open(
                    self.environment_variable_path + self.environment_variable_name, "w"
                ) as file:
                    file.write("")
                print(f"{self.environment_variable_name} file is overwritten.\n")

            else:
                print(f"{self.environment_variable_name} file is untouched.\n")

        else:
            self.agree_to_create_env_file: bool = (
                self.ask_choice_question(
                    f"Are you sure you want to add {self.environment_variable_name} file?",
                    ["Yes", "No"],
                )
                == "Yes"
            )

            if self.agree_to_create_env_file:
                self.create_folders(self.environment_variable_path)

                with open(
                    self.environment_variable_path + self.environment_variable_name, "w"
                ) as file:
                    file.write("")
                print(f"{self.environment_variable_name} file is created.\n")

    def create_project_folder_files(self) -> None:
        self.create_folders(self.entry_point_path)

        if os.path.exists(self.entry_point_path + self.entry_point):
            agree_to_override_main_file: bool = (
                self.ask_choice_question(
                    f"Do you want to override {self.entry_point} file?", ["Yes", "No"]
                )
                == "Yes"
            )

            if not agree_to_override_main_file:
                print(f"{self.entry_point} file is untouched.\n")
                return

        self.animation.start(f"Creating src folder and {self.entry_point} file")

        with open(self.entry_point_path + self.entry_point, "w") as file:
            file.write(
                f"""{"from dotenv import load_dotenv\nimport os\nload_dotenv()\n# to use environment variables\n# os.getenv('ENV_VARIABLE_NAME')" if self.agree_to_create_env_file else ''}
                
def main() -> None:
    print('Hello, World!')
                
if __name__ == '__main__':
    main()
"""
            )
        self.animation.stop()
        print("src folder created. \n")

    def install_packages(self) -> None:
        self.packages.append("pipdeptree")

        result = subprocess.run(
            self.generate_script(["python -m pip install --upgrade pip"]),
            shell=True,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            ...

        script: str = self.generate_script(
            ["pip install --no-cache-dir " + " ".join(self.packages)]
        )
        result = subprocess.run(script, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            self.animation.stop()
            print(Fore.RED + result.stderr + Style.RESET_ALL)
            sys.exit(0)

    def uninstall_packages(self) -> None:

        script: str = self.generate_script(
            ["python -m pip uninstall " + " ".join(self.packages) + " -y"]
        )
        result = subprocess.run(script, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            self.animation.stop()
            print(Fore.RED + result.stderr + Style.RESET_ALL)
            sys.exit(0)

    def parse_installed_package_dependency(self) -> None:
        def format_package_dependency(result: str) -> None:
            try:
                for package in json.loads(result.stdout):
                    package_name = f"{package['package']['package_name']}=={
                        package['package']['installed_version']}"
                    dependencies = [
                        f"{dep['package_name']}=={dep['installed_version']}"
                        for dep in package["dependencies"]
                    ]
                    self.package_dependency[package_name] = dependencies

                def build_nested_structure(package_name):
                    if package_name not in self.package_dependency:
                        return []
                    nested_dependencies = []
                    for dep in self.package_dependency[package_name]:
                        nested_dependencies.append({dep: build_nested_structure(dep)})
                    return nested_dependencies

                nested_dict = {}
                for package_name in self.package_dependency:
                    is_top_level = all(
                        package_name not in deps
                        for deps in self.package_dependency.values()
                    )
                    if is_top_level:
                        nested_dict[package_name] = build_nested_structure(package_name)

                list_of_nested_dict = list(nested_dict.items())

                for i, value in enumerate(list(nested_dict.keys())):
                    if value.startswith("pipdeptree=="):
                        del list_of_nested_dict[i]
                        break

                self.package_dependency = dict(list_of_nested_dict)
            except Exception as e:
                self.animation.stop()
                print("An error occurred while checking packages. Please try again.")
                print(f"Error message is {e}")
                sys.exit(0)

        script: str = self.generate_script(["pipdeptree --json"])
        result = subprocess.run(script, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            format_package_dependency(result)
        else:
            self.animation.stop()
            print(Fore.RED + result.stderr + Style.RESET_ALL)

    def format_dependencies(self) -> str:
        output = "[dependencies]\n"

        def process_package(package, dependencies, level=0):
            indent = "\t" * level
            output_lines = [f"{indent}{'-' if level > 0 else ''}{package}"]

            for dependency in dependencies:
                for dep_name, sub_deps in dependency.items():
                    output_lines.extend(process_package(dep_name, sub_deps, level + 1))

            return output_lines

        for package, dependencies in self.package_dependency.items():
            output += "\n".join(process_package(package, dependencies)) + "\n"

        return output

    def create_configuration_file(self) -> None:
        def write_file_content() -> str:
            file_content: str = """"""

            file_content += (
                f"""[project]
name = "{self.project_name}"
version = "{self.version}"
description = "{self.description}"
entry_point = "{self.entry_point_path}{self.entry_point}"
git_repository = "{self.git_repository}"
author = "{self.author}"
license = "{self.license}"
\n\n"""
                if self.usage_of_ppm == "as a project manager"
                else """"""
            )

            file_content += f"""[python]
python_version = "{self.python_version}" \n\n
[environment]
path = "{self.virtual_environment_activate_path}" \n\n
[environment_variables]
"""

            if self.agree_to_create_env_file:
                file_content += f"""path = "{self.environment_variable_path}{self.environment_variable_name}"
\n\n"""

            file_content += (
                f"""[command]
run = "python {self.entry_point_path}{self.entry_point}"\n\n
"""
                if self.usage_of_ppm == "as a project manager"
                else """[command]
run = "" \n\n
"""
            )

            formated_dependencies = self.format_dependencies()
            file_content += formated_dependencies

            return file_content

        file_content = write_file_content()

        with open(self.meta_data_file_name, "w") as file:
            file.write(file_content)

    def overwrite_configuration_file(self) -> None:
        formated_dependencies = self.format_dependencies()

        with open(self.meta_data_file_name, "r") as file:
            lines = file.readlines()

        try:
            char_index = lines.index("[dependencies]\n")
        except ValueError:
            ...
        else:
            lines = lines[:char_index] + [formated_dependencies]

            with open(self.meta_data_file_name, "w") as file:
                file.writelines(lines)

    def git_initiate(self) -> None:
        try:
            if self.git_init:
                result = subprocess.run(
                    self.generate_script(
                        ["git init", f"git remote add origin {self.git_repository}"]
                    ),
                    shell=True,
                )
        except Exception as e:
            self.animation.stop()
            print(f"An error occurred while initiating git. Error message is {e}")
            sys.exit(0)
