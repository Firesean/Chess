class Piece:
    '''
    Piece Class,
    piece_types is a selector for different classes,
    piece is a dictionary containing (color and piece type) attributes for unicode of pieces
    '''
    piece_types = ["Pawn", "Knight", "Bishop", "Rook", "Queen", "King"]
    pieces = {"White Pawn": u"\u265F", "White Knight": u"\u265E", "White Bishop": u"\u265D",
              "White Rook": u"\u265C", "White Queen": u"\u265B", "White King": u"\u265A",
              "Black Pawn": u"\u2659", "Black Knight": u"\u2658", "Black Bishop": u"\u2657",
              "Black Rook": u"\u2656", "Black Queen": u"\u2655", "Black King": u"\u2654"}

    def __init__(self, row=0, col=0):  # Position = Row 1-8 (A - G) Col 1-8
        '''
        :param row:
        :param col:
        Generates Piece Class based on subclass,
        pieceType is the name of current class,
        color is set within program,
        pattern is a list containing possible movement types
        '''
        self.row = row
        self.col = col
        self.pieceType = type(self).__name__
        self.color = None
        self.pattern = []

    def get_row(self):
        '''
        :return: self.row
        '''
        return self.row

    def get_col(self):
        '''
        :return: self.col
        '''
        return self.col

    def get_piece_type(self):
        '''
        :return: self.pieceType
        '''
        return self.pieceType

    def set_color(self, color):
        '''
        :param color:
        :return: None
        Sets piece color
        '''
        self.color = color

    def get_color(self):
        '''
        :return: self.color
        '''
        return self.color

    def get_image_path(self):
        '''
        :return: Dictionary Key for unicode
        Using the color and pieceType class name
        '''
        return self.color + " " + self.pieceType


class Pawn(Piece):
    '''
    Pawn, weakest but no the worst piece,
    Moves one square upwards at a time,
    Can attack diagonally by one square,
    Can move upwards by two square while on bench,
    En Passant : Can take a pawn that just moved double from bench and is aside of the current pawn,
    Must switch piece type if reaches opponents edge,
    '''
    onBench = True

    def at_bench(self):
        return self.onBench

    def move_pattern(self):
        pass

    def move(self, x, y):
        self.row += x
        self.col += y
        self.onBench = False


class Bishop(Piece):
    '''
    Bishop,
    Moves diagonally infinitely on to an enemy piece or before a friendly piece
    '''
    pass
    # Value : 3
    # Moves diagonally as far as possible


class Knight(Piece):
    '''
    Knight,
    Moves in a L shape Moves 3 squares and 1 square in the opposite direction
    Up or Down 3 Left or Right 1
    Left or Right 3 Up or Down 1
    Can Hop Pieces
    '''
    pass
    # Value : 3
    # Moves in a L pattern 3 vertically 1 across or 1 vertically and 3 across from
    # Current position
    # Can hop over pieces


class Rook(Piece):
    '''
    Rook,
    Moves Horizontal and Vertically infinitely on to an enemy piece or before a friendly piece,
    Castling : Can be used if current Rook and King haven't moved with No Pieces between the two,
    King moves over 2 spaces with the Rook placed behind the King's path
    '''
    moved = False
    pass
    # Value : 5
    # Moves in straight lines (No diagonals) as far as possible
    # Castling if it hasn't moved from originally position


class Queen(Piece):
    '''
    Queen,
    Moves Horizontal, Vertical, and Diagonal infinitely on to an enemy piece or before a friendly piece
    '''
    pass
    # Value : 9
    # Moves any direction as far as possible
    # Most valuable piece


class King(Piece):
    '''
    King, Most Valuable Piece
    Moves one Square in any direction
    Castling : As stated in Rook class, King moves two squares and the Rook is placed behind the King
    Check : In threat of being taken, Must be saved
    Checkmate : No moves can be made to save
    '''
    pass
    # Value : inf
    inCheck = False
    moved = False

    def has_moved(self):
        return self.moved

    def get_in_check(self):
        return self.inCheck

    # Moves any direction by one square
    # If King hasn't been in check and moved it can do a movement to left or right by 2 squares
    # followed by the rook placed behind to the king known as Castling
    # If King is captured the player whose King is captured loses.
    # If King is at threat then that player whose King is threaten Must
    # Try to get out of check if no way of getting out of check is possible it is Check Mate / Game over
    # Players can not intentionally move the King into check as it is an Illegal move


