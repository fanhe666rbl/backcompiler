# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import argparse
from tokenizer.Token import Tokenizer
from analyser.Analyser import Analyser


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-te', help="this is a test")
    parser.add_argument('-l', '--analyse', action="store_true")
    parser.add_argument('-t', '--tokenize', action="store_true")
    parser.add_argument('-o', '--output')
    parser.add_argument('-i', '--input')
    args = parser.parse_args()
    if args.tokenize:
        print("to")
        if args.input:
            print(args.input)

            f = open('input.rs')
            fileContent = f.read()
            print(fileContent)
            f.close()
            f = open(args.input)
            tokenizer = Tokenizer(f.read())
            # tokenizer.lexer.input()
            while 1:
                tok = tokenizer.next_token()
                if not tok == 'EOF':
                    print(tok)
                else:
                    print('EOF')
                    break

    if args.analyse:
        print("an")
        if args.input:
            print(args.input)
            # f = open('input.rs')
            # fileContent = f.read()
            # # print(fileContent)
            # f.close()
            # f = open(args.input)
            # print(f.read())
            # f.close()
            f = open(args.input)
            tokenizer = Tokenizer(f.read())
            # tokenizer.lexer.input()
            analyser = Analyser(tokenizer, is_debug=True)
            # analyser.analyse_test()
            analyser.analyse()


# # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
