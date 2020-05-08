from lexer import Lexer
from parser_icsdi import Parser

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

    return ast.node, ast.error
