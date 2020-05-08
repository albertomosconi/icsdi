from constants import DIGITS, TT_INT, TT_FLOAT, TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_LPAREN, TT_RPAREN
from position import Postition
from tokens import Token
from errors import IllegalCharError

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
