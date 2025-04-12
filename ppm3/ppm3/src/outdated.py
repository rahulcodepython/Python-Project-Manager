from .manager import Manager


class Outdated:
    def __init__(self):
        self.manager = Manager()

    def outdated(self):
        self.manager.check_file_existence()
        self.manager.show_outdated_packages()
