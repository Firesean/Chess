from enum import Enum


class MovementType(Enum):
    RANGE = 0
    SET = 1
    CONDITIONAL = 2


class MovementPattern:
    # Range between numbers,
    # Set no matter what it has to move a certain amount,
    # conditional like castling and En Passant
    
    def __init__(self, horizontal=0, vertical=0, diagonal=0, _type=MovementType.RANGE):
        self.horizontal = horizontal
        self.vertical = vertical
        self.diagonal = diagonal
        self.type = _type

    def return_position(self, row, col, diagonal):
        pass


class Vertical(MovementPattern):
    pass


class Horizontal(MovementPattern):
    pass


class Diagonal(MovementPattern):
    pass


class LJump(MovementPattern):
    pass


LJump(3,1,0,MovementPattern.types[1])
LJump(1,3,0,MovementPattern.types[1])
LJump(3,-1,0,MovementPattern.types[1])
LJump(-3,1,0,MovementPattern.types[1])
LJump(-3,-1,0,MovementPattern.types[1])

