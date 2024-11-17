from .default import PPM_Default
import sys, re


class Uninstall:
    def __init__(self):
        self.ppm = PPM_Default()

    def check_configuration_file_file(self) -> None:
        if not self.ppm.configuration_file_exists:
            print(
                f"{self.ppm.meta_data_file_name} file not found. Please run 'ppm init' command to create {self.ppm.meta_data_file_name} file."
            )
            sys.exit(0)

    def parse_preinstalled_packages(self) -> None:
        text = ""

        with open(self.ppm.meta_data_file_name, "r") as file:
            contents = file.readlines()
            char_index = contents.index("[dependencies]\n") + 1

            text = "".join(contents[char_index:])

        pattern = r"-?([a-zA-Z0-9\-_]+==[0-9\.]+)"
        self.ppm.packages = [match.lstrip("-") for match in re.findall(pattern, text)]

    def uninstall(self, *args) -> None:
        self.check_configuration_file_file()
        if len(args[0]) == 0:
            self.parse_preinstalled_packages()
        else:
            self.ppm.packages = args[0]
        self.ppm.uninstall_packages()
        if len(args[0]) == 0:
            self.ppm.overwrite_configuration_file_remove_dependencies()
        else:
            self.ppm.overwrite_configuration_file()
        self.ppm.parse_installed_package_dependency(show_print_statement=False)
        self.ppm.overwrite_configuration_file(show_print_statement=False)
