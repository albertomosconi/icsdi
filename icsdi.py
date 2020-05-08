from lexer import Lexer
from parsericsdi import Parser

########################
# RUN
########################


def run(fn, text):
    'generate tokens'
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error

    'generate AST (abstract syntax tree)'
    parser = Parser(tokens)
    ast = parser.parse()

    return ast, None
