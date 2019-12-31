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
        self.selected = None
        self.window_size = window_size  # (X, Y)

        # Main
        self.root.iconbitmap(self.icon_ref)
        self.draw_board()
        self.draw_pieces()
        self.set_binds()
        self.root.title(type(game).__name__)
        self.root.mainloop()

    @staticmethod
    def calculate_row_col(pos, spacer, offset):
        return int(((pos - offset) / spacer)+.5)

    @staticmethod
    def calculate_xy(index, spacer, offset):
        return index * spacer + offset

    def controller(self, event):
        if self.selected:
            self.move_piece(event)
        else:
            self.select_piece(event)

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
                    self.reference.append(self.canvas.create_text(self.calculate_xy(col_index, spacer, offset),
                                                                  self.calculate_xy(row_index, spacer, offset),
                                                                  text=piece.get_image(),
                                                                  font="TimesNewRoman {}".format(offset)))
                    piece.set_interface_ref(self.reference[len(self.reference)-1])

    def get_offset(self):
        return int(self.get_spacer() / 2)

    def get_row_col_with_xy(self, x, y):
        spacer = self.get_spacer()
        offset = self.get_offset()
        return self.calculate_row_col(x, spacer, offset), self.calculate_row_col(y, spacer, offset)

    def get_spacer(self):
        return int(self.window_size / self.game.get_board_size())

    def get_xy_with_col_row(self, col, row):
        spacer = self.get_spacer()
        offset = self.get_offset()
        return self.calculate_xy(col, spacer, offset), self.calculate_xy(row, spacer, offset)

    def move_piece(self, event=None):
        if self.selected:
            spacer = self.get_offset()
            row, col = self.get_row_col_with_xy(event.y, event.x)
            x, y = self.get_xy_with_col_row(col, row)
            piece = self.game.get_space(col, row)
            if piece and self.selected.get_color() == piece.get_color():
                return
            elif piece:
                self.canvas.delete(piece.get_interface_ref())
            self.canvas.coords(self.selected.get_interface_ref(),
                               x, y)
            self.game.move_piece(self.selected, row, col)
            self.selected = None

    def select_piece(self, event=None):
        if event:
            x, y = event.x, event.y
            col, row = self.get_row_col_with_xy(x, y)
            self.selected = self.game.get_space(col, row)
            # self.reveal_movable(self.selected)

    def set_binds(self):
        self.root.bind("<Button-1>", lambda event: self.controller(event))





