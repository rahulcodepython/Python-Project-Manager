import os
import sys


class Init():
    def __init__(self) -> None:
        self.current_working_directory: str = os.getcwd()
        self.current_folder_name: str = os.path.basename(
            self.current_working_directory)
        self.entry_point_path = f"./src/"
        self.project_name = self.current_folder_name.lower()
        self.version = "1.0.0"
        self.description = ""
        self.entry_point = "main.py"
        self.git_repository = ""
        self.author = ""
        self.license = "ISC"
        self.agree_to_create_ppm_toml = "yes"
        self.python_version = sys.version.split(" ")[0]
        self.virtual_environment_path = "./venv/Scripts/activate"
        self.meta_data_file_name = "ppm.toml"

    def valided_user_input(self, prompt: str, default: str) -> str:
        try:
            user_input = input(f"{prompt} ({default}) ")
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

        # Confirm and show details
        print(f"\nAbout to write to {
              self.current_working_directory}\\{self.meta_data_file_name}:")
        self.agree_to_create_ppm_toml = self.valided_user_input(
            "Is this ok?", self.agree_to_create_ppm_toml)

    def create_ppm_toml(self) -> None:
        with open(self.meta_data_file_name, "w") as file:
            file.write(f"""[project]
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
path = "{self.virtual_environment_path}"


[environment_variables]
path = "./env"


[command]
run = "python {self.entry_point_path}"


[dependencies]
""")
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

    def create_env_file(self) -> None:
        with open(".env", "w") as file:
            file.write("")

    def create_project_folder_files(self) -> None:
        if not os.path.exists("src"):
            os.makedirs("src")

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

    def init(self) -> None:
        self.get_user_input()

        if (self.agree_to_create_ppm_toml.lower() == "yes" or self.agree_to_create_ppm_toml.lower() == "y"):
            self.create_env_file()
            self.create_project_folder_files()
            self.create_ppm_toml()
