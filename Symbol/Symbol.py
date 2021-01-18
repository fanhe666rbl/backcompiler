class Symbol:
    name = ""
    v_type = ""
    # re_type = ""
    is_initialization = False
    is_constant = False
    is_global = False
    is_param = False
    layer = 0
    stack_offset = 0

    def __init__(self, name, v_type, is_initialization,
                 is_constant):
        self.name = name
        self.v_type = v_type
        # self.re_type = re_type
        self.is_initialization = is_initialization
        self.is_constant = is_constant
        return

    def __str__(self):
        return self.name + " " + self.v_type + " " + str(self.layer) + " " + str(self.is_global) + " " + str(self.stack_offset)

    def set_global(self, layer):
        self.layer = layer
        if layer == 0:
            self.is_global = True

    def set_param(self, is_param):
        self.is_param = is_param
        return

