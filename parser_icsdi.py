from constants import DIGITS, TT_INT, TT_FLOAT, TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_LPAREN, TT_RPAREN, TT_EOF
from nodes import NumberNode, BinOpNode, UnaryOpNode
from errors import InvalidSyntaxError

########################
# PARSER
########################


class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error:
                self.error = res.error
            return res.node

        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self


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
        if not res.error and self.current_token.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "Expected '+', '-', '*' or '/'"
            ))
        return res

    def factor(self):
        'returns NumberNode if the current token is an INT or FLOAT'
        res = ParseResult()
        tok = self.current_token

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())

            if res.error:
                return res

            return res.success(UnaryOpNode(tok, factor))

        elif tok.type in (TT_INT, TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))

        elif tok.type == TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())

            if res.error:
                return res

            if self.current_token.type == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Expected ')'"
                ))

        return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected INT or FLOAT"))

    def term(self):
        'evaluates term'
        return self.binary_operation(self.factor, (TT_MUL, TT_DIV))

    def expr(self):
        'evaluates expression'
        return self.binary_operation(self.term, (TT_PLUS, TT_MINUS))

    def binary_operation(self, func, ops):
        'returns BinOpNode for allowed operators (ops) using "func" to get the left and right nodes'
        res = ParseResult()
        left = res.register(func())

        if res.error:
            return res

        while self.current_token.type in ops:
            op_token = self.current_token
            res.register(self.advance())
            right = res.register(func())
            if res.error:
                return res
            left = BinOpNode(left, op_token, right)

        return res.success(left)
