########################
# CONSTANTS
########################

DIGITS = '0123456789'

########################
# ERRORS
########################


class Error:
    'general error class'

    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        'return error as string'
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln+1}'
        return result


class IllegalCharError(Error):
    'unsupported character error object'

    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

########################
# POSITION
########################


class Postition:
    'object that holds the current position in the file: index, line and column'

    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn  # file name
        self.ftxt = ftxt  # file content

    def advance(self, current_char):
        'moves forward of one character'
        self.idx += 1
        self.col += 1

        if current_char == '\n':  # end of the line
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        'return a copy of the position object'
        return Postition(self.idx, self.ln, self.col, self.fn, self.ftxt)


########################
# TOKENS
########################


'data types'
TT_INT = 'TT_INT'
TT_FLOAT = 'FLOAT'

'operands'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'

'parenthesis'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'


class Token:
    'the token object'

    def __init__(self, type_, value=None):
        'initialize token object'
        self.type = type_
        self.value = value

    def __repr__(self):
        'display the object'
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'

########################
# LEXER
########################


class Lexer:
    def __init__(self, fn, text):
        'initialize lexer object'
        self.fn = fn  # file name
        self.text = text  # text that will be processed
        self.pos = Postition(-1, 0, -1, fn, text)  # current position
        self.current_char = None  # current character
        self.advance()  # move to the first char

    def advance(self):
        'moves the lexer to the next character of the text'
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(
            self.text) else None

    def make_tokens(self):
        'creates a list of tokens from the input text'
        tokens = []

        while self.current_char != None:
            cc = self.current_char
            if cc in ' \t':  # ignore spaces and tabs
                self.advance()
            elif cc in DIGITS:
                tokens.append(self.make_number())
            elif cc == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif cc == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif cc == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif cc == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif cc == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif cc == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            else:
                pos_start = self.pos.copy()
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + cc + "'")

        return tokens, None

    def make_number(self):
        'finds the number that starts with the digit in current_char'
        num_str = ''
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + '.':
            cc = self.current_char
            if cc == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += cc
            self.advance()

        if dot_count == 0:  # if there isn't a dot it means the number is an INT
            return Token(TT_INT, int(num_str))
        else:  # otherwise it's a FLOAT
            return Token(TT_FLOAT, float(num_str))


########################
# NODES
########################

class NumberNode:
    'syntax tree node that holds either INT or FLOAT numbers'

    def __init__(self, token):
        self.token = token

    def __repr__(self):
        'display node'
        return f'{self.token}'


class BinOpNode:
    'syntax tree node for binary operators: +, -, etc'

    def __init__(self, left_node, op_token, right_node):
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node

    def __repr__(self):
        'display node'
        return f'({self.left_node}, {self.op_token}, {self.right_node})'


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
