import subprocess
import platform
import inquirer
import sys
import os
import json
from .loading import Loading
from typing import List, Literal


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

    def ask_choice_question(self, question: str, choices: List[str]) -> str:
        question = [
            inquirer.List(
                "choice",
                message=question,
                choices=choices,
                carousel=True,  # Allows navigation through choices in a loop
            )
        ]
        try:
            answer = inquirer.prompt(question)

            if answer is None:
                raise KeyboardInterrupt

            return answer["choice"]

        except KeyboardInterrupt:
            print("Operation is terminated.")
            sys.exit(0)

    def valided_user_input(self, prompt: str, default: str) -> str:
        try:
            return input(f"{prompt} ({default}) ") or default
        except KeyboardInterrupt:
            print("Operation is terminated.")
            sys.exit(0)

    def get_package_name_for_installation(self) -> None:
        print("\nAdd the packages you want to install in the project.")
        print(
            "Enter the package name like (<package_name>==<version>) or (<package_name>) to install spacific version or latest version."
        )

        try:
            while True:
                package_name: str = input(
                    "Enter package name to install (press Enter to end): "
                )
                if package_name:
                    self.packages.append(package_name)
                else:
                    break
        except KeyboardInterrupt:
            print("Operation is terminated.")
            sys.exit(0)
        finally:
            print("\n")

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

    def create_virtualenv(self, animation=False, show_print_statement=True) -> None:
        self.animation.start("Creating virtual environment") if animation else None
        if not os.path.exists(self.virtual_environment_name):
            subprocess.run(
                [sys.executable, "-m", "venv", self.virtual_environment_name]
            )

            self.animation.stop()
            if show_print_statement:
                print("Virtual environment created.\n")
        else:
            self.animation.stop()
            if show_print_statement:
                print("Virtual environment already exists.\n")

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
        if self.usage_of_ppm == "as a dependency manager":
            return

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
                """from dotenv import load_dotenv
import os
                    
load_dotenv()
                
# to use environment variables
# os.getenv('ENV_VARIABLE_NAME')
                
def main() -> None:
    print('Hello, World!')
                
if __name__ == '__main__':
    main()
"""
            )
        self.animation.stop()
        print("src folder created. \n")

    def install_packages(self, animation=False, show_print_statement=True) -> None:
        self.animation.start("Installing packages") if animation else None

        self.packages.append("pipdeptree")

        script: str = self.generate_script(
            ["pip install --no-cache-dir " + " ".join(self.packages)]
        )
        result = subprocess.run(script, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            self.animation.stop()
            print("An error occurred while checking packages. Please try again.")
            print(f"Error message is {result.stderr}")
            sys.exit(0)

        self.animation.stop()
        if show_print_statement:
            print("All packages installed.\n")

    def uninstall_packages(self, animation=False) -> None:
        self.animation.start("Uninstalling packages") if animation else None

        script: str = self.generate_script(
            ["python -m pip uninstall " + " ".join(self.packages) + " -y"]
        )
        result = subprocess.run(script, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            self.animation.stop()
            print("An error occurred while checking packages. Please try again.")
            print(f"Error message is {result.stderr}")
            sys.exit(0)

        self.animation.stop()
        print("All packages uninstalled.\n")

    def parse_installed_package_dependency(
        self, animation=False, show_print_statement=True
    ) -> None:
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
                print("An error occurred while checking packages. Please try again.")
                print(f"Error message is {e}")
                sys.exit(0)

        self.animation.start("Checking packages") if animation else None
        script: str = self.generate_script(["pipdeptree --json"])
        result = subprocess.run(script, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            format_package_dependency(result)
        else:
            self.animation.stop()
            print("An error occurred while checking packages. Please try again.")
            print(f"Error message is {result.stderr}")
            sys.exit(0)

        self.animation.stop()
        if show_print_statement:
            print("All packages checked.\n")

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
[environment_variables]\n"""

            if self.agree_to_create_env_file:
                file_content += f"""path = "{self.environment_variable_path}{self.environment_variable_name}"
\n\n"""

            file_content += (
                f"""[command]
run = "python {self.entry_point_path}{self.entry_point}"\n\n
"""
                if self.usage_of_ppm == "as a project manager"
                else """"""
            )

            formated_dependencies = self.format_dependencies()
            file_content += formated_dependencies

            return file_content

        self.animation.start(f"Creating {self.meta_data_file_name} file")

        file_content = write_file_content()

        with open(self.meta_data_file_name, "w") as file:
            file.write(file_content)

        self.animation.stop()
        print(f"{self.meta_data_file_name} file is created.")

    def console_write_instructions(self) -> None:
        print(
            f"\n{self.project_name} project is created in {self.current_working_directory}."
        )
        print("This python project is built on python version", self.python_version)
        print("Congratulations! Your project is ready to go.")
        print("To install the dependencies, use the command 'ppm install'")

        if self.usage_of_ppm == "as a project manager":
            print("To run the project, use the command 'ppm run'")
            print(
                f"main.py file is created in src folder ({ self.entry_point_path}). You can start coding in main.py file."
            )
        print("Happy coding!")

    def overwrite_configuration_file(
        self, animation=False, show_print_statement=True
    ) -> None:
        (
            self.animation.start(f"Overwritting {self.meta_data_file_name} file")
            if animation
            else None
        )

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

        self.animation.stop()
        if show_print_statement:
            print(f"{self.meta_data_file_name} file is overwritten.\n")
