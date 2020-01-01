from enum import Enum


class MovementType(Enum):
    CONDITIONAL = 0
    RANGE = 1
    SET = 2


class MovementPattern:
    # Range between numbers,
    # Set no matter what it has to move a certain amount,
    # conditional like castling and En Passant

    def __init__(self, _type=MovementType.RANGE, distance=8):
        self.distance = distance
        self.type = _type


class Diagonal(MovementPattern):

    def return_positions(self, piece, board):
        '''
        :param piece:
        :param board:
        :return: Possible Movements
        '''
        move_able = []
        old_row, old_col = board.get_piece_pos(piece)
        for corner in range(1, 5):
            corner = bin(corner)
            corner = corner[-2:].replace("b", "0")
            x_dir, y_dir = int(str(corner[0]).replace("0", "-1")), int(str(corner[1]).replace("0", "-1"))
            print(x_dir, y_dir)
            for i in range(1, self.distance):
                new_row, new_col = old_row+i*x_dir, old_col+i*y_dir
                space = board.get_space(new_row, new_col)
                if new_row < 0 or new_col < 0:  # Off Board
                    print(1)
                    continue
                elif space and space.get_color() == piece.get_color():  # Runs into same colored piece
                    print(2)
                    break
                elif space:  # Runs into piece
                    print(3)
                    move_able.append((new_col, new_row))
                    break
                else:  # Other
                    move_able.append((new_col, new_row))
        return move_able


class Horizontal(MovementPattern):
    '''
    :param piece:
    :param board:
    :return: Possible Movements
    '''
    def return_positions(self, piece, board):
        move_able = []
        # cur_pos = (X,Y)
        # Fix algorithm to check from piece instead of through the piece
        x, y = board.get_piece_pos(piece)
        for index in range(-board.get_board_size(), board.get_board_size()):
            i, j = x+index, y
            move_able.append((i, j))
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
        x, y = board.get_piece_pos(piece)
        return move_able


class Vertical(MovementPattern):
    '''
    :param piece:
    :param board:
    :return: Possible Movements
    '''
    def return_positions(self, piece, board):
        move_able = []
        # cur_pos = (X,Y)
        # Fix algorithm to check from piece instead of through the piece
        x, y = board.get_piece_pos(piece)
        for index in range(-board.get_board_size(), board.get_board_size()):
            i, j = x, y+index
            move_able.append((i, j))
        return move_able



