import subprocess
import threading
import inquirer
import time
import sys
import os
import json


class Init():
    def __init__(self) -> None:
        self.current_working_directory: str = os.getcwd()
        self.current_folder_name: str = os.path.basename(
            self.current_working_directory)
        self.entry_point_path: str = f"./src/"
        self.project_name: str = self.current_folder_name.lower()
        self.version: str = "1.0.0"
        self.description: str = ""
        self.entry_point: str = "main.py"
        self.git_repository: str = ""
        self.author: str = ""
        self.license: str = "ISC"
        self.agree_to_create_env_file: bool = True
        self.python_version: str = sys.version.split(" ")[0]
        self.meta_data_file_name: str = "ppm.toml"
        self.virtual_environment_name: str = ".venv"
        self.environment_variable_name: str = ".env"
        self.virtual_environment_activate_script = os.path.join(
            self.virtual_environment_name, "Scripts", "activate") if os.name == "nt" else os.path.join(self.virtual_environment_name, "bin", "activate")
        self.packages: list[str] = []
        self.package_dependency: dict = {}
        self.stop_event = threading.Event()
        self.animation_thread = None

    def loading_animation(self, msg: str) -> None:
        while not self.stop_event.is_set():
            for frame in ["   ", ".  ", ".. ", "...", ".. ", ".  "]:
                print(f"\r{msg} {frame}", end="")
                time.sleep(0.3)

    def start_animation(self, message: str):
        if self.animation_thread and self.animation_thread.is_alive():
            self.stop_animation()

        self.stop_event.clear()
        self.animation_thread = threading.Thread(
            target=self.loading_animation, args=(message,))
        self.animation_thread.start()

    def stop_animation(self):
        if self.animation_thread:
            self.stop_event.set()
            self.animation_thread.join()
            self.animation_thread = None

    def get_user_input_for_package(self) -> None:
        while True:
            package_name: str = input(
                "Enter package name to install (press Enter to end): ")
            if package_name:
                self.packages.append(package_name)
            else:
                break

    def valided_user_input(self, prompt: str, default: str) -> str:
        try:
            user_input: str = input(f"{prompt} ({default}) ")
            return user_input if user_input else default
        except KeyboardInterrupt:
            print("\nOperation is terminated.")
            sys.exit(0)

    def ask_yes_no_question(self, question: str) -> bool:
        question = [
            inquirer.List(
                'choice',
                message=question,
                choices=['Yes', 'No'],
                carousel=True  # Allows navigation through choices in a loop
            )
        ]
        answer = inquirer.prompt(question)
        return True if answer['choice'] == 'Yes' else False

    def get_user_input(self) -> None:
        print(f"""
This utility will walk you through creating a {self.meta_data_file_name} file.
It only covers the most common items and meta data of the project.
        """)
        print("Press ^C at any time to quit.")
        print("Press Enter to use the default value. \n")

        self.project_name = self.valided_user_input(
            "project name", self.project_name)
        self.version = self.valided_user_input("version", self.version)
        self.description = self.valided_user_input(
            "description", self.description)
        self.entry_point = self.valided_user_input(
            "entry point", self.entry_point)
        self.git_repository = self.valided_user_input(
            "git repository", self.git_repository)
        self.author = self.valided_user_input("author", self.author)
        self.license = self.valided_user_input("license", self.license)
        self.entry_point_path += self.entry_point

        print("\nAdd the packages you want to install in the project.")
        print("Enter the package name like (<package_name>==<version>) or (<package_name>) to install spacific version or latest version.")
        self.get_user_input_for_package()

        # Confirm and show details
        print(f"\nAbout to write to " + self.current_working_directory +
              "\\" + self.meta_data_file_name + ":")
        agree_to_create_ppm_toml: bool = self.ask_yes_no_question(
            "Is this ok?")
        if not agree_to_create_ppm_toml:
            print("\nOperation is terminated.")
            sys.exit(0)

    def create_env_file(self) -> None:
        self.agree_to_create_env_file: bool = self.ask_yes_no_question(
            f"Are you sure you want to add {self.environment_variable_name} file?")

        if self.agree_to_create_env_file:
            if os.path.isfile(self.environment_variable_name):
                override_env_file: bool = self.ask_yes_no_question(
                    f"{self.environment_variable_name} file already exists. Do you want to override it?")

                if override_env_file:
                    with open(self.environment_variable_name, "w") as file:
                        file.write("")
                    print(
                        f"\n{self.environment_variable_name} file is overwritten.\n")

                else:
                    print(
                        f"\n{self.environment_variable_name} file is untouched.\n")

            else:
                with open(self.environment_variable_name, "w") as file:
                    file.write("")
                print(f"\n{self.environment_variable_name} file is created.\n")

    def create_project_folder_files(self) -> None:
        if not os.path.exists("src"):
            os.makedirs("src")

        if os.path.exists("src/main.py"):
            agree_to_override_main_file: bool = self.ask_yes_no_question(
                "Do you want to override main.py file?")

            if not agree_to_override_main_file:
                print("\nmain.py file is untouched.\n")
                return

        self.start_animation("Creating src folder and main.py file")

        with open("src/main.py", "w") as file:
            file.write("""from dotenv import load_dotenv
import os
                    
load_dotenv()
                
# to use environment variables
# os.getenv('ENV_VARIABLE_NAME')
                
def main() -> None:
    print('Hello, World!')
                
if __name__ == '__main__':
    main()
""")
        self.stop_animation()
        print("\nsrc folder created. \n")

    def create_virtualenv(self) -> None:
        self.start_animation("Creating virtual environment")
        if not os.path.exists(self.virtual_environment_name):
            subprocess.run([sys.executable, "-m", "venv",
                            self.virtual_environment_name])
            self.stop_animation()
            print("\nVirtual environment created.\n")
        else:
            self.stop_animation()
            print("\nVirtual environment already exists.\n")

    def install_packages(self) -> None:
        self.start_animation("Installing packages")

        self.packages.append("python-dotenv")
        self.packages.append("pipdeptree")

        script: str = self.virtual_environment_activate_script + \
            " && pip install --no-cache-dir " + " ".join(self.packages)
        subprocess.run(
            script, shell=True, capture_output=True, text=True)

        self.stop_animation()
        print("\nAll packages installed.\n")

    def format_package_dependency(self, result: str) -> None:
        # Parse each package and its dependencies into my_dict
        for package in json.loads(result.stdout):
            package_name = f"{package['package']['package_name']}=={
                package['package']['installed_version']}"
            dependencies = [
                f"{dep['package_name']}=={dep['installed_version']}" for dep in package['dependencies']
            ]
            self.package_dependency[package_name] = dependencies

        # Function to recursively build nested structure
        def build_nested_structure(package_name):
            if package_name not in self.package_dependency:
                return []  # No dependencies for this package
            nested_dependencies = []
            for dep in self.package_dependency[package_name]:
                nested_dependencies.append({dep: build_nested_structure(dep)})
            return nested_dependencies

        # Build the final output with only top-level packages and nested dependencies
        nested_dict = {}
        for package_name in self.package_dependency:
            # Check if the package is a top-level parent (not a dependency of any other package)
            is_top_level = all(
                package_name not in deps for deps in self.package_dependency.values())
            if is_top_level:
                nested_dict[package_name] = build_nested_structure(
                    package_name)

        self.package_dependency = nested_dict

    def parse_installed_package_dependency(self) -> None:
        self.start_animation("Checking packages")
        script: str = self.virtual_environment_activate_script + \
            " && pipdeptree --json"
        result = subprocess.run(
            script, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            self.format_package_dependency(result)

        self.stop_animation()
        print("\nAll packages checked.\n")

    def format_dependencies(self) -> str:
        output = "[dependencies]\n"

        def process_package(package, dependencies, level=0):
            indent = "\t" * level
            output_lines = [f"{indent}{'-' if level > 0 else ''}{package}"]

            for dependency in dependencies:
                for dep_name, sub_deps in dependency.items():
                    output_lines.extend(process_package(
                        dep_name, sub_deps, level + 1))

            return output_lines

        for package, dependencies in self.package_dependency.items():
            output += "\n".join(process_package(package, dependencies)) + "\n"

        return output

    def create_ppm_toml(self) -> None:
        self.start_animation(f"Creating {self.meta_data_file_name} file")
        file_content: str = f"""[project]
name = "{self.project_name}"
version = "{self.version}"
description = "{self.description}"
entry_point = "{self.entry_point}"
git_repository = "{self.git_repository}"
author = "{self.author}"
license = "{self.license}"


[python]
python_version = "{self.python_version}"


[environment]
path = "{self.virtual_environment_activate_script}"


[environment_variables]"""
        if self.agree_to_create_env_file:
            file_content += """ path = "./env" """

        file_content += f"""\n\n
[command]
run = "python {self.entry_point_path}"


[dependencies]
"""
        formated_dependencies = self.format_dependencies()
        file_content += formated_dependencies

        with open(self.meta_data_file_name, "w") as file:
            file.write(file_content)

        self.stop_animation()

        print(f"\n" + self.current_working_directory +
              "\\" + self.meta_data_file_name + " created.")
        print("\nThis python project is built on python version",
              self.python_version)
        print("\nCongratulations! Your project is ready to go.")
        print("\nTo install the dependencies, use the command 'ppm install'")
        print("To run the project, use the command 'ppm run'")
        print("To activate the virtual environment, use the command 'ppm activate'")
        print("To deactivate the virtual environment, use the command 'ppm deactivate'")
        print(f"\nmain.py file is created in src folder ({
            self.entry_point_path}). You can start coding in main.py file.")
        print("\nHappy coding!")

    def init(self) -> None:
        self.get_user_input()
        self.create_env_file()
        self.create_project_folder_files()
        self.create_virtualenv()
        self.install_packages()
        self.parse_installed_package_dependency()
        self.create_ppm_toml()
