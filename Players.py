class Player:
    white = "White"
    black = "Black"

    def __init__(self, score=0, color=white, pieces = []):
        self.score = score
        self.color = color
        self.pieces = []

    def get_color(self):
        return self.color

    def take_piece(self, piece):
        return self.pieces.remove(piece)

    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score
