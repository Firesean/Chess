# import Players
from Pieces import *
# https://en.wikipedia.org/wiki/Chess_symbols_in_Unicode


class Chess:
    '''
    Chess game, Two Colors and Players, Default information such as Piece Positioning, Board size and color are located here.
    '''
    default_colors = ["White", "Black"]
    board_size = 8
    default_board_state = ([Pawn().get_class_name()] + [Rook().get_class_name(), Knight().get_class_name(),
                           Bishop().get_class_name(), Queen().get_class_name(),
                           King().get_class_name(), Bishop().get_class_name(),
                           Knight().get_class_name(), Rook().get_class_name()])

    def __init__(self):
        '''
        :param board_size:
        Generates the full game
        '''
        # Declarations
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

    def get_piece_pos(self, piece):
        for i in range(len(self.board)):
            if piece in self.board[i]:
                return self.board[i].index(piece), i

    def get_space(self, col, row):
        '''
        :param row:
        :param col:
        :return: Position on board, Piece Class or None
        '''
        try:
            return self.board[col][row]
        except IndexError:
            return None

    def move_piece(self, piece, row, col):
        self.board[col][row] = piece

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
                    piece = self.default_board_state[col + 1]
                    if row == start:
                        piece = self.default_board_state[0]
                    new_piece = eval("{0}()".format(piece))
                    self.board[col][row] = new_piece
                    self.get_space(col, row).set_color(color)


