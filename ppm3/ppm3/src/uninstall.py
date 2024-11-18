from .default import PPM_Default
import sys, re, subprocess


class Uninstall:
    def __init__(self):
        self.ppm = PPM_Default()

    def check_configuration_file_file(self) -> None:
        if not self.ppm.configuration_file_exists:
            self.ppm.animation.stop()
            print(
                f"{self.ppm.meta_data_file_name} file not found. Please run 'ppm init' command to create {self.ppm.meta_data_file_name} file."
            )
            sys.exit(0)

    def parse_preinstalled_packages(self) -> None:
        package_name = "pipdeptree"

        result = subprocess.run(
            ["pipdeptree", "-p", package_name, "--warn", "silence"],
            capture_output=True,
            text=True,
        )

        exclude_packages = set()
        for line in result.stdout.splitlines():
            if " - " in line:
                dep = line.split("==")[0].strip(" -")
                exclude_packages.add(dep.split(" ")[0])
        exclude_packages.add(package_name)

        result = subprocess.run(["pip", "freeze"], capture_output=True, text=True)
        all_packages = set(line.split("==")[0] for line in result.stdout.splitlines())
        self.ppm.packages = list(all_packages - exclude_packages)

    def parse_package_dependency_tree(self, packages_name) -> None:
        dependencies = set()

        for package_name in packages_name:
            result = subprocess.run(
                ["pipdeptree", "-p", package_name, "--warn", "silence"],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            for line in result.stdout.splitlines():
                if ("installed") in line:
                    dependencies.add(line.split(" ")[1])
            dependencies.add(package_name)

        self.ppm.packages = list(dependencies)

    def uninstall(self, with_dependencies, *args) -> None:
        self.ppm.animation.start("Uninstalling packages")
        self.check_configuration_file_file()
        if len(args[0]) == 0:
            self.parse_preinstalled_packages()
        else:
            if with_dependencies:
                self.parse_package_dependency_tree(args[0])
            else:
                self.ppm.packages = args[0]
        self.ppm.uninstall_packages()
        if len(args[0]) == 0:
            self.ppm.overwrite_configuration_file_remove_dependencies()
        else:
            self.ppm.overwrite_configuration_file()
        self.ppm.parse_installed_package_dependency()
        self.ppm.overwrite_configuration_file()
        self.ppm.animation.stop("Packages uninstalled successfully")
