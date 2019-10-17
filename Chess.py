# import Players

from Pieces import *
# https://en.wikipedia.org/wiki/Chess_symbols_in_Unicode


class Chess:
    default_board_size = 8
    default_board_state = ([Pawn(Piece.piece_types[0])] * default_board_size) + \
                          [Rook(Piece.piece_types[3]), Knight(Piece.piece_types[1]),
                           Bishop(Piece.piece_types[2]), Queen(Piece.piece_types[4]),
                           King(Piece.piece_types[5]), Bishop(Piece.piece_types[2]),
                           Knight(Piece.piece_types[1]), Rook(Piece.piece_types[3])]

    def __init__(self, board_size=default_board_size):
        # Declarations
        self.board_size = board_size
        self.board = []
        self.players = []
        # Main
        self.create_board()
        self.set_up_board()
        self.show_board()

    def create_board(self):
        self.board = []
        for row in range(self.board_size):
            self.board.append([None])
            self.board[row] *= self.board_size

    def set_up_board(self):
        for start, end, side, color in [[1, -1, -1, "White"], [self.board_size-2, self.board_size, 1, "Black"]]:
            # Start row to End row by side then color is assigned
            print(start, end, side, color)
            for row in range(start, end, side):
                for col in range(self.board_size):
                    if row == start:
                        self.board[row][col] = self.default_board_state[col]  # Sets pawns
                    else:
                        self.board[row][col] = self.default_board_state[col+self.board_size]  # Sets piece order
                    self.board[row][col].set_color(color)

    def get_space(self, x, y):
        return self.board[x][y]

    def show_board(self):
        for row in self.board:
            for piece in row:
                if piece is None:
                    print(u"\u0011", end=" ")
                    continue
                print(Piece.pieces[piece.get_image()], end=" ")
            print("\n")

Chess()

