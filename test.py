from tokenizer.Token import Tokenizer


# f = open('input.rs')
# fileContent = f.read()
# # print(fileContent)
# f.close()
f = open('input.rs')
tokenizer = Tokenizer(f.read())
# tokenizer.lexer.input()
while 1:
    tok = tokenizer.token()
    if not tok:
        break
    print(tok)
