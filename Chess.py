# import Players
from Pieces import *
# https://en.wikipedia.org/wiki/Chess_symbols_in_Unicode


class Chess:
    default_colors = ["Black", "White"]
    board_size = 8
    default_board_state = ([Pawn().get_class_name()] + [Rook().get_class_name(), Knight().get_class_name(),
                           Bishop().get_class_name(), Queen().get_class_name(),
                           King().get_class_name(), Bishop().get_class_name(),
                           Knight().get_class_name(), Rook().get_class_name()])

    def __init__(self):
        # Declarations
        self.board = []
        self.players = []

        # Main
        self.new_board()
        self.set_pieces()
        self.selected_piece = None

    def get_board(self):
        return self.board

    def get_board_size(self):
        return self.board_size

    def get_piece_pos(self, piece):
        for i in range(len(self.board)):
            if piece in self.board[i]:
                return i, self.board[i].index(piece)  # row, col

    def get_space(self, row, col):
        if self.is_on_board(row, col):
            return self.board[row][col]
        else:
            return None

    def is_on_board(self, row, col):
        if row < 0 or col < 0:
            return False
        if row >= self.get_board_size() or col >= self.get_board_size():
            return False
        return True

    def move_piece_on_board(self, piece, row, col):
        old_row, old_col = self.get_piece_pos(piece)
        self.board[old_row][old_col] = None
        self.board[row][col] = piece

    def new_board(self):
        self.board = []
        for row in range(self.board_size):
            self.board.append([None])
            self.board[row] *= self.board_size

    def set_pieces(self):
        '''
        Generates the board with new pieces and sets location & color
        '''
        for start, end, side, color in [[1, -1, -1, self.default_colors[0]],
                                        [self.board_size-2, self.board_size, 1, self.default_colors[1]]]:
            for row in range(start, end, side):
                for col in range(self.board_size):
                    piece = self.default_board_state[col + 1]
                    if row == start:
                        piece = self.default_board_state[0]
                    new_piece = eval("{0}()".format(piece))
                    self.board[row][col] = new_piece
                    self.get_space(row, col).set_color(color)


