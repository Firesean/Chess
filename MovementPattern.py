from enum import Enum


class MovementType(Enum):
    CONDITIONAL = 0
    RANGE = 1
    SET = 2


class MovementPattern:
    # Range between numbers,
    # Set no matter what it has to move a certain amount,
    # conditional like castling and En Passant

    def __init__(self, horizontal=0, vertical=0, diagonal=0, _type=MovementType.RANGE):
        self.diagonal = diagonal
        self.horizontal = horizontal
        self.type = _type
        self.vertical = vertical


class Diagonal(MovementPattern):

    def return_positions(self, piece, board):
        move_able = []
        # cur_pos = (X,Y)
        # Fix algorithm to check from piece instead of through the piece
        x, y = piece.get_pos()
        for distance in range(-self.diagonal, self.diagonal+1):
            if x + distance < 0 or x + distance > board.get_board_size():
                break
            if y + distance < 0 or y + distance > board.get_board_size():
                break

            if distance and not board.get_space(x+distance, y+distance):
                move_able.append((x+distance, y+distance))
            break
        return move_able


class Horizontal(MovementPattern):

    def return_positions(self, piece, board):
        move_able = []
        board = board.board
        # cur_pos = (X,Y)
        # Fix algorithm to check from piece instead of through the piece
        x, y = piece.get_pos()
        for distance in range(-self.horizontal, self.horizontal+1):
            if x + distance < 0 or x + distance > board.get_board_size():
                break
            if distance and not board.get_space(x+distance, y):
                move_able.append((x+distance, y))
            break
        return move_able


class LJump(MovementPattern):

    def return_positions(self, piece, board):
        moves = [(1, 3), (3, 1), (-1, 3), (3, -1), (1, -3), (-3, 1), (-3, -1), (-1, -3)]
        move_able = []
        x, y = piece.get_pos()
        for row, col in moves:
            try:
                if board.get.space(x+row, y+col):
                    continue
            except IndexError:
                continue
            move_able.append((x+row, y+col))
        return move_able


class Vertical(MovementPattern):

    def return_positions(self, piece, board):
        move_able = []
        # cur_pos = (X,Y)
        # Fix algorithm to check from piece instead of through the piece
        x, y = piece.get_pos()
        for distance in range(-self.vertical, self.vertical+1):
            if y + distance < 0 or y + distance > board.get_board_size():
                break
            if distance and not board.get_space(x, y+distance):
                move_able.append((x, y+distance))
            break
        return move_able



