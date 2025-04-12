from .manager import Manager


class Update:
    def __init__(self):
        self.manager = Manager()

    def update(self, packages):
        self.manager.check_file_existence()

        if packages is None:
            self.manager.parse_outdated_packages()
        else:
            self.manager.packages = packages

        self.manager.install_packages()
        self.manager.get_pip_packages()
        self.manager.create_write_configuration_file()
