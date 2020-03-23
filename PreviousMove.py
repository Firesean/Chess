class PreviousMove:
    '''
    This class will later be used to move backwards through the game
    if needed for testing purposes or beginner usage against AI Agent.
    '''

    def __init__(self, piece=None, pattern_name="", old_row=0, old_col=0, new_row=0, new_col=0, captured=None):
        self.CAPTURED = captured
        self.NEW_COL = new_col
        self.NEW_ROW = new_row
        self.OLD_COL = old_col
        self.OLD_ROW = old_row
        self.PATTERN_NAME = pattern_name
        self.PIECE = piece

    def display_all(self):
        print(f'''
        Captured : {self.CAPTURED}
        New Row : {self.NEW_ROW}
        New Col : {self.NEW_COL}
        Old Row : {self.OLD_ROW}
        Old Col : {self.OLD_COL}
        Pattern : {self.PATTERN_NAME}
        Piece : {self.PIECE}
        ''')

    def get_captured(self):
        return self.CAPTURED

    def get_pattern_used(self):
        if self.PATTERN_NAME:
            return self.PATTERN_NAME

    def get_piece_used(self):
        return self.PIECE

    def is_default(self):
        if [self.OLD_ROW, self.OLD_COL] == [self.NEW_ROW, self.NEW_COL]:
            return True
        return False

