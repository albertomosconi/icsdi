from position import Position
from constants import DIGITS, TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_LPAREN, TT_RPAREN, TT_FLOAT, TT_INT, TT_EOF
from tokens import Token
from errors import IllegalCharError
#######################################
# LEXER
#######################################


class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(
            self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            cc = self.current_char
            if cc in ' \t':
                self.advance()
            elif cc in DIGITS:
                tokens.append(self.make_number())
            elif cc == '+':
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()
            elif cc == '-':
                tokens.append(Token(TT_MINUS, pos_start=self.pos))
                self.advance()
            elif cc == '*':
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
            elif cc == '/':
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            elif cc == '(':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif cc == ')':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + cc + "'")

        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos)
