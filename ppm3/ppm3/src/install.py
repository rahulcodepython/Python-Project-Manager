from .default import PPM_Default
import sys, re


class Install:
    def __init__(self):
        self.ppm = PPM_Default()

    def parse_preinstalled_packages(self) -> None:
        text = ""

        with open(self.ppm.meta_data_file_name, "r") as file:
            contents = file.readlines()
            char_index = contents.index("[dependencies]\n") + 1

            text = "".join(contents[char_index:])

        pattern = r"-?([a-zA-Z0-9\-_]+==[0-9\.]+)"
        self.ppm.packages = [match.lstrip("-") for match in re.findall(pattern, text)]

    def install(self, *args) -> None:
        self.ppm.animation.start("Installing packages")
        self.ppm.check_configuration_file_file()
        if len(args[0]) == 0:
            self.parse_preinstalled_packages()
        else:
            self.ppm.packages = args[0]
        self.ppm.create_virtualenv()
        self.ppm.install_packages()
        self.ppm.parse_installed_package_dependency()
        self.ppm.overwrite_configuration_file()
        self.ppm.animation.stop("Packages installed successfully")
