from .default import PPM_Default
from .decorators import operation_termination


class Init:
    def __init__(self) -> None:
        self.ppm = PPM_Default()

    def identify_ppm_usage(self) -> None:
        self.ppm.usage_of_ppm = self.ppm.ask_choice_question(
            "How do you want to use ppm?",
            ["as a project manager", "as a dependency manager"],
        )

    def configure_project_by_user_input(self) -> None:
        print(
            f"""
This utility will walk you through creating a {self.ppm.meta_data_file_name} file.
It only covers the most common items and meta data of the project.
        """
        )
        print("Press ^C at any time to quit.")
        print("Press Enter to use the default value. \n")

        if self.ppm.usage_of_ppm == "as a project manager":
            self.ppm.project_name = self.ppm.valided_user_input(
                "project name", self.ppm.project_name
            )
            self.ppm.version = self.ppm.valided_user_input("version", self.ppm.version)
            self.ppm.description = self.ppm.valided_user_input(
                "description", self.ppm.description
            )
            self.ppm.entry_point = self.ppm.valided_user_input(
                "entry point", self.ppm.entry_point
            )
            self.ppm.author = self.ppm.valided_user_input("author", self.ppm.author)
            self.ppm.license = self.ppm.valided_user_input("license", self.ppm.license)

            print("")
            github_conf = self.ppm.ask_choice_question(
                "Do you want to add github configuration?",
                ["Yes", "No"],
            )
            if github_conf == "Yes":
                self.ppm.git_init = True
                self.ppm.git_repository = self.ppm.valided_user_input(
                    "github repository name", self.ppm.git_repository
                )

        self.ppm.get_package_name_for_installation()

    def console_write_instructions(self) -> None:
        self.ppm.animation.stop()
        print(
            f"\n{self.ppm.project_name} project is created in {self.ppm.current_working_directory}.\n"
        )
        print(
            "This python project is built on python version",
            self.ppm.python_version,
            ".\n",
        )
        print("Congratulations! Your project is ready to go.\n")
        print("To install the dependencies, use the command 'ppm install'\n")
        print("To uninstall the dependencies, use the command 'ppm uninstall'\n")

        if self.ppm.usage_of_ppm == "as a project manager":
            print("To run the project, use the command 'ppm run'\n")
            print(
                f"main.py file is created in src folder ({ self.ppm.entry_point_path}). You can start coding in main.py file.\n"
            )
        else:
            print(
                f"To run the project, you have to first add script manually in {self.ppm.meta_data_file_name} file and then use the command 'ppm run'\n"
            )

        print("Happy coding!")

    @operation_termination
    def init(self, select_default_values=None) -> None:
        self.identify_ppm_usage()
        (
            self.configure_project_by_user_input()
            if not select_default_values
            else print("Default values are selected.\n")
        )
        self.ppm.create_env_file()
        (
            self.ppm.create_project_folder_files()
            if self.ppm.usage_of_ppm == "as a project manager"
            else None
        )
        self.ppm.animation.start("Configuring project")
        self.ppm.create_virtualenv()
        (
            self.ppm.packages.append("python-dotenv")
            if self.ppm.agree_to_create_env_file
            else None
        )
        self.ppm.install_packages()
        self.ppm.parse_installed_package_dependency()
        self.ppm.git_initiate()
        self.ppm.create_configuration_file()
        self.console_write_instructions()


# ppm run
