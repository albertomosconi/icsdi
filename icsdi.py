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
# RUN
########################

def run(fn, text):
    'runs lexer on input text and returns list of tokens and error'
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    return tokens, error
