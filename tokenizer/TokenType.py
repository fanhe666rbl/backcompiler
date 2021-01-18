

TokenType = {
    # 关键字
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
    # 运算符
    '+': 'PLUS',  # -> '+'
    '-': 'MINUS',  # -> '-'
    '*': 'MUL',  # -> '*'
    '/': 'DIV',  # -> '/'
    '=': 'ASSIGN',  # -> '='
    '==': 'EQ',  # -> '=='
    '!=': 'NEQ',  # -> '!='
    '<': 'LT',  # -> '<'
    '>': 'GT',  # -> '>'
    '<=': 'LE',  # -> '<='
    '>=': 'GE',  # -> '>='
    '(': 'L_PAREN',  # -> '('
    ')': 'R_PAREN',  # -> ')'
    '{': 'L_BRACE',  # -> '{'
    '}': 'R_BRACE',  # -> '}'
    '->': 'ARROW',  # -> '->'
    ',': 'COMMA',  # -> ','
    ':': 'COLON',  # -> ':'
    ';': 'SEMICOLON',  # -> ';'
    # 字面量
    'int': 'UINT_LITERAL',  # -> digit+
    'void': 'VOID',  # void
    'type': 'TYPE',   # int|void|double
    'ID': 'IDENT',  # [_a-zA-Z][_a-zA-Z0-9]*
    'double': 'DOUBLE_LITERAL',  # -> digit+ '.' digit+ ([eE] digit+)?
    'string': 'STRING_LITERAL',  # 字符串

    'EOF': 'EOF'
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
     'IDENT',  # [_a-zA-Z][_a-zA-Z0-9]*
     'DOUBLE_LITERAL',  # -> digit+ '.' digit+ ([eE] digit+)?
     'STRING_LITERAL',  # 字符串

     # 'tmp', # 测试
     # 注释
     'COMMENT'  # '//' regex(.*) '\n'
]