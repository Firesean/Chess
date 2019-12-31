from enum import Enum


class MovementType(Enum):
    CONDITIONAL = 0
    RANGE = 1
    SET = 2


class MovementPattern:
    '''
    :param piece:
    :param board:
    :return: Possible Movements
    '''
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
        # cur_pos = (X,Y)
        # Fix algorithm to check from piece instead of through the piece
        x, y = board.get_piece_pos(piece)
        for index in range(-board.get_board_size(), board.get_board_size()):
            i, j = x+index, y+index
            move_able.append((i, j))
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



