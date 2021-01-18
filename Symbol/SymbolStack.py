from Symbol.Symbol import Symbol
from Symbol.SymbolType import SymbolType


class SymbolStack:
    SymbolStack = []
    layer = 0

    def __init__(self):
        # self.insert_symbol()
        return

    def __str__(self):
        print("--------------------")
        for symbol in self.SymbolStack:
            print(symbol)
        print("--------------------")
        return "stack\n"

    def insert_symbol(self, symbol):
        # if self.layer == 0:
        #     is_global = True
        # else:
        #     is_global = False
        # symbol = Symbol(name, v_type, re_type, is_initialization,
        #                 is_constant, is_global, self.layer)
        symbol.set_global(self.layer)
        symbol.stack_offset = self.get_offset(symbol)
        self.SymbolStack.append(symbol)
        return

    def push_layer(self):
        self.layer += 1
        return

    def pop_layer(self):

        # print("--------------")
        print(self.layer)
        while len(self.SymbolStack) > 0 and self.SymbolStack[-1].layer == self.layer:
            # print(self.SymbolStack.pop())
            self.SymbolStack.pop()
        # print("--------------")
        self.layer -= 1
        return

    def find_symbol(self, name):
        i = len(self.SymbolStack) - 1
        while i >= 0:
            if self.SymbolStack[i].name == name:
                return self.SymbolStack[i]
            i -= 1
        return None

    def get_offset(self, symbol: Symbol):
        offset = 0
        if symbol.v_type == SymbolType['FN_KW']:
            i = len(self.SymbolStack) - 1
            while i >= 0:
                s: Symbol = self.SymbolStack[i]
                if s.v_type == SymbolType['FN_KW']:
                    offset += 1
                i -= 1
            return offset

        i = len(self.SymbolStack) - 1
        while i >= 0:
            s = self.SymbolStack[i]
            if s.v_type != SymbolType['FN_KW'] and\
                    s.is_global == symbol.is_global and\
                    s.is_param == symbol.is_param:
                # 同级偏移加一
                offset += 1
            i -= 1
        return offset
