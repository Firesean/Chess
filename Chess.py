import Players
from Pieces import *
from PreviousMove import *
from PlayerManager import *
# https://en.wikipedia.org/wiki/Chess_symbols_in_Unicode


class Chess:
    board_size = 8
    board_colors = ["gray", "LightSalmon4"]
    default_board_state = ([Pawn().get_piece_name()] + [Rook().get_piece_name(), Knight().get_piece_name(),
                                                        Bishop().get_piece_name(), Queen().get_piece_name(),
                                                        King().get_piece_name(), Bishop().get_piece_name(),
                                                        Knight().get_piece_name(), Rook().get_piece_name()])
    movement_color = "firebrick3"

    def __init__(self, players=[Players.Player("White"), Players.Player("Black")]):
        # Declarations
        self.board = []
        self.moves_made = []
        self.player_manager = None
        self.players = players
        self.piece_directions = {f"{players[0].get_color()}": 1, f"{players[1].get_color()}": -1}
        # Downwards is 1 and Upwards is -1
        self.current_player = players[0]
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

    def append_to_moves_made(self, piece, pattern_name, row, col, old_row, old_col, captured=None):
        self.moves_made.append(PreviousMove(piece, pattern_name, old_row, old_col, row, col, captured))
    # Grab the pieces patterns and determine which pattern was used
    # Save it along with the distance taken to new position

    @staticmethod
    def create_piece(piece_name): # Takes a piece_name and creates a piece
        return eval(f'{piece_name}()')

    def get_board(self):
        return self.board

    def get_board_size(self):
        return self.board_size

    def get_current_color(self):
        return self.current_player.get_color()

    def get_current_player(self):
        return self.current_player

    def get_board_colors(self):
        return self.board_colors

    def get_movement_color(self):
        return self.movement_color

    def get_last_move_made(self):
        if len(self.moves_made) != 0:
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
        return self.piece_directions

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
            piece.increment_rank()
            if Pattern.DoubleJump().get_pattern_name() in pattern_name:
                piece.increment_rank()
            piece.off_bench()
            if piece.get_rank() == self.get_board_size() - 2:
                print("Pawn Promotion")
        elif piece.get_piece_name() == King().get_piece_name():
            piece.move_king()
            # If last move as EnPassant
        if Pattern.EnPassant().get_pattern_name() in pattern_name:
            piece_direction = self.get_piece_directions()[piece.get_color()]
            captured = self.get_space(row-piece_direction, col)
            self.board[row-piece_direction][col] = None
        self.append_to_moves_made(piece, pattern_name, row, col, old_row, old_col, captured)
        self.board[old_row][old_col] = None
        self.board[row][col] = piece

    def new_board(self):
        self.board = []
        for row in range(self.board_size):
            self.board.append([None])
            self.board[row] *= self.board_size

    def set_board(self, board): # Takes 2D Array with items of Piece Classes to build a board given
        for row in board:
            for col in row:
                pass

    def set_move_able(self, move_able):
        self.move_able = move_able

    def set_piece(self, piece, row, col, color): # Set a piece
        self.board[row][col] = piece
        self.get_space(row, col).set_color(color)
        # Add piece to player's pieces based on color

    def set_start_pieces(self): # Set multiple pieces
        # Default layout
        '''
        Generates the board with new pieces and sets location & color
        Will adjust to take a template and place piece for piece
        '''
        for start, end, side, player in [[1, -1, -1, self.players[0]],
                                        [self.board_size-2, self.board_size, 1, self.players[1]]]:
            for row in range(start, end, side):
                for col in range(self.board_size):
                    piece = self.default_board_state[col + 1]
                    if row == start:
                        piece = self.default_board_state[0]
                    self.set_piece(self.create_piece(piece), row, col, player.get_color())
                    player.add_piece(piece)

    def switch_player(self):
        new_player = self.players.index(self.current_player) - 1
        self.current_player = self.players[new_player]
