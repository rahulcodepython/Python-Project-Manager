import os
import sys


class Init():
    def __init__(self) -> None:
        self.current_working_directory: str = os.getcwd()
        self.current_folder_name: str = os.path.basename(
            self.current_working_directory)
        self.project_name = self.current_folder_name.lower()
        self.version = "1.0.0"
        self.description = ""
        self.entry_point = "main.py"
        self.git_repository = ""
        self.author = ""
        self.license = "ISC"
        self.agree_to_create_ppm_toml = "yes"

    def valided_user_input(self, prompt: str, default: str) -> str:
        try:
            user_input = input(f"{prompt} ({default}) ")
            return user_input if user_input else default
        except KeyboardInterrupt:
            print("\nOperation is terminated.")
            sys.exit(0)

    def get_user_input(self) -> None:
        print("""
This utility will walk you through creating a ppm.toml file.
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

        # Confirm and show details
        print(f"\nAbout to write to {
              self.current_working_directory}\\ppm.toml:")
        self.agree_to_create_ppm_toml = self.valided_user_input(
            "Is this ok?", self.agree_to_create_ppm_toml)

        print(self.agree_to_create_ppm_toml, self.project_name, self.version,
              self.description, self.entry_point, self.git_repository, self.author, self.license)

    def create_ppm_toml(self) -> None:
        with open("ppm.toml", "w") as file:
            file.write(f"""[project]
name = "{self.project_name}"
version = "{self.version}"
description = "{self.description}"
entry_point = "{self.entry_point}"
git_repository = "{self.git_repository}"
author = "{self.author}"
license = "{self.license}"


[dependencies]
""")
        print("ppm.toml created")

    def init(self) -> None:
        self.get_user_input()
        self.create_ppm_toml() if (self.agree_to_create_ppm_toml.lower(
        ) == "yes" or self.agree_to_create_ppm_toml.lower(
        ) == "y") else print("Operation is terminated.")
