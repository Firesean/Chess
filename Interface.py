import tkinter as tk


class Interface:

    def __init__(self, game, window_size, root=tk.Tk()):
        # Root
        self.root = root

        # Declarations
        self.canvas = None
        self.reference = []
        self.game = game
        self.window_size = window_size  # (X, Y)

        # Main
        self.draw_board(self.game, self.window_size)
        self.root.title(type(game).__name__)
        self.root.mainloop()

    def draw_board(self, game, window_size):
        '''
        :param game:
        :param window_size:
        Draws the outline of the board
        :return: None
        '''
        self.canvas = tk.Canvas(height=window_size, width=window_size)
        board_size = game.get_board_size()
        spacer = int(window_size / board_size)
        self.root.geometry("{0}x{0}".format(window_size+spacer))
        for line in range(board_size):
            self.canvas.create_line(0, line * spacer, window_size, line * spacer)
            self.canvas.create_line(line * spacer, 0, line * spacer, window_size)
        self.canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Centers the canvas in Root Window
        # Place an outline around board

    def draw_pieces(self, game, window_size):
        '''
        :param game:
        :param window_size:
        Draws the pieces onto the board
        Adds pieces to reference to later move pieces on the interface
        :return: None
        '''

        board = game.get_board()




