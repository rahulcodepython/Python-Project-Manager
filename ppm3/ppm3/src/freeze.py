from .decorators import operation_termination
from .manager import Manager


class Freeze:
    def __init__(self):
        self.manager = Manager()

    @operation_termination
    def freeze(self):
        self.manager.check_file_existence()
        self.manager.create_virtualenv()
        self.manager.freeze_requirements()
