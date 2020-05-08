########################
# CONTEXT
########################


class Context:
    'keeps track of which function calls the current char is in'

    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
