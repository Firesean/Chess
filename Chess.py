import Players
from Pieces import *
from PreviousMove import *
from PlayerManager import *

class Chess:
    BOARD_SIZE = 8
    BOARD_COLORS = ["gray", "LightSalmon4"]
    START_BOARD = ([Pawn().get_piece_name()] + [Rook().get_piece_name(), Knight().get_piece_name(),
                                                Bishop().get_piece_name(), Queen().get_piece_name(),
                                                King().get_piece_name(), Bishop().get_piece_name(),
                                                Knight().get_piece_name(), Rook().get_piece_name()])
    MOVEMENT_COLOR = "firebrick3"

    def __init__(self, pm=PlayerManager([Players.Player("White", []), Players.Player("Black", [])])):
        # Declarations
        self.board = []
        self.moves_made = []
        self.PM = pm # Player Manager
        self.PLAYERS = pm.get_players()
        self.PIECE_DIRECTIONS = {f"{self.PLAYERS[0].get_color()}": 1, f"{self.PLAYERS[1].get_color()}": -1}
        # Downwards is 1 and Upwards is -1
        self.current_player = self.PLAYERS[0]
        # Main
        self.move_able = {}
        self.new_board()
        self.set_start_pieces()
        self.selected_piece = None

    def all_possible_moves(self, player):
        moves = []
        for piece in player.get_pieces():
            moves = self.get_pattern_and_moves(piece)
        return moves

    @staticmethod
    def alter_pawn(piece, pattern_name):
        piece.increment_rank()
        if Pattern.DoubleJump().get_pattern_name() in pattern_name:
            piece.increment_rank()
        piece.off_bench()

    def append_to_moves_made(self, piece, pattern_name, row, col, old_row, old_col, captured=None):
        self.moves_made.append(PreviousMove(piece, pattern_name, old_row, old_col, row, col, captured))


    def check_pawn_promotion(self):
        last_move = self.get_last_move_made()
        piece = last_move.get_piece_used()
        if piece.get_piece_name() == Pawn().get_piece_name():
            if piece.get_rank() == self.get_board_size() - 2:
                return True
        return False

    @staticmethod
    def create_piece(piece_name): # Takes a piece_name and creates a piece
        return eval(f'{piece_name}()')


    def get_board(self):
        return self.board

    def get_board_size(self):
        return self.BOARD_SIZE

    def get_current_color(self):
        return self.current_player.get_color()

    def get_board_colors(self):
        return self.BOARD_COLORS

    def get_movement_color(self):
        return self.MOVEMENT_COLOR

    def get_last_move_made(self):
        if self.moves_made:
            return self.moves_made[-1]
        return PreviousMove()

    def get_move_able(self):
        return self.move_able

    @staticmethod
    def get_move_pattern(move, moves):
        for key, value in moves.items():
            if not move in value: # Not a move able position
                continue
            else:
                return key # Returns pattern name
        return False

    def get_pattern_and_moves(self, piece):
        move_able = {}
        if piece.patterns:
            if isinstance(piece.patterns, tuple or list):
                for pattern in piece.patterns:
                    move_able[f"{pattern}"] = self.get_pattern_positions(pattern, piece)
            else:
                move_able[f"{piece.patterns}"] = self.get_pattern_positions(piece.patterns, piece)
        self.move_able = dict(move_able)
        return self.move_able

    def get_pattern_positions(self, pattern, piece):
        return pattern.return_positions(piece, self)

    def get_piece_directions(self):
        return self.PIECE_DIRECTIONS

    def get_piece_pos(self, piece):
        for row in range(len(self.board)):
            if piece in self.board[row]:
                return row, self.board[row].index(piece)  # row, col

    def get_space(self, row, col):
        if self.is_on_board(row, col):
            return self.board[row][col]
        return None

    def is_movable_position(self, piece, row, col):
        position = self.get_space(row, col)
        if position and piece.get_color() == position.get_color():
            return False
        if not self.is_on_board(row, col):
            return False
        return True

    def is_on_board(self, row, col):
        if row < 0 or col < 0:
            return False
        if row >= self.get_board_size() or col >= self.get_board_size():
            return False
        return True

    def move_piece_on_board(self, piece, pattern_name, row, col, captured=None):
        old_row, old_col = self.get_piece_pos(piece)
        # Temp placed here to adjust pieces
        if piece.get_piece_name() == Pawn().get_piece_name():
            self.alter_pawn(piece, pattern_name)
        elif piece.get_piece_name() == King().get_piece_name():
            piece.move_king()
        if Pattern.EnPassant().get_pattern_name() in pattern_name:
            piece_direction = self.get_piece_directions()[piece.get_color()]
            captured = self.get_space(row-piece_direction, col)
            self.board[row-piece_direction][col] = None
        self.append_to_moves_made(piece, pattern_name, row, col, old_row, old_col, captured)
        self.board[old_row][old_col] = None
        self.board[row][col] = piece

    def new_board(self):
        self.board = []
        for row in range(self.BOARD_SIZE):
            self.board.append([None])
            self.board[row] *= self.BOARD_SIZE

    def set_board(self, board): # Takes 2D Array with items of Piece Classes to build a board given
        self.board = board

    def set_move_able(self, move_able):
        self.move_able = move_able

    def set_piece(self, piece, row, col, color):
        self.board[row][col] = piece
        self.get_space(row, col).set_color(color)

    def set_start_pieces(self):
        for start, end, side, player in [[1, -1, -1, self.PLAYERS[0]],
                                         [self.BOARD_SIZE - 2, self.BOARD_SIZE, 1, self.PLAYERS[1]]]:
            for row in range(start, end, side):
                for col in range(self.BOARD_SIZE):
                    piece = self.START_BOARD[col + 1]
                    if row == start:
                        piece = self.START_BOARD[0]
                    self.set_piece(self.create_piece(piece), row, col, player.get_color())
                    player.add_piece(self.get_space(row, col))