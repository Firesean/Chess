class MovementPattern:
    X_index = 0
    Y_index = 1

    def __init__(self, direction=2, distance=7):
        self.distance = distance
        self.direction = direction

    @staticmethod
    def get_direction_of(given, requested):
        '''
        :param given:
        :param requested:
        :return: Returns direction as a translated binary, 0 being -1 and 1 positive
        '''
        given = bin(given + 1)[-2:].replace("b", "0")
        return int(str(given[requested]).replace("0", "-1"))

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
        for corner in range(self.direction):
            x_dir, y_dir = self.get_direction_of(corner, self.X_index), self.get_direction_of(corner, self.Y_index)
            for i in range(1, self.distance+1):
                new_row, new_col = cur_row+i*x_dir, cur_col+i*y_dir
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
        for corner in range(self.direction):
            x_dir = self.get_direction_of(corner, self.X_index)
            for i in range(1, self.distance+1):
                new_col = cur_col+i*x_dir
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
        moves = [(1, 3), (3, 1), (-1, 3), (3, -1), (1, -3), (-3, 1), (-3, -1), (-1, -3)]
        move_able = []
        cur_row, cur_col = board.get_piece_pos(piece)
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
        for corner in range(self.direction):
            y_dir = self.get_direction_of(corner, self.Y_index)
            for i in range(1, self.distance+1):
                new_row = cur_row+i*y_dir
                if self.is_movable(board, piece, new_row, cur_col):
                    move_able.append([cur_col, new_row])
                    if board.get_space(*move_able[-1][::-1]):
                        break
                else:
                    break
        return move_able



