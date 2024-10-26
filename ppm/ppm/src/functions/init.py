import os
import sys
import subprocess
import time
import re


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
        self.agree_to_create_env_file: str = "yes"
        self.python_version: str = sys.version.split(" ")[0]
        self.meta_data_file_name: str = "ppm.toml"
        self.virtual_environment_name: str = ".venv"
        self.environment_variable_name: str = ".env"
        self.virtual_environment_activate_script = os.path.join(
            self.virtual_environment_name, "Scripts", "activate") if os.name == "nt" else os.path.join(self.virtual_environment_name, "bin", "activate")
        self.packages: list[str] = ['django', 'requests']
        self.package_dependency: dict = {}

    def parse_package_name(self) -> None:
        for index, package_name in enumerate(self.packages):
            if '@' in package_name:
                name, version = package_name.split('@', 1)
                if version.lower() != "latest":
                    self.packages[index] = f"{name}=={version}"
                else:
                    self.packages[index] = name
            else:
                self.packages[index] = package_name

    def remove_version_from_package_name(self, package_name) -> str:
        for i in range(len(package_name)):
            if package_name[i] == '<' or package_name[i] == '=' or package_name[i] == '>':
                return package_name[:i]
        return package_name

    def parse_dependencies_stdout_and_prepare_package_dependency_dictionary(self, output):
        package_dependency: dict = {}
        main_package = re.compile(
            r'^Collecting (\S+)(==[\d.]+)?')
        dependency_re = re.compile(
            r'^Collecting (\S+)(==[\d.]+)? \(from (\S+)\)')

        final_version_list: list[str] = output.splitlines()[-1].split(' ')[2:]
        unparsed_parent_package_list: dict = {}

        for line in output.splitlines():
            if main_package.match(line) and not dependency_re.match(line):
                line_list = line.split(' ')
                name = line_list[-1].replace('(', '').replace(')', '')
                for final_name in final_version_list:
                    parsed_final_name: str = final_name.rsplit('-', 1)[0]
                    version: str = final_name.rsplit('-', 1)[1]
                    if name in parsed_final_name.lower():
                        key_name = f"{parsed_final_name}@{version}"
                        unparsed_parent_package_list[parsed_final_name.lower(
                        )] = key_name
                        package_dependency[key_name] = []
                        break

            elif dependency_re.match(line):
                line_list = line.split(' ')
                parent_package = line_list[-1].replace(
                    '(', '').replace(')', '')
                package_name = self.remove_version_from_package_name(
                    line_list[1])
                if parent_package in unparsed_parent_package_list.keys():
                    for final_name in final_version_list:
                        parsed_final_name: str = final_name.rsplit('-', 1)[0]
                        version: str = final_name.rsplit('-', 1)[1]
                        if package_name in parsed_final_name.lower():
                            package_dependency[unparsed_parent_package_list[parent_package]].append(
                                f"{parsed_final_name}@{version}")

        self.package_dependency.update(package_dependency)

    def check_dependencies(self, dry_run_script) -> None:
        print("Checking dependencies...\n")
        checking_dependencies_stdout_result = subprocess.run(
            dry_run_script, shell=True, capture_output=True, text=True)
        self.parse_dependencies_stdout_and_prepare_package_dependency_dictionary(
            checking_dependencies_stdout_result.stdout) if checking_dependencies_stdout_result.returncode == 0 else print("Failed to retrieve dependencies. Check for errors.")

    def install_packages(self, script) -> None:
        print("Installing packages...\n")
        subprocess.run(
            script, shell=True, capture_output=True, text=True)
        print("All packages installed.\n")

    def check_dependencies_and_install_packages(self) -> None:
        self.parse_package_name()

        dry_run_script: str = self.virtual_environment_activate_script + \
            " && pip install --no-cache-dir --dry-run " + \
            "python-dotenv " + " ".join(self.packages)
        script: str = self.virtual_environment_activate_script + \
            " && pip install --no-cache-dir " + \
            "python-dotenv " + " ".join(self.packages)

        self.check_dependencies(dry_run_script)

        self.install_packages(script)

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
        print("Enter the package name like (<package_name>@<version>) or (<package_name>@latest) to install spacific version or latest version.")
        self.get_user_input_for_package()

        # Confirm and show details
        print(f"\nAbout to write to {
              self.current_working_directory}\\{self.meta_data_file_name}:")
        agree_to_create_ppm_toml = self.valided_user_input(
            "Is this ok?", "yes")
        if agree_to_create_ppm_toml.lower() != "yes" and agree_to_create_ppm_toml.lower() != "y":
            print("\nOperation is terminated.")
            sys.exit(0)

    def create_env_file(self) -> None:
        self.agree_to_create_env_file = self.valided_user_input(
            f"Are you sure you want to add {self.environment_variable_name} file?", self.agree_to_create_env_file)

        if self.agree_to_create_env_file.lower() == "yes" or self.agree_to_create_env_file.lower() == "y":
            self.agree_to_create_env_file = "y"

            if os.path.isfile(self.environment_variable_name):
                override_env_file = self.valided_user_input(
                    f"{self.environment_variable_name} file already exists. Do you want to override it?", "no")

                if override_env_file.lower() == "yes" or override_env_file.lower() == "y":
                    with open(self.environment_variable_name, "w") as file:
                        file.write("")
                    print(
                        f"\n{self.environment_variable_name} file is overwritten.")

                else:
                    print(
                        f"\n{self.environment_variable_name} file is untouched.")

            else:
                with open(self.environment_variable_name, "w") as file:
                    file.write("")
                print(f"\n{self.environment_variable_name} file is created.")

    def create_project_folder_files(self) -> None:
        if not os.path.exists("src"):
            os.makedirs("src")
        else:
            print("\nsrc folder already exists.")

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
        print("\nsrc folder created.")

    def create_virtualenv(self) -> None:
        if not os.path.exists(self.virtual_environment_name):
            print("\nCreating virtual environment...")
            subprocess.run([sys.executable, "-m", "venv",
                           self.virtual_environment_name])
            print("\nVirtual environment created.\n")
        else:
            print("\nVirtual environment already exists.\n")

    def create_ppm_toml(self) -> None:
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
        if self.agree_to_create_env_file == "y":
            file_content += """ path = "./env" """

        file_content += f"""\n\n
[command]
run = "python {self.entry_point_path}"


[dependencies]
"""
        for key, value in self.package_dependency.items():
            file_content += f"{key}\n"
            for item in value:
                file_content += f"\t- {item}\n"

        with open(self.meta_data_file_name, "w") as file:
            file.write(file_content)

        print(f"\n{self.current_working_directory}\\{
            self.meta_data_file_name} created.")
        print("This python project is built on python version", self.python_version)
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
        self.check_dependencies_and_install_packages()
        self.create_ppm_toml()
