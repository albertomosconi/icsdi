from constants import DIGITS, TT_INT, TT_FLOAT, TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_LPAREN, TT_RPAREN
from nodes import NumberNode, BinOpNode

########################
# PARSER
########################


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_idx = -1
        self.advance()

    def advance(self):
        self.token_idx += 1
        if self.token_idx < len(self.tokens):
            self.current_token = self.tokens[self.token_idx]
        return self.current_token

    def parse(self):
        res = self.expr()
        return res

    def factor(self):
        'returns NumberNode if the current token is an INT or FLOAT'
        tok = self.current_token

        if tok.type in (TT_INT, TT_FLOAT):
            self.advance()
            return NumberNode(tok)

    def term(self):
        'evaluates term'
        return self.binary_operation(self.factor, (TT_MUL, TT_DIV))

    def expr(self):
        'evaluates expression'
        return self.binary_operation(self.term, (TT_PLUS, TT_MINUS))

    def binary_operation(self, func, ops):
        'returns BinOpNode for allowed operators (ops) using "func" to get the left and right nodes'
        left = func()

        while self.current_token.type in ops:
            op_token = self.current_token
            self.advance()
            right = func()
            left = BinOpNode(left, op_token, right)

        return left
