from lexer import Lexer
from parser_icsdi import Parser
from interpreter import Interpreter
from context import Context

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
    if ast.error:
        return None, ast.error

    'run program'
    interpreter = Interpreter()
    context = Context('<program>')
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
