import tkinter as tk


class Interface:

    def __init__(self, board, window_size, root=tk.Tk()):
        self.root = root
        self.board = board
        self.window_size = window_size  # (X, Y)

    def draw_board(self):
        pass


