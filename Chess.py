# import Players

from Pieces import *


class Chess:
    default_board_size = 8
    default_board_state = ([Pawn(0,0, Piece.pieces[0])]*default_board_size)+\
                          [Rook(0,0, Piece.pieces[3]), Knight(0,0,Piece.pieces[1]),
                           Bishop(0,0, Piece.pieces[2]),Queen(0,0, Piece.pieces[4]),
                           King(0,0, Piece.pieces[5]), Bishop(0,0, Piece.pieces[2]),
                           Knight(0,0, Piece.pieces[1]), Rook(0,0,Piece.pieces[3])]

    def __init__(self, board_size=default_board_size):
        # Declarations
        self.board_size = board_size
        self.board = []
        self.players = []
        # Main
        self.create_board()
        self.set_up_board()
        for row in self.board:
            for piece in row:
                if piece is None:
                    print(None, end=" ")
                    continue
                print(piece.get_piece_type(), end=" ")
            print("\n")

    def create_board(self):
        self.board = []
        for row in range(self.board_size):
            self.board.append([None])
            self.board[row] *= self.board_size

    def set_up_board(self):
        for start, end, side in [[1, -1, -1], [self.board_size-2, self.board_size, 1]]:  # Direction of placing pieces
            for row in range(start, end, side):
                for col in range(self.board_size):
                    if row == start:
                        self.board[row][col] = self.default_board_state[col]  # Sets pawns
                    else:
                        self.board[row][col] = self.default_board_state[col+self.board_size]  # Sets piece order

    # def canMove(self, piece , x , y):
    #     movePattern = piece.movePattern()

    def get_space(self, x, y):
        return self.board[x][y]


Chess()
