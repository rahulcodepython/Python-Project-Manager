import subprocess
import sys
import threading
import time
import json
import platform
import os


class Install():
    def __init__(self):
        self.packages: list[str] = []
        self.package_dependency: dict = {}
        self.meta_data_file_name: str = "ppm.toml"
        self.virtual_environment_name: str = ".venv"
        self.virtual_environment_activate_path = os.path.join(
            self.virtual_environment_name, "Scripts", "activate") if os.name == "nt" else os.path.join(self.virtual_environment_name, "bin", "activate")
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

    def check_ppm_toml_file(self) -> None:
        if not os.path.exists(self.meta_data_file_name):
            print(
                f"{self.meta_data_file_name} file not found. Please run 'ppm init' command to create {self.meta_data_file_name} file.")
            sys.exit(0)

    def take_package_name(self):
        print("Install packages in the project.")
        print("Press ^C at any time to quit.")
        print("\nAdd the packages you want to install in the project.")
        print("Enter the package name like (<package_name>==<version>) or (<package_name>) to install spacific version or latest version.")

        while True:
            package_name: str = input(
                "Enter package name to install (press Enter to end): ")
            if package_name:
                self.packages.append(package_name)
            else:
                break

        print("\n")

    def build_script(self, script: list[str]) -> str:
        if platform.system() == "Windows":
            return f"{self.virtual_environment_activate_path} && " + " && ".join(script)
        else:
            shell = os.getenv("SHELL", "/bin/bash")
            if "zsh" in shell:
                return f"zsh -c 'source {self.virtual_environment_activate_path} && " + " && ".join(script) + "'"
            else:
                return f"bash -c 'source {self.virtual_environment_activate_path} && " + " && ".join(script) + "'"

    def install_packages(self) -> None:
        self.start_animation("Installing packages")

        script: str = self.build_script(
            ["pip install --no-cache-dir " + " ".join(self.packages)])
        result = subprocess.run(
            script, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            print("An error occurred while checking packages. Please try again.")
            print(f"Error message is {result.stderr}")
            sys.exit(0)

        self.stop_animation()
        print("\nAll packages installed.\n")

    def format_package_dependency(self, result: str) -> None:
        for package in json.loads(result.stdout):
            package_name = f"{package['package']['package_name']}=={
                package['package']['installed_version']}"
            dependencies = [
                f"{dep['package_name']}=={dep['installed_version']}" for dep in package['dependencies']
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
                package_name not in deps for deps in self.package_dependency.values())
            if is_top_level:
                nested_dict[package_name] = build_nested_structure(
                    package_name)

        self.package_dependency = nested_dict

    def parse_installed_package_dependency(self) -> None:
        self.start_animation("Checking packages")
        script: str = self.build_script(["pipdeptree --json"])
        result = subprocess.run(
            script, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            self.format_package_dependency(result)
        else:
            print("An error occurred while checking packages. Please try again.")
            print(f"Error message is {result.stderr}")
            sys.exit(0)

        self.stop_animation()
        print("\nAll packages checked.\n")

    def format_dependencies(self) -> str:
        output = ""

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

    def overwrite_ppm_toml(self) -> None:
        self.start_animation(f"Overwritting {self.meta_data_file_name} file")

        formated_dependencies = self.format_dependencies()

        with open(self.meta_data_file_name, 'r') as file:
            lines = file.readlines()

        try:
            char_index = lines.index('[dependencies]\n') + 1
        except ValueError:
            ...
        else:
            lines = lines[:char_index] + [formated_dependencies]

            with open(self.meta_data_file_name, 'w') as file:
                file.writelines(lines)

        self.stop_animation()

        print(f"\n{self.meta_data_file_name} file is overwritten.\n")

    def install(self):
        self.check_ppm_toml_file()
        self.take_package_name()
        self.install_packages()
        self.parse_installed_package_dependency()
        self.overwrite_ppm_toml()
