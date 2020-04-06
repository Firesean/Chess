import Pieces


class MovementPattern:
    '''
    Movement Pattern Class always for a set of methods which the primary use is to calculate positions of
    the function return_positions for a specified movement pattern
    A template for the board to determine moves
    '''
    ROW_INDEX = 0
    COL_INDEX = 1


    def __init__(self, quadrant_corners=2, max_distance=7):
        self.max_distance = max_distance
        self.quadrant_corners = quadrant_corners

    @staticmethod
    def get_direction_of(quadrant, axis):
        # Input is a quadrant, in a geometric / algebraic  term of a xy axis graph
        # The piece is considered a 0,0 and directions around the piece are determined by input
        # With the quadrant we choose and determine which direction within the quadrant we return based on the axis_direction
        # Either X or Y value within the binary is returned X - 0 Index , Y - 1 Index
        quadrant = bin(quadrant+1)[-2:].replace("b", "0")  # Returns the last 2 characters of the binary
        # Input = Integer + 1 -> Bin, using the last two characters
        # Examples : 01 10 11 00
        #            xy xy xy xy
        return int(str(quadrant[axis]).replace("0", "-1"))  # Returns the direction of item based on index given
        # Outputs
        # Horizontal : 1 = Right, -1 = Left using an X index
        # Vertical : -1 = Up, 1 = Down using Y index
        # Diagonal : -1, 1 = Top Left, 1, -1 = Bottom Right, 1, 1 = Top Right, -1, -1 = Bottom Left, using Both indexes

    def get_max_distance(self):
        return self.max_distance

    def get_pattern_name(self):
        return type(self).__name__

    def is_movable(self, board, piece, new_row, new_col):
        space = board.get_space(new_row, new_col)
        piece_type = piece.get_piece_name()
        if not board.is_on_board(new_row, new_col):
            return False
        elif space and space.get_color() == piece.get_color():  # Runs into same colored piece
            return False
        elif Pieces.Pawn().get_piece_name() == piece_type:
            return self.is_valid_pawn_move(board, piece, new_row, new_col, self)
        # Other
        return True

    def is_valid_pawn_move(self, game, pawn, new_row, new_col, pattern):
        piece_direction = game.get_piece_directions()[pawn.get_color()] # Up or Down
        y_pos = game.get_piece_pos(pawn)[self.ROW_INDEX] # Grabs position of piece
        if piece_direction > 0: # Black moving Down
            if y_pos < new_row:
                return self.validate_pawn_move(game, pawn, new_row, new_col, pattern)
        elif piece_direction < 0: # White moving Up
            if y_pos > new_row:
                return self.validate_pawn_move(game, pawn, new_row, new_col, pattern)
        return False

    @staticmethod
    def validate_pawn_move(board, pawn, new_row, new_col, pattern):
        if pattern.get_pattern_name() == Vertical().get_pattern_name():
            if pattern.get_max_distance() > 1 and not pawn.at_bench():
                return False
            elif board.get_space(new_row, new_col):
                return False
            return True
        elif board.get_space(new_row, new_col) and pattern.get_pattern_name() == Diagonal().get_pattern_name():
            return True
        return False

class Castling(MovementPattern):

    # Has he moved, The King
    # piece COL
    # Rook COL - Piece, positions between
    # Range piece Col+1 Rook COL
    # IF THERE IS A PIECE BETWEEN
    #   RETURN FALSE
    # Else
    #   TRUE
    # Next Rook
    # After Rooks are determined check for Kings possibilities
    # Your king must not pass through a square that is under attack / threat by enemy pieces;
    # The king must not end up in check.

    def return_positions(self, piece, game):
        move_able = []
        rooks = []
        if piece.moved:
            return move_able
        piece_pos = game.get_piece_pos(piece)
        # Col : 0 Index and Board Size - 1 Index for Rooks
        for col in [0, game.get_board_size() - 1]:
            other_piece = game.get_space(piece_pos[self.ROW_INDEX], col)
            if other_piece and other_piece.get_piece_name() == Pieces.Rook().get_piece_name():
                # Has rook moved and check for matching colors
                rooks.append(other_piece)
        for rook in rooks:
            rook_patterns = game.get_pattern_and_moves(rook)
            spaces_between = []
            for pattern in rook_patterns:
                for move in rook_patterns[pattern]:
                    if move[self.ROW_INDEX] == piece_pos[self.ROW_INDEX]:
                        spaces_between.append(move)
                for move in spaces_between:
                    if move: # Check if move would be through check
                        break
                else: # Not through check
                    pass

            if len(spaces_between) + 1 == abs(piece_pos[self.COL_INDEX] - game.get_piece_pos(rook)[self.COL_INDEX]):
                print("True")
            else:
                print("False")
        # Return king's directions if can move
        return move_able

class Diagonal(MovementPattern):

    def return_positions(self, piece, game):
        move_able = []
        cur_row, cur_col = game.get_piece_pos(piece)
        # Refer to get_direction_of for understanding of the code statement below
        for quadrant in range(self.quadrant_corners):
            row_dir, col_dir = self.get_direction_of(quadrant, self.ROW_INDEX), self.get_direction_of(quadrant, self.COL_INDEX)
            for distance in range(1, self.max_distance + 1):
                new_row, new_col = cur_row + distance * col_dir, cur_col + distance * row_dir
                if self.is_movable(game, piece, new_row, new_col):
                    # Will King be threaten
                    if piece.get_piece_name() == Pieces.Pawn().get_piece_name():
                        if not self.is_valid_pawn_move(game, piece, new_row, new_col, self):
                            break
                    move_able.append([new_row, new_col])
                    if game.get_space(*move_able[-1]):
                        break
                else:
                    break
        return move_able

class DoubleJump(MovementPattern):

    def return_positions(self, piece, game):
        return Vertical(self.quadrant_corners, self.max_distance).return_positions(piece, game)

class EnPassant(MovementPattern):

    def return_positions(self, piece, game):
        move_able = []
        last_move =  game.get_last_move_made()
        if not last_move.is_default():
            other_piece = last_move.get_piece_used()
            if DoubleJump().get_pattern_name() in last_move.get_pattern_used(): # Is Double jump
                piece_direction = game.get_piece_directions()[piece.get_color()]
                if self.is_adjacent(game, piece, other_piece):
                    # Will King be threaten
                    other_piece_pos = game.get_piece_pos(other_piece)
                    move_able.append([other_piece_pos[self.ROW_INDEX] + piece_direction , other_piece_pos[self.COL_INDEX]])
        return move_able

    def is_adjacent(self, game, piece, other_piece):
        piece_pos = game.get_piece_pos(piece)
        other_pos = game.get_piece_pos(other_piece)
        if piece_pos[self.ROW_INDEX] == other_pos[self.ROW_INDEX]:
            if abs(piece_pos[self.COL_INDEX] - other_pos[self.COL_INDEX]) == 1:
                return True
        return False

class Horizontal(MovementPattern):

    def return_positions(self, piece, game):
        move_able = []
        cur_row, cur_col = game.get_piece_pos(piece)
        # Refer to get_direction_of for understanding of the code statement below
        for quadrant in range(self.quadrant_corners):
            row_dir = self.get_direction_of(quadrant, self.ROW_INDEX)
            for distance in range(1, self.max_distance + 1):
                new_col = cur_col + distance * row_dir
                if self.is_movable(game, piece, cur_row, new_col):
                    # Will King be threaten
                    move_able.append([cur_row, new_col])
                    if game.get_space(*move_able[-1]):
                        break
                else:
                    break
        return move_able


class LJump(MovementPattern):

    def return_positions(self, piece, game):
        moves = [(1, self.max_distance),(self.max_distance ,1)]
        move_able = []
        cur_row, cur_col = game.get_piece_pos(piece)
        # Refer to get_direction_of for understanding of the code statement below
        for quadrant in range(self.quadrant_corners):
            row_dir, col_dir = self.get_direction_of(quadrant, self.ROW_INDEX), self.get_direction_of(quadrant, self.COL_INDEX)
            for move in moves:
                new_row, new_col = cur_row + move[0] * col_dir, cur_col + move[1] * row_dir
                if self.is_movable(game, piece, new_row, new_col):
                    # Will King be threaten
                    move_able.append([new_row, new_col])
        return move_able

class Vertical(MovementPattern):

    def return_positions(self, piece, game):
        move_able = []
        cur_row, cur_col = game.get_piece_pos(piece)
        # Refer to get_direction_of for understanding of the code statement below
        for quadrant in range(self.quadrant_corners):
            y_dir = self.get_direction_of(quadrant, self.COL_INDEX)

            if piece.get_piece_name() == Pieces.Pawn().get_piece_name():
                piece_direction = game.get_piece_directions()[piece.get_color()]
                if piece_direction != y_dir:
                    continue

            elif piece.get_piece_name() == Pieces.King().get_piece_name():
                if not piece.is_moved(): # Haven't Moved
                    pass

            for distance in range(1, self.max_distance + 1):
                new_row = cur_row + distance * y_dir
                if self.is_movable(game, piece, new_row, cur_col):
                    # Will King be threaten
                    move_able.append([new_row, cur_col])
                    if game.get_space(*move_able[-1]):
                        break
                else:
                    break
        return move_able







