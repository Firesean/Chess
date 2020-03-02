class PreviousMove:
    '''
    This class will later be used to move backwards through the game if needed if testing purposes or beginner's usage against AI
    Agent.
    '''

    def __init__(self, piece=None, pattern_name="", old_row=0, old_col=0, new_row=0, new_col=0, captured=None):
        self.captured = captured
        self.new_col = new_col
        self.new_row = new_row
        self.old_col = old_col
        self.old_row = old_row
        self.pattern_name = pattern_name
        self.piece = piece

    def display_all(self):
        print(f'''
        Captured : {self.captured}
        New Row : {self.new_row}
        New Col : {self.new_col}
        Old Row : {self.old_row}
        Old Col : {self.old_col}
        Pattern : {self.pattern_name}
        Piece : {self.piece}
        ''')

    def get_captured(self):
        return self.captured

    def get_pattern_used(self):
        if self.pattern_name:
            return self.pattern_name

    def get_piece_used(self):
        return self.piece

    def is_default(self):
        if [self.old_row, self.old_col] == [self.new_row, self.new_col]:
            return True
        return False

