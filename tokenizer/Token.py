import ply.lex as lex
from ply.lex import TOKEN

reserved = {
    'fn': 'FN_KW',
    'let': 'LET_KW',
    'const': 'CONST_KW',
    'as': 'AS_KW',
    'while': 'WHILE_KW',
    'if': 'IF_KW',
    'else': 'ELSE_KW',
    'return': 'RETURN_KW',
    'break': 'BREAK_KW',
    'continue': 'CONTINUE_KW',
}

tokens = [
     'PLUS',  # -> '+'
     'MINUS',  # -> '-'
     'MUL',  # -> '*'
     'DIV',  # -> '/'
     'ASSIGN',  # -> '='
     'EQ',  # -> '=='
     'NEQ',  # -> '!='
     'LT',  # -> '<'
     'GT',  # -> '>'
     'LE',  # -> '<='
     'GE',  # -> '>='
     'L_PAREN',  # -> '('
     'R_PAREN',  # -> ')'
     'L_BRACE',  # -> '{'
     'R_BRACE',  # -> '}'
     'ARROW',  # -> '->'
     'COMMA',  # -> ','
     'COLON',  # -> ':'
     'SEMICOLON',  # -> ';'

     'UINT_LITERAL',  # -> digit+
     'TYPE',   # int|double|void
     'IDENT',  # [_a-zA-Z][_a-zA-Z0-9]*
     'DOUBLE_LITERAL',  # -> digit+ '.' digit+ ([eE] digit+)?
     'STRING_LITERAL',  # 字符串

     # 'tmp', # 测试
     # 注释
     'COMMENT'  # '//' regex(.*) '\n'
] + list(reserved.values())


def Lexer():
    # Regular expression rules for simple tokens

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_MUL = r'\*'
    t_DIV = r'/'
    t_EQ = r'=='
    t_ASSIGN = r'='

    t_NEQ = r'!='
    t_GE = r'>='
    t_LE = r'<='
    t_LT = r'<'
    t_GT = r'>'

    t_L_PAREN = r'\('
    t_R_PAREN = r'\)'

    t_L_BRACE = r'{'
    t_R_BRACE = r'}'
    t_ARROW = r'->'
    t_COMMA = r','
    t_COLON = r':'
    t_SEMICOLON = r';'

    t_ignore_COMMENT = r'//.*'
    # string_regular_char = r"""([^"\\])"""

    escape_sequence = r"""(\\[\\"'nrt])"""
    string_regular_char = r"""([^\n\t\r"\\])"""
    string_literal = r'"' + r'(' + string_regular_char + r'|' + escape_sequence + r')*' + r'"'

    @TOKEN(string_literal)
    def t_STRING_LITERAL(t):
        t.value = t.value[1:-1]
        return t
    # def t_COMMENT(t):
    #     r'//.*'
    #     pass

    # def t_tmp(t):
    #     r"""([^\s"\\])"""
    #     return t

    def t_TYPE(t):
        r"""(int|void|double)"""
        t.type = reserved.get(t.value, 'TYPE')  # Check for reserved words
        return t

    def t_IDENT(t):
        r"""[a-zA-Z_][a-zA-Z_0-9]*"""
        t.type = reserved.get(t.value, 'IDENT')  # Check for reserved words
        return t

    def t_DOUBLE_LITERAL(t):
        r"""\d+\.\d+([eE] \d+)?"""
        t.value = float(t.value)
        return t

    # A regular expression rule with some action code
    def t_UINT_LITERAL(t):
        r"""\d+"""
        t.value = int(t.value)
        return t

    # Define a rule so we can track line numbers
    def t_newline(t):
        r"""\n+"""
        t.lexer.lineno += len(t.value)

    # Compute column.
    #     input is the input text string
    #     token is a token instance
    def find_column(input_txt, token):
        last_cr = input_txt.rfind("\n", 0, token.lexpos)
        if last_cr < 0:
            last_cr = 0
        column = (token.lexpos - last_cr) + 1
        return column

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    # Error handling rule
    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer from my environment and return it
    return lex.lex()


class EOFToken:
    type = 'EOF'
    value = 'EOF'
    lexpos = -1
    lineno = -1


class Tokenizer:

    def __init__(self, data):
        self.lex = Lexer()
        self.lex.input(data)

    def next_token(self):
        tok = self.lex.token()
        if tok:
            return tok
        else:
            return EOFToken()


