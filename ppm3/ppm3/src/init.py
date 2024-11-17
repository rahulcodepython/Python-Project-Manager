from .default import PPM_Default


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
            self.ppm.git_repository = self.ppm.valided_user_input(
                "git repository", self.ppm.git_repository
            )
            self.ppm.author = self.ppm.valided_user_input("author", self.ppm.author)
            self.ppm.license = self.ppm.valided_user_input("license", self.ppm.license)

        self.ppm.get_package_name_for_installation()

    def init(self, select_default_values=None) -> None:
        self.identify_ppm_usage()
        self.configure_project_by_user_input() if not select_default_values else None
        print("Default values are selected.\n")
        self.ppm.create_env_file()
        self.ppm.create_project_folder_files()
        self.ppm.create_virtualenv(True)
        self.ppm.packages.append("python-dotenv")
        self.ppm.install_packages(True)
        self.ppm.parse_installed_package_dependency(True)
        self.ppm.create_configuration_file()
        self.ppm.console_write_instructions()
