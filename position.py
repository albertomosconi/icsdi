########################
# POSITION
########################


class Position:
    'object that holds the current position in the file: index, line and column'

    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn  # file name
        self.ftxt = ftxt  # file content

    def advance(self, current_char=None):
        'moves forward of one character'
        self.idx += 1
        self.col += 1

        if current_char == '\n':  # end of the line
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        'return a copy of the position object'
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)
