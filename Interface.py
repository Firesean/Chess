from tkinter import *
from PIL import Image, ImageTk

class Interface:
    background_image = Image.open(r"darkWood.png")
    board_tag = "board_tag"
    canvas = None
    contrast_color = "gray50"
    current_moves = []
    interface_start_pos = 2
    movement_tag = "movement"
    piece_tag = "piece"
    reference = []
    selected = None


    def __init__(self, game, window_size, root=Tk()):
        # Root
        self.root = root
        # Declarations

        self.game = game
        self.icon_ref = "chessPicture.ICO"
        self.window_size = window_size


        # Main
        self.background_image = self.background_image.resize((self.window_size, self.window_size), Image.ANTIALIAS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.create_interface()
        self.set_binds()
        self.root.mainloop()

    @staticmethod
    def calculate_board_pos(pos, spacer, offset):
        return int(((pos - offset) / spacer)+.5)

    @staticmethod
    def calculate_interface_pos(index, spacer, offset):
        return index * spacer + offset

    def display_clear_movable(self):
        for move in self.current_moves:
            self.canvas.delete(move)
        self.current_moves = []

    def controller(self, event):
        if self.selected:
            # if self.selected.get_color() == self.game.get_current_player():
            self.move_piece(event)
            # else:
            #     self.selected = None
            #     self.clear_movable()
        else:
            self.select_piece(event)

    def create_interface(self):
        self.draw_board()
        self.draw_pieces()
        self.root.title(type(self.game).__name__)
        self.root.iconbitmap(self.icon_ref)

    def display_moves(self, piece):
        '''
        :param piece:
        Goes through the pieces pattern's to show movable locations
        Displays the movable locations
        '''
        move_able = []
        try:
            if piece.patterns:
                if isinstance(piece.patterns, tuple or list):
                    for pattern in piece.patterns:
                        move = pattern.return_positions(piece, self.game)
                        move_able += move
                else:
                    move_able = piece.patterns.return_positions(piece, self.game)
            for move in move_able:
                row, col = move
                x, y = self.get_xy_with_col_row(col, row)
                offset = self.get_offset()

                self.current_moves.append(self.canvas.create_rectangle(x-offset,
                                                                       y-offset,
                                                                       x+offset,
                                                                       y+offset,
                                                                       fill=self.game.get_default_movement_color(),
                                                                       stipple=self.contrast_color))

            self.canvas.lift(self.piece_tag)
            self.game.set_move_able(move_able)
        except AttributeError:
            print("No Patterns")

    def draw_board(self):
        '''
        Draws the design structure of the board as a grid and borders and *colors needed parts
        '''
        self.canvas = Canvas(self.root, height=self.window_size, width=self.window_size)
        self.canvas.create_image(0, 0, anchor=NW, image=self.background_photo)
        board_size = self.game.get_board_size()
        spacer = self.get_spacer()
        self.root.geometry("{0}x{0}".format(self.window_size+spacer))
        for line in range(board_size):

            self.canvas.create_line(self.interface_start_pos,
                                    line * spacer,
                                    self.window_size,
                                    line * spacer,
                                    tags=self.board_tag)

            self.canvas.create_line(line * spacer,
                                    self.interface_start_pos,
                                    line * spacer,
                                    self.window_size,
                                    tags=self.board_tag)

        self.canvas.create_rectangle(self.interface_start_pos,
                                     self.interface_start_pos,
                                     self.window_size,
                                     self.window_size,
                                     tags=self.board_tag)

        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)  # Centers the canvas in Root Window
        self.draw_squares()
        # Place an outline around board

    def draw_pieces(self):
        '''
        Draws pieces onto the board
        '''
        board = self.game.get_board()
        spacer = self.get_spacer()
        offset = self.get_offset()
        for row in board:
            for piece in row:
                if piece:
                    row, col = self.game.get_piece_pos(piece)
                    self.reference.append(self.canvas.create_text(self.calculate_interface_pos(col, spacer, offset),
                                                                  self.calculate_interface_pos(row, spacer, offset),
                                                                  text=piece.get_unicode(),
                                                                  font="TimesNewRoman {}".format(offset),
                                                                  tags=self.piece_tag,
                                                                  fill=piece.get_color()))
                    piece.set_interface_ref(self.reference[-1])

    def draw_squares(self):
        board_size = self.game.get_board_size()
        offset = self.get_offset()
        colors = self.game.get_default_board_colors()
        for row in range(board_size):
            for col in range(board_size):
                x, y = self.get_xy_with_col_row(col, row)
                color = colors[0]
                if row % 2 == col % 2:
                    color = colors[1]

                self.canvas.create_rectangle(x - offset,
                                             y - offset,
                                             x + offset,
                                             y + offset,
                                             fill=color,
                                             tags=self.board_tag,
                                             stipple=self.contrast_color)

    def get_offset(self):
        return int(self.get_spacer() / 2)

    def get_col_row_with_xy(self, x, y):
        spacer = self.get_spacer()
        offset = self.get_offset()
        return self.calculate_board_pos(x, spacer, offset), self.calculate_board_pos(y, spacer, offset)

    def get_spacer(self):
        return int(self.window_size / self.game.get_board_size())

    def get_xy_with_col_row(self, col, row):
        spacer = self.get_spacer()
        offset = self.get_offset()
        x, y = self.calculate_interface_pos(col, spacer, offset), self.calculate_interface_pos(row, spacer, offset)
        return x, y

    def movable_position(self, piece, row, col):
        position = self.game.get_space(row, col)
        if position and piece.get_color() == position.get_color():
            return False
        if not self.game.is_on_board(row, col):
            return False
        return True

    def move_piece(self, event=None):
        '''
        :param event:
        Checks if pieces can move and will move to selected position
        '''
        if event:
            self.display_clear_movable()
            col, row = self.get_col_row_with_xy(event.x, event.y)
            if not [row, col] in self.game.get_move_able(): # Not a move able position
                self.selected = None
                return
            if self.movable_position(self.selected, row, col):
                location = self.game.get_space(row, col)
                x, y = self.get_xy_with_col_row(col, row) # Centers the position on the board
                self.canvas.coords(self.selected.get_interface_ref(), x, y)
                if location:
                    self.canvas.delete(location.get_interface_ref())
                self.game.move_piece_on_board(self.selected, row, col)
            self.selected = None

    def select_piece(self, event=None):
        if event:
            x, y = event.x, event.y
            offset = self.get_offset()
            if x < offset or y < offset:
                return
            col, row = self.get_col_row_with_xy(x, y)
            self.selected = self.game.get_space(row, col)
            if self.selected:
                self.display_moves(self.selected)

    def set_binds(self):
        self.root.bind("<Button-1>", lambda event: self.controller(event))






