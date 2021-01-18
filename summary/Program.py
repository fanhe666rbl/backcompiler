from summary.Function import Function
from summary.Global import Global


class Program:
    magic = [0x72, 0x30, 0x3b, 0x3e]
    version = [0x00, 0x00, 0x00, 0x01]
    Global = []
    Function = []

    def __init__(self):
        return

    def add_function(self, func: Function):
        self.Function.append(func)
        return

    def add_global(self, glob: Global):
        self.Global.append(glob)
        return

    def find_function(self, name):
        for func in self.Function:
            if func.name == name:
                return func
        return None

