class Player:
    black = "Black"
    white = "White"

    def __init__(self, score=0, color=white, pieces = []):
        self.color = color
        self.pieces = []
        self.score = score

    def get_color(self):
        '''
        :return: Player Color
        '''
        return self.color

    def get_score(self):
        '''
        :return: Score value
        '''
        return self.score

    def set_score(self, score):
        '''
        :param score:
        Sets score's value
        :return: None
        '''
        self.score = score

    def take_piece(self, piece):
        '''
        :param piece:
        Adds value to score
        Returns the piece removed
        :return:
        '''
        self.score += piece.get_value()
        return self.pieces.remove(piece)


