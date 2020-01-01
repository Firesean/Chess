from enum import Enum


class MovementType(Enum):
    CONDITIONAL = 0
    RANGE = 1
    SET = 2


class MovementPattern:
    # Range between numbers,
    # Set no matter what it has to move a certain amount,
    # conditional like castling and En Passant

    def __init__(self, distance=8):
        self.distance = distance


class Diagonal(MovementPattern):

    def return_positions(self, piece, board):
        '''
        :param piece:
        :param board:
        :return: Possible Movements
        '''
        move_able = []
        old_row, old_col = board.get_piece_pos(piece)
        for corner in range(4):
            corner = bin(corner+1)[-2:].replace("b", "0")
            x_dir, y_dir = int(str(corner[0]).replace("0", "-1")), int(str(corner[1]).replace("0", "-1"))
            for i in range(1, self.distance):
                new_row, new_col = old_row+i*x_dir, old_col+i*y_dir
                space = board.get_space(new_row, new_col)
                if new_row < 0 or new_col < 0:  # Off Board
                    continue
                elif space and space.get_color() == piece.get_color():  # Runs into same colored piece
                    break
                elif space:  # Runs into piece
                    move_able.append([new_col, new_row])
                    break
                else:  # Other
                    move_able.append([new_col, new_row])
        return move_able


class Horizontal(MovementPattern):

    def return_positions(self, piece, board):
        '''
        :param piece:
        :param board:
        :return: Possible Movements
        '''
        move_able = []
        old_row, cur_col = board.get_piece_pos(piece)
        for corner in range(2):
            corner = bin(corner+1)[-2:].replace("b", "0")
            x_dir = int(str(corner[0]).replace("0", "-1"))
            for i in range(1, self.distance):
                new_col = cur_col+i*x_dir
                space = board.get_space(old_row, new_col)
                if new_col < 0:  # Off Board
                    continue
                elif space and space.get_color() == piece.get_color():  # Runs into same colored piece
                    break
                elif space:  # Runs into piece
                    move_able.append([new_col, old_row])
                    break
                else:  # Other
                    move_able.append([new_col, old_row])
        return move_able


class LJump(MovementPattern):
    '''
    :param piece:
    :param board:
    :return: Possible Movements
    '''
    def return_positions(self, piece, board):
        moves = [(1, 3), (3, 1), (-1, 3), (3, -1), (1, -3), (-3, 1), (-3, -1), (-1, -3)]
        move_able = []
        row, col = board.get_piece_pos(piece)
        return move_able


class Vertical(MovementPattern):

    def return_positions(self, piece, board):
        '''
        :param piece:
        :param board:
        :return: Possible Movements
        '''
        move_able = []
        old_row, cur_col = board.get_piece_pos(piece)
        for corner in range(2):
            corner = bin(corner+1)[-2:].replace("b", "0")
            y_dir = int(str(corner[1]).replace("0", "-1"))
            for i in range(1, self.distance):
                new_row = old_row+i*y_dir
                space = board.get_space(new_row, cur_col)
                if new_row < 0:  # Off Board
                    continue
                elif space and space.get_color() == piece.get_color():  # Runs into same colored piece
                    break
                elif space:  # Runs into piece
                    move_able.append([cur_col, new_row])
                    break
                else:  # Other
                    move_able.append([cur_col, new_row])
        return move_able



