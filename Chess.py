# import Players

from Pieces import *
# https://en.wikipedia.org/wiki/Chess_symbols_in_Unicode


class Chess:
    '''
    Chess game, Two Colors and Players, Default information such as Piece Positioning, Board size and color are located here.
    '''
    default_colors = ["White", "Black"]
    default_board_size = 8
    default_board_state = ([Pawn(Piece.piece_types[0])] + \
                          [Rook(Piece.piece_types[3]), Knight(Piece.piece_types[1]),
                           Bishop(Piece.piece_types[2]), Queen(Piece.piece_types[4]),
                           King(Piece.piece_types[5]), Bishop(Piece.piece_types[2]),
                           Knight(Piece.piece_types[1]), Rook(Piece.piece_types[3])])

    def __init__(self, board_size=default_board_size):
        '''
        :param board_size:
        Generates the full game
        '''
        # Declarations
        self.board_size = board_size
        self.board = []
        self.players = []
        # Main
        self.new_board()
        self.set_pieces()
        self.selected_piece = None

    def get_board(self):
        '''
        :return: Board
        '''
        return self.board

    def get_board_size(self):
        '''
        :return: Size of board
        '''
        return self.board_size

    def get_space(self, row, col):
        '''
        :param row:
        :param col:
        :return: Position on board, Piece Class or None
        '''
        return self.board[row][col]

    def new_board(self):
        '''
        :return: None
        Sets board to empty to then continue to generate a new board
        '''
        self.board = []
        for row in range(self.board_size):
            self.board.append([None])
            self.board[row] *= self.board_size

    def print_board(self):
        '''
        :return: None
        For Debugging usages / Testing
        Displays a console prompt board state
        '''
        for row in self.board:
            for piece in row:
                if not piece:
                    print(u"\u0011", end=" ")
                    continue
                print(Piece.pieces[piece.get_image_path()], end=" ")
            print("\n")

    def set_pieces(self):
        '''
        :return: None
        Creates new pieces and sets colors/position for piece
        '''
        for start, end, side, color in [[1, -1, -1, self.default_colors[0]],
                                        [self.board_size-2, self.board_size, 1, self.default_colors[1]]]:  # 2 Iterations O(2^1)
            for row in range(start, end, side):  # 2 Rows Iterations O(4^2)
                for col in range(self.board_size):  # Col Iterations O(4*N^3) O("32"^3)
                    piece = self.default_board_state[col + 1].get_piece_type()
                    if row == start:
                        piece = self.default_board_state[0].get_piece_type()
                    new_piece = eval("{0}({1},{2})".format(piece, row, col))
                    if row == start:

                        self.board[row][col] = new_piece  # Sets pawns
                    else:

                        self.board[row][col] = new_piece  # Sets pieces by positioning in board state
                    self.get_space(row, col).set_color(color)

