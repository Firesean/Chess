class Player:
    black = "Black"
    white = "White"

    def __init__(self, score=0, color=white, pieces=[]):
        self.color = color
        self.pieces = []

    def get_color(self):
        return self.color

    def take_piece(self, piece):
        return self.pieces.remove(piece)


