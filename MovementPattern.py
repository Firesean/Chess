import Pieces


class MovementPattern:
    X_index = 0
    Y_index = 1

    def __init__(self, quadrant_corners=2, max_distance=7):
        self.max_distance = max_distance
        self.quadrant_corners = quadrant_corners

    @staticmethod
    def get_direction_of(quadrant, axis_direction):
        # Input is a quadrant, in a geometric / algebraic  term of a xy axis graph
        # The piece is considered a 0,0 and directions around the piece are determined by input
        # With the quadrant we choose and determine which direction within the quadrant we return based on the axis_direction
        # Either X or Y value within the binary is returned X - 0 Index , Y - 1 Index
        '''
        :param quadrant:
        :param axis_direction:
        :return: Returns direction as a translated binary, 0 being negative and 1 positive
        '''
        quadrant = bin(quadrant + 1)[-2:].replace("b", "0")  # Returns the last 2 characters of the binary
        # Input = Integer -> Bin, using the last two characters
        # Examples : 00 01 10 11
        #            xy xy xy xy
        return int(str(quadrant[axis_direction]).replace("0", "-1"))  # Returns the direction of item based on index given
        # Outputs
        # Horizontal : 1 = Right, -1 = Left using a index
        # Vertical : -1 = Up, 1 = Down using a index
        # Diagonal : -1, 1 = Top Left, 1, -1 = Bottom Right, 1, 1 = Top Right, -1, -1 = Bottom Left, using Both indexes

    @staticmethod
    def is_movable(board, piece, new_row, new_col):
        '''
        :param board:
        :param piece:
        :param new_row:
        :param new_col:
        :return: All possible moves as tuples within a list
        '''
        space = board.get_space(new_row, new_col)
        if not board.is_on_board(new_row, new_col):
            return False
        elif space and space.get_color() == piece.get_color():  # Runs into same colored piece
            return False
        else:  # Other
            return True


class Diagonal(MovementPattern):

    def return_positions(self, piece, board):
        '''
        :param piece:
        :param board:
        :return: Possible Movements
        '''
        move_able = []
        cur_row, cur_col = board.get_piece_pos(piece)
        # Refer to get_direction_of for understanding of the algorithm below
        for quadrant in range(self.quadrant_corners):
            x_dir, y_dir = self.get_direction_of(quadrant, self.X_index), self.get_direction_of(quadrant, self.Y_index)
            for distance in range(1, self.max_distance + 1):
                new_row, new_col = cur_row + distance * x_dir, cur_col + distance * y_dir
                if self.is_movable(board, piece, new_row, new_col):
                    move_able.append([new_col, new_row])
                    if board.get_space(*move_able[-1][::-1]):
                        break
                else:
                    break
        return move_able


class Horizontal(MovementPattern):

    def return_positions(self, piece, board):
        '''
        :param piece:
        :param board:
        :return: Possible Movements
        '''
        move_able = []
        cur_row, cur_col = board.get_piece_pos(piece)
        # Refer to get_direction_of for understanding of the algorithm below
        for quadrant in range(self.quadrant_corners):
            x_dir = self.get_direction_of(quadrant, self.X_index)
            for distance in range(1, self.max_distance + 1):
                new_col = cur_col + distance * x_dir
                if self.is_movable(board, piece, cur_row, new_col):
                    move_able.append([new_col, cur_row])
                    if board.get_space(*move_able[-1][::-1]):
                        break
                else:
                    break
        return move_able


class LJump(MovementPattern):

    def return_positions(self, piece, board):
        '''
        :param piece:
        :param board:
        :return: Possible Movements
        '''
        moves = [(1, self.max_distance),(self.max_distance ,1)]
        move_able = []
        cur_row, cur_col = board.get_piece_pos(piece)
        # Refer to get_direction_of for understanding of the algorithm below
        for quadrant in range(self.quadrant_corners):
            x_dir, y_dir = self.get_direction_of(quadrant, self.X_index), self.get_direction_of(quadrant, self.Y_index)
            for move in moves:
                new_row, new_col = cur_row + move[self.X_index]*x_dir, cur_col + move[self.Y_index]*y_dir
                if self.is_movable(board, piece, new_row, new_col):
                    move_able.append([new_col, new_row])
        return move_able


class Vertical(MovementPattern):

    def return_positions(self, piece, board):
        '''
        :param piece:
        :param board:
        :return: Possible Movements
        '''
        move_able = []
        cur_row, cur_col = board.get_piece_pos(piece)
        # Refer to get_direction_of for understanding of the algorithm below
        for quadrant in range(self.quadrant_corners):
            y_dir = self.get_direction_of(quadrant, self.Y_index)
            for distance in range(1, self.max_distance + 1):
                new_row = cur_row + distance * y_dir
                if self.is_movable(board, piece, new_row, cur_col):
                    if piece.get_piece_name() == Pieces.Pawn().get_class_name():
                        # To be added
                        piece_color = piece.get_color()
                        colors = board.get_default_piece_colors()
                        index_of = int(str(colors.index(piece_color)).replace("0", "-1"))

                    move_able.append([cur_col, new_row])
                    if board.get_space(*move_able[-1][::-1]):
                        break
                else:
                    break
        return move_able






