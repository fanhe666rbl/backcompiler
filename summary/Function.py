class Function:
    name = ""
    return_type = ""
    is_return = False
    param_num = 0
    params = []
    body_size = 0
    instructions = []

    def __init__(self, name, return_type):
        self.name = name
        self.return_type = return_type
        if return_type != "VOID":
            self.is_return = True
        return

    def add_instructions(self, instruction):
        self.instructions.append(instruction)
        return

    def set_params(self, params: list):
        self.params = params
        self.param_num = len(self.params)
        return

