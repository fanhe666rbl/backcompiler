class TypeError (Exception):
    left_type = ""
    right_type = ""
    pos = 0
    op = ""

    def __init__(self, left_type, right_type, pos, op):
        self.left_type = left_type
        self.right_type = right_type
        self.pos = pos
        self.op = op

    def __str__(self):
        return "type error: " + self.left_type + " " + self.op + " " + self.right_type + " at " + str(self.pos)
