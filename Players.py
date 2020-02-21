class Player:
    black = "Black"
    white = "White"

    def __init__(self, color=white, pieces=[]):
        self.color = color
        self.pieces = pieces

    def add_piece(self, piece):
        self.pieces.append(piece)

    def get_color(self):
        return self.color

    def take_piece(self, piece):
        return self.pieces.remove(piece)

    def get_pieces(self):
        return self.pieces

