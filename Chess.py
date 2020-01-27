import Players
from Pieces import *
# https://en.wikipedia.org/wiki/Chess_symbols_in_Unicode


class Chess:
    board_size = 8
    default_board_colors = ["gray", "LightSalmon4"]
    default_board_state = ([Pawn().get_piece_name()] + [Rook().get_piece_name(), Knight().get_piece_name(),
                                                        Bishop().get_piece_name(), Queen().get_piece_name(),
                                                        King().get_piece_name(), Bishop().get_piece_name(),
                                                        Knight().get_piece_name(), Rook().get_piece_name()])
    default_movement_color = "firebrick3"
    default_piece_colors = [Players.Player.black, Players.Player.white]
    default_piece_directions = {f"{default_piece_colors[0]}" : 1, f"{default_piece_colors[1]}" : -1} # Down = 1 , Up = 1
    current_player = default_piece_colors[0]

    def __init__(self):
        # Declarations
        self.board = []
        self.last_move = None
        self.last_piece = None
        self.players = []

        # Main
        self.move_able = []
        self.new_board()
        self.set_pieces()
        self.selected_piece = None

    @staticmethod
    def create_piece(piece):
        return eval(f'{piece}()')

    def get_board(self):
        return self.board

    def get_board_size(self):
        return self.board_size

    def get_current_player(self):
        return self.current_player

    def get_default_board_colors(self):
        return self.default_board_colors

    def get_default_movement_color(self):
        return self.default_movement_color

    def get_default_piece_colors(self):
        return self.default_piece_colors

    def get_default_piece_directions(self):
        return self.default_piece_directions

    def get_move_able(self):
        return self.move_able

    def get_pattern_positions(self, pattern, piece):
        return pattern.return_positions(piece, self)

    def get_piece_pos(self, piece):
        for row in range(len(self.board)):
            if piece in self.board[row]:
                return row, self.board[row].index(piece)  # row, col

    def get_space(self, row, col):
        if self.is_on_board(row, col):
            return self.board[row][col]
        return None

    def is_on_board(self, row, col):
        if row < 0 or col < 0:
            return False
        if row >= self.get_board_size() or col >= self.get_board_size():
            return False
        return True

    def movable_position(self, piece, row, col):
        position = self.get_space(row, col)
        if position and piece.get_color() == position.get_color():
            return False
        if not self.is_on_board(row, col):
            return False
        return True


    def move_piece_on_board(self, piece, row, col):
        old_row, old_col = self.get_piece_pos(piece)
        if piece.get_piece_name() == Pawn().get_piece_name():
            piece.off_bench()
        self.board[old_row][old_col] = None
        self.board[row][col] = piece

    def new_board(self):
        self.board = []
        for row in range(self.board_size):
            self.board.append([None])
            self.board[row] *= self.board_size

    def set_move_able(self, move_able):
        self.move_able = move_able

    def set_pieces(self):
        '''
        Generates the board with new pieces and sets location & color
        '''
        for start, end, side, color in [[1, -1, -1, self.default_piece_colors[0]],
                                        [self.board_size-2, self.board_size, 1, self.default_piece_colors[1]]]:
            for row in range(start, end, side):
                for col in range(self.board_size):
                    piece = self.default_board_state[col + 1]
                    if row == start:
                        piece = self.default_board_state[0]
                    new_piece = self.create_piece(piece)
                    self.board[row][col] = new_piece
                    self.get_space(row, col).set_color(color)

    def switch_player(self):
        new_player = self.default_piece_colors.index(self.current_player) - 1
        self.current_player = self.default_piece_colors[new_player]


