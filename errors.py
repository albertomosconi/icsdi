from strings_with_arrows import *

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
        result += '\n\n' + \
            string_with_arrows(self.pos_start.ftxt,
                               self.pos_start, self.pos_end)
        return result


class IllegalCharError(Error):
    'unsupported character error object'

    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


class InvalidSyntaxError(Error):
    'error that happens in the parsing process'

    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Invalid Syntax", details)
