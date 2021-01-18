class ExpectedTokenError(Exception):
    expect_type = ""
    get_type = ""
    pos = 0

    def __init__(self, expect_type, get_type, pos):
        self.expect_type = expect_type
        self.get_type = get_type
        self.pos = pos

    def __str__(self):
        return "expect: " + self.expect_type + " at " + str(self.pos) + " but get:" + self.get_type
