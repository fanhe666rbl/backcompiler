# import sys
# import os
# sys.path.append(os.path.dirname(sys.path[0]))

from tokenizer.Token import Tokenizer
from tokenizer.TokenType import TokenType
from error.ExpectedTokenError import ExpectedTokenError
from error.TypeError import TypeError
from error.NoDefineError import NoDefineError
from Symbol.Symbol import Symbol
from Symbol.SymbolStack import SymbolStack
from Symbol.SymbolType import SymbolType
from summary.Program import Program
from summary.Function import Function


class Analyser:
    tokenizer = Tokenizer
    instructions = []
    symbolStack = SymbolStack

    program = Program()

    # 偷看的token
    peekedToken = None
    is_debug = False

    def __init__(self, tokenizer, is_debug):
        self.tokenizer = tokenizer
        self.is_debug = is_debug
        self.symbolStack = SymbolStack()

    def peek(self):
        if not self.peekedToken:
            self.peekedToken = self.tokenizer.next_token()
        return self.peekedToken

    def next(self):
        if self.peekedToken:
            token = self.peekedToken
            self.peekedToken = None
            return token
        else:
            return self.tokenizer.next_token()

    def check(self, t_type):
        token = self.peek()
        if not token:
            return False
        return token.type == t_type

    def next_if(self, t_type):
        token = self.peek()
        if token:
            if token.type == t_type:
                return self.next()
            else:
                return None
        else:
            return None

    def expect(self, t_type):
        token = self.peek()
        if token:
            if token.type == t_type:
                return self.next()
            else:
                e = ExpectedTokenError(t_type, token.type, token.lexpos)
                raise e
        else:
            e = ExpectedTokenError(t_type, "None", -1)
            raise e

    def check_type(self, left_type, right_type, pos, op):
        # print(left_type, right_type, pos, op)
        if left_type == "None" or right_type == "None":
            e = TypeError(left_type, right_type, pos, op)
            raise e
        if left_type == right_type:
            return
        else:
            e = TypeError(left_type, right_type, pos, op)
            raise e

    def analyse(self):
        self.analyse_program()
        return self.instructions

    def analyse_program(self):
        # self.symbolStack
        func = Function("_start", "VOID")
        self.program.add_function(func)

        while not self.check(TokenType['EOF']):
            if self.check(TokenType['let']) or self.check(TokenType['const']):
                self.analyse_decl_stmt()
            elif self.check(TokenType['fn']):
                self.analyse_function()
            else:
                break

        self.expect(TokenType['EOF'])
        print(self.symbolStack)
        if self.is_debug:
            print("finish program")
        return

    def analyse_function(self):
        v_type = self.expect(TokenType['fn']).type
        ident = self.expect(TokenType['ID'])
        # 符号表加入 先加入符号表，1.递归调用 2.全局变量
        symbol = Symbol(ident.value, SymbolType[v_type], is_initialization=True,
                        is_constant=True)
        self.symbolStack.insert_symbol(symbol)

        self.expect(TokenType['('])
        self.symbolStack.push_layer()
        # 获取参数
        params = self.analyse_param_list()
        # 设置is_param
        for param in params:
            param.set_param(True)

        self.expect(TokenType[')'])
        self.expect(TokenType['->'])
        re_t = self.expect(TokenType['type'])
        # 这里的返回值加到函数的性质里，之后在函数中查
        re_type = SymbolType[TokenType[re_t.value]]

        func = Function(ident.value, re_type)
        func.set_params(params)

        self.program.add_function(func)
        # print(v_type)

        self.analyse_block_stmt()
        self.symbolStack.pop_layer()
        if self.is_debug:
            print("finish function")
        return

    def analyse_param_list(self):
        params = []
        while not self.check(TokenType[')']):
            params.append(self.analyse_param())
            if not self.check(TokenType[',']):
                break
            self.expect(TokenType[','])

        if self.is_debug:
            print("finish param list")
        return params

    def analyse_param(self):
        is_const = False
        if self.next_if(TokenType['const']):
            is_const = True
        ident = self.expect(TokenType['ID'])
        self.expect(TokenType[':'])
        v_t = self.expect(TokenType['type'])

        v_type = SymbolType[TokenType[v_t.value]]
        symbol = Symbol(ident.value, v_type, is_initialization=True, is_constant=False)
        self.symbolStack.insert_symbol(symbol)

        if self.is_debug:
            print("finish param")
        return symbol

    def analyse_block_stmt(self):
        self.expect(TokenType['{'])
        while not self.check(TokenType['}']):
            self.analyse_stmt()
        self.expect(TokenType['}'])
        if self.is_debug:
            print("finish block stmt")
        return

    def analyse_stmt(self):
        if self.check(TokenType['let']) or self.check(TokenType['const']):
            self.analyse_decl_stmt()
        elif self.check(TokenType['if']):
            self.analyse_if_stmt()
        elif self.check(TokenType['while']):
            self.analyse_while_stmt()
        elif self.check(TokenType['return']):
            self.analyse_return_stmt()
        elif self.check(TokenType['{']):
            self.symbolStack.push_layer()
            self.analyse_block_stmt()
            self.symbolStack.pop_layer()
        elif self.check(TokenType[';']):
            self.next()
        # elif self.check(TokenType['break']):
        #     self.analyse_break()
        # elif self.check(TokenType['continue']):
        #     self.analyse_continue()
        elif self.check(TokenType['}']):
            return
        else:
            self.analyse_expr_stmt()

        # if self.is_debug:
        #     print("finish stmt")
        return

    def analyse_decl_stmt(self):
        if self.check(TokenType['const']):
            symbol = self.analyse_const_decl_stmt()
        elif self.check(TokenType['let']):
            symbol = self.analyse_let_decl_stmt()

        if self.is_debug:
            print("finish decl stmt")
        return symbol

    def analyse_const_decl_stmt(self):
        self.expect(TokenType['const'])
        ident = self.expect(TokenType['ID'])
        self.expect(TokenType[':'])
        v_t = self.expect(TokenType['type'])
        self.expect(TokenType['='])
        self.analyse_expr()
        self.expect(TokenType[';'])

        v_type = SymbolType[TokenType[v_t.value]]

        symbol = Symbol(ident.value, v_type, is_initialization=True, is_constant=True)
        self.symbolStack.insert_symbol(symbol)
        if self.is_debug:
            print("finish const decl stmt")
        return symbol

    def analyse_let_decl_stmt(self):
        self.expect(TokenType['let'])
        ident = self.expect(TokenType['ID'])
        self.expect(TokenType[':'])
        v_t = self.expect(TokenType['type'])
        if self.check(TokenType['=']):
            self.expect(TokenType['='])
            self.analyse_expr()
        self.expect(TokenType[';'])

        v_type = SymbolType[TokenType[v_t.value]]

        symbol = Symbol(ident.value, v_type, is_initialization=True, is_constant=True)
        self.symbolStack.insert_symbol(symbol)
        if self.is_debug:
            print("finish let decl stmt")
        return symbol

    def analyse_if_stmt(self):
        self.expect(TokenType['if'])
        self.analyse_expr()
        self.symbolStack.push_layer()
        # print(self.symbolStack.layer)
        self.analyse_block_stmt()
        self.symbolStack.pop_layer()
        if self.check(TokenType['else']):
            if self.check(TokenType['{']):
                self.symbolStack.push_layer()
                self.analyse_block_stmt()
                self.symbolStack.pop_layer()
            elif self.check(TokenType['if']):
                self.analyse_if_stmt()

        if self.is_debug:
            print("finish if stmt")
        return

    def analyse_while_stmt(self):
        self.expect(TokenType['while'])
        self.analyse_expr()
        self.symbolStack.push_layer()
        self.analyse_block_stmt()
        self.symbolStack.pop_layer()

        if self.is_debug:
            print("finish while stmt")
        return

    def analyse_return_stmt(self):
        self.expect(TokenType['return'])
        if not self.check(TokenType[';']):
            self.analyse_expr()
        self.expect(TokenType[';'])

        if self.is_debug:
            print("finish return stmt")
        return

    def analyse_expr_stmt(self):
        self.analyse_expr()
        self.expect(TokenType[';'])

        if self.is_debug:
            print("finish expr stmt")
        return

    # superE->nE|nE>nE
    # nE->T{+-T}
    # T->F{*/F}
    # F->-nE|(nE)|id|num
    #     F as->F as ty,id(->fn(param),id=->id=sE

    # 每个函数的最后要放入操作符
    def analyse_expr(self):
        left_type = self.analyse_narrow_expr()
        if self.check(TokenType['>']) or \
                self.check(TokenType['>=']) or \
                self.check(TokenType['<']) or \
                self.check(TokenType['<=']) or \
                self.check(TokenType['==']) or \
                self.check(TokenType['!=']):
            op = self.next()
            # print(op)
            right_type = self.analyse_expr()
            self.check_type(left_type, right_type, op.lexpos, op.value)
        # if self.is_debug:
        #     print("finish expr")
        return left_type

    def analyse_narrow_expr(self):
        left_type = self.analyse_item()
        while self.check(TokenType['+']) or self.check(TokenType['-']):
            op = self.next()
            right_type = self.analyse_item()
            self.check_type(left_type, right_type, op.lexpos, op.value)
            # left_type = right_type
        return left_type

    def analyse_item(self):
        left_type = self.analyse_factor()
        while self.check(TokenType['*']) or self.check(TokenType['/']):
            op = self.next()
            right_type = self.analyse_factor()
            self.check_type(left_type, right_type, op.lexpos, op.value)
        return left_type

    # 放入操作数
    def analyse_factor(self):

        v_type = ""
        if self.check(TokenType['-']):
            sign = self.next()
            v_type = self.analyse_narrow_expr()
        elif self.check(TokenType['(']):
            self.expect(TokenType['('])
            v_type = self.analyse_narrow_expr()
            self.expect(TokenType[')'])

        elif self.check(TokenType['ID']):
            v_type = self.push_ident()

        elif self.check(TokenType['int']) or self.check(TokenType['double']):
            num = self.next()
            v_type = SymbolType[num.type]
        elif self.check(TokenType['string']):
            string = self.next()
            v_type = SymbolType[string.type]

        if self.check(TokenType['as']):
            self.expect(TokenType['as'])
            t = self.expect(TokenType['type'])
            # print(t)
            v_type = SymbolType[TokenType[t.value]]
        return v_type

    # 将调用的参数压栈
    def analyse_call_param_list(self):
        self.analyse_expr()
        while self.check(TokenType[',']):
            self.next()
            self.analyse_expr()

    # 处理关于ident的情况：
    # 函数（：压入参数，然后call（预留返回值位置）
    # 赋值=：如果是const，报错，如果不是，将变量压栈，值store
    # 普通值压栈
    def push_ident(self):
        t = self.next()
        # print(t)
        ident = self.symbolStack.find_symbol(t.value)
        # print(ident)
        if not ident:
            print(t.value)
            # print(self.symbolStack)
            e = NoDefineError
            raise e
        v_type = ident.v_type

        if ident.v_type == SymbolType['FN_KW']:
            self.expect(TokenType['('])
            self.analyse_call_param_list()
            self.expect(TokenType[')'])
            # 在函数中找，然后查
            v_type = self.program.find_function(t.value).return_type
        elif self.check(TokenType['=']):
            self.expect(TokenType['='])
            self.analyse_expr()
            v_type = 'None'
        return v_type

    def analyse_test(self):
        while 1:
            if self.check('EOF'):
                print("finish")
                break
            else:
                tok = self.next()
                print(str(tok.value) + ' : ' + tok.type)
            # tok = self.next()
            # if not tok:
            #     print('EOF')
            #     break
            # else:
            #     print(tok)
            #     # print(tok.type)
            #     # print(self.check("IDENT"))
            #     # print(self.expect("FN_KW"))


