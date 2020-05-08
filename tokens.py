########################
# TOKENS
########################


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
