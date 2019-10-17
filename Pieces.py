class Piece:
    piece_types = ["Pawn", "Knight", "Bishop", "Rook", "Queen", "King"]
    pieces = {"White Pawn": u"\u265F", "White Knight": u"\u265E", "White Bishop": u"\u265D",
              "White Rook": u"\u265C", "White Queen": u"\u265B", "White King": u"\u265A",
              "Black Pawn": u"\u2659", "Black Knight": u"\u2658", "Black Bishop": u"\u2657",
              "Black Rook": u"\u2656", "Black Queen": u"\u2655", "Black King": u"\u2654"}

    def __init__(self, row=0, col=0):  # Position = Row 1-8 (A - G) Col 1-8
        self.row = row
        self.col = col
        self.patterns = ["<", "^", ">", "V"]
        self.pieceType = type(self).__name__
        self.color = None

    def get_row(self):
        return self.row

    def get_col(self):
        return self.col

    def get_piece_type(self):
        return self.pieceType

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def get_image(self):
        return self.color + " " + self.pieceType

class Pawn(Piece):
    onBench = True

    def at_bench(self):
        return self.onBench

    def move_pattern(self):
        pass
    # Double move on bench
    # Takes pieces diagonally
    # Moves forward once
    # En Passant after a pawn uses a double move you can capture by going behind it
    # Pawn Promotion - If a pawn reaches the opponents edge MUST be promoted to any piece aside
    # from a King

    def move_piece(self, x, y):
        self.row += x
        self.col += y
        self.onBench = False


class Bishop(Piece):
    pass
    # Moves diagonally as far as possible


class Knight(Piece):
    pass
    # Moves in a L pattern 3 vertically 1 across or 1 vertically and 3 across from
    # Current position
    # Can hop over pieces


class Rook(Piece):
    pass
    # Moves in straight lines (No diagonals) as far as possible
    # Castling if hasn't moved from originally position


class Queen(Piece):
    pass
    # Moves any direction as far as possible
    # Most valuable piece


class King(Piece):
    pass
    inCheck = False
    moved = False

    def has_moved(self):
        return self.moved

    def get_in_check(self):
        return self.inCheck

    # Moves any direction by one square
    # If King hasn't been in check and moved it can do a movement to left or right by 2 squares
    # followed by the rook placed next to the king known as Castling
    # If King is captured the player whose King is captured loses.
    # If King is at threat then that player whose King is threaten Must
    # Try to get out of check if no way of getting out of check it is Check Mate / Game over
    # Players can not intentionally move the King into check as it is an Illegal move


