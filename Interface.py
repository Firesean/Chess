import tkinter as tk


class Interface:

    def __init__(self, game, window_size, root=tk.Tk()):
        # Root
        self.root = root

        # Declarations
        self.canvas = None
        self.reference = []
        self.game = game
        self.icon_ref = "chessPicture.ICO"
        self.window_size = window_size  # (X, Y)

        # Main
        self.root.iconbitmap(self.icon_ref)
        self.draw_board()
        self.draw_pieces()
        self.root.title(type(game).__name__)
        self.root.mainloop()

    @staticmethod
    def calculate_row_col(pos, spacer, offset):
        return int((pos - offset) / spacer)

    @staticmethod
    def calculate_xy(index, spacer, offset):
        return index * spacer + offset

    def draw_board(self):
        '''
        :param game:
        :param window_size:
        Draws the outline of the board
        :return: None
        '''
        self.canvas = tk.Canvas(height=self.window_size, width=self.window_size)
        board_size = self.game.get_board_size()
        spacer = self.get_spacer()
        self.root.geometry("{0}x{0}".format(self.window_size+spacer))
        for line in range(board_size):
            self.canvas.create_line(2, line * spacer, self.window_size, line * spacer)
            self.canvas.create_line(line * spacer, 2, line * spacer, self.window_size)
        self.canvas.create_rectangle(2, 2, self.window_size, self.window_size)
        self.canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Centers the canvas in Root Window
        # Place an outline around board

    def draw_pieces(self):
        '''
        :param game:
        :param window_size:
        Draws the pieces onto the board
        Adds pieces to reference to later move pieces on the interface
        :return: None
        '''

        board = self.game.get_board()
        spacer = self.get_spacer()
        offset = self.get_offset()
        for col in board:
            for piece in col:
                if piece:
                    col_index = board.index(col)
                    row_index = col.index(piece)
                    self.reference.append(self.canvas.create_text(self.calculate_xy(row_index, spacer, offset),
                                                                  self.calculate_xy(col_index, spacer, offset),
                                                                  text=piece.get_image(),
                                                                  font="TimesNewRoman {}".format(offset)))

    def get_offset(self):
        return int(self.get_spacer() / 2)

    def get_row_col_with_xy(self, x, y):
        spacer = self.get_spacer()
        offset = self.get_offset()
        return self.calculate_row_col(x, spacer, offset), self.calculate_row_col(y, spacer, offset)

    def get_spacer(self):
        return int(self.window_size / self.game.get_board_size())

    def get_xy_with_row_col(self, row, col):
        spacer = self.get_spacer()
        offset = self.get_offset()
        return self.calculate_xy(row, spacer, offset), self.calculate_xy(col, spacer, offset)

    def select_piece(self, event=None):
        pass




