from tkinter import * # User Interface
from PIL import Image, ImageTk # Image Manipulation
import MovementPattern as Pattern
import os

CDIRECTORY = os.getcwd() + "\\"

class Interface:
    background_image = Image.open(f"{CDIRECTORY}" + r"images/darkWood.png")
    board_tag = "board_tag" # Used order canvas items
    border_size = 0
    canvas = None
    contrast_color = "gray50" # Used for transparency usage
    image_object = None
    indicator_display = None
    interface_start_pos = 2
    menu_bar = None
    movement_tag = "movement" # Used order canvas items
    moves_displayed = []
    pixels_dropped = -12 # Pixels to the bottom
    pixels_slided = 0 # Pixels to the left
    piece_indicator = None
    piece_tag = "piece" # Used order canvas items
    references = []
    selected = None


    def __init__(self, game, window_size, root=Tk()):
        # Root
        self.root = root
        # Declarations
        self.game = game
        self.icon_ref = "images/chessicon.ICO"
        self.window_size = window_size
        # Main
        self.background_image = self.background_image.resize((self.window_size, self.window_size), Image.ANTIALIAS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.create_interface()
        self.set_binds()
        self.root.mainloop()

    @staticmethod
    def calculate_board_pos(pos, spacer, offset): # Returns the position on the game board
        return int(((pos - offset) / spacer)+.5)

    @staticmethod
    def calculate_interface_pos(index, spacer, offset): # Returns the position on the interface
        return index * spacer + offset

    def check_enpassant(self):
        last_move = self.game.get_last_move_made()
        # Checks for EnPassant
        if Pattern.EnPassant().get_pattern_name() in last_move.get_pattern_used():
            self.canvas.delete(last_move.get_captured().get_interface_ref())

    def controller(self, event):
        if self.selected:
            self.de_indicate_piece(self.selected)
            if self.selected.get_color() == self.game.get_current_color():
                # Attempts to move piece based on position on canvas clicked
                self.move_piece(event)
            else:
                self.selected = None
                self.display_clear_movable()
        else:
            self.select_piece(event)

    def create_interface(self):
        self.draw_board()
        self.draw_pieces()
        indicator_size = self.get_offset() / 2
        self.indicator_display = self.canvas.create_rectangle(0,0, indicator_size, indicator_size,
                                                              fill=self.game.get_current_color())
        self.root.resizable(width=False, height=False)
        self.root.title(type(self.game).__name__)
        self.root.iconbitmap(self.icon_ref)
        self.create_menu()

    def create_menu(self):
        self.menu_bar = Menu(self.root)

        background_menu = Menu(self.menu_bar, tearoff=0)
        for image_path in self.get_background_paths(): # Loops through the images/ directory
            # Filter the image for a name
            label = self.get_image_name(image_path)

            background_menu.add_radiobutton(label=f"{label}", command=lambda path=image_path: self.set_background(path))

        display_menu = Menu(self.menu_bar, tearoff=0) # , fg="white", background = "black"
        display_menu.add_radiobutton(label="Show Moves")
        display_menu.add_radiobutton(label="Hide Moves")

        players_menu = Menu(self.menu_bar, tearoff=0)
        players_menu.add_radiobutton(label="Single")
        players_menu.add_radiobutton(label="Multi-player")

        self.menu_bar.add_cascade(label="Backgrounds", menu=background_menu)
        self.menu_bar.add_cascade(label="Players", menu=players_menu)
        self.menu_bar.add_cascade(label="Display Moves", menu=display_menu)
        self.menu_bar.add_command(label="Quit Game", command=lambda: quit())



        self.root.config(menu=self.menu_bar)


    def de_indicate_piece(self, piece): # Adjusts piece back to center of it's square
        ref = piece.get_interface_ref()
        self.canvas.move(ref, -1*self.pixels_slided, -1*self.pixels_dropped)
        self.canvas.delete(self.piece_indicator)

    def display_clear_movable(self): # Removes all canvas objects that display moves
        for move in self.moves_displayed:
            self.canvas.delete(move)
        self.moves_displayed = []

    def display_moves(self, piece):
        '''
        :param piece:
        Goes through the pieces pattern's to show movable locations
        Displays the movable locations
        '''
        move_able = self.get_pattern_and_moves(piece)
        if not move_able: # Empty List
            self.selected = None
            return
        color = self.game.get_default_movement_color()
        # color = "cyan"
        for path in move_able:
            moves = move_able[path]
            for move in moves:
                row, col = move
                x, y = self.get_xy_with_col_row(col, row)
                offset = self.get_offset()
                self.moves_displayed.append(self.canvas.create_rectangle(x-offset,
                                                                        y-offset,
                                                                        x+offset,
                                                                        y+offset,
                                                                        fill=color,
                                                                        stipple=self.contrast_color))
            self.canvas.lift(self.piece_tag)

    def draw_board(self):
        '''
        Draws the design structure of the board as a grid and borders and *colors needed parts
        '''
        self.canvas = Canvas(self.root, height=self.window_size, width=self.window_size, bd=self.border_size)
        self.image_object = self.canvas.create_image(0, 0, anchor=NW, image=self.background_photo)
        board_size = self.game.get_board_size()
        spacer = self.get_spacer()
        self.root.geometry("{0}x{0}".format(self.window_size))

        for line in range(board_size):
            #  Rows
            self.canvas.create_line(self.interface_start_pos,
                                    line * spacer,
                                    self.window_size,
                                    line * spacer,
                                    tags=self.board_tag)

            # Columns
            self.canvas.create_line(line * spacer,
                                    self.interface_start_pos,
                                    line * spacer,
                                    self.window_size,
                                    tags=self.board_tag)

        # Border
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
                    self.references.append(self.canvas.create_text(self.calculate_interface_pos(col, spacer, offset),
                                                                   self.calculate_interface_pos(row, spacer, offset),
                                                                   text=piece.get_unicode(),
                                                                   font="comicsansms {}".format(offset),
                                                                   tags=self.piece_tag,
                                                                   fill=piece.get_color()))
                    piece.set_interface_ref(self.references[-1])

    def draw_squares(self):
        board_size = self.game.get_board_size()
        offset = self.get_offset()
        colors = self.game.get_default_board_colors()
        for row in range(board_size):
            for col in range(board_size):
                x, y = self.get_xy_with_col_row(col, row)
                color = colors[0]

                if row % 2 == col % 2: # Creates checkered Pattern
                    color = colors[1]

                self.canvas.create_rectangle(x - offset,
                                             y - offset,
                                             x + offset,
                                             y + offset,
                                             fill=color,
                                             tags=self.board_tag,
                                             stipple=self.contrast_color)

    @staticmethod
    def get_background_paths(img_type =".png"):
        backgrounds = []
        for image in os.listdir(CDIRECTORY + "images"):
            if image.endswith(img_type):
                backgrounds.append(image)
        return backgrounds

    def get_col_row_with_xy(self, x, y):
        spacer = self.get_spacer()
        offset = self.get_offset()
        return self.calculate_board_pos(x, spacer, offset), self.calculate_board_pos(y, spacer, offset)

    @staticmethod
    def get_image_name(img_path):
        image = img_path.split(".")[0]  # Grabs everything before File type
        label = ""
        for ch in list(image):
            if ch.isupper():
                ch = " " + ch
            label += ch
        return label[0].upper() + label[1:]


    def get_pattern_and_moves(self, piece):
        return self.game.get_pattern_and_moves(piece)

    def get_movable_position(self, piece, row, col):
        return self.game.get_movable_position(piece, row, col)

    def get_offset(self):
        return int(self.get_spacer() / 2)

    def get_spacer(self):
        return int(self.window_size / self.game.get_board_size())

    def get_xy_with_col_row(self, col, row):
        spacer = self.get_spacer()
        offset = self.get_offset()
        x, y = self.calculate_interface_pos(col, spacer, offset), self.calculate_interface_pos(row, spacer, offset)
        return x, y

    def indicate_piece(self, piece):
        # Adjusts piece to display a small shadow giving effect of piece being raised
        ref = piece.get_interface_ref()
        offset = self.get_offset() / 2
        x, y = self.canvas.coords(ref)
        self.piece_indicator = self.canvas.create_oval(x+offset,y+offset,
                                                       x-offset,y+offset + offset/self.game.get_board_size())
        self.canvas.move(ref, self.pixels_slided, self.pixels_dropped)

    def interface_adjust_piece(self, row, col):
        x, y = self.get_xy_with_col_row(col, row)  # Centers the position on the board
        self.canvas.coords(self.selected.get_interface_ref(), x, y)

    def move_indicator(self, event=None): # Indicator that follows the mouse
        size = self.get_offset() / 2
        offset = self.get_offset() / 4
        x_pos, y_pos = event.x + offset, event.y + offset
        self.canvas.coords(self.indicator_display, x_pos, y_pos, x_pos+size, y_pos+size)

    def move_piece(self, event=None):
        '''
        :param event:
        Checks if pieces can move and will move to selected position
        '''
        if event:
            self.display_clear_movable()
            col, row = self.get_col_row_with_xy(event.x, event.y)
            # Determines if possible Moves
            # Deselects if none
            pattern_name = self.game.get_move_pattern([row, col], self.game.get_move_able()) # If Any positions are possible
            if not pattern_name:
                self.selected = None
                return

            if self.get_movable_position(self.selected, row, col):
                location = self.game.get_space(row, col)
                self.interface_adjust_piece(row, col)
                # Deletes piece if captured
                if location:
                    self.canvas.delete(location.get_interface_ref())
                # self.adjust_piece(self.selected) # Will modify to alter pieces that are kept track of if moved
                self.game.move_piece_on_board(self.selected, pattern_name, row, col, location)

                self.check_enpassant()
                self.game.switch_player()
                self.canvas.itemconfigure(self.indicator_display, fill=self.game.get_current_color())
            self.selected = None

    @staticmethod
    def open_image(image_path):
        return Image.open(f"{CDIRECTORY}"+ "images\\" + image_path)

    def select_piece(self, event=None):
        if event:
            x, y = event.x, event.y
            offset = self.get_offset()
            if x < offset or y < offset: # Makes sure you are on the board interface
                return
            col, row = self.get_col_row_with_xy(x, y)
            self.selected = self.game.get_space(row, col)
            if self.selected:
                self.display_moves(self.selected)
                self.indicate_piece(self.selected)

    def set_binds(self):
        self.root.bind("<Button-1>", lambda event: self.controller(event))
        self.root.bind("<Motion>", lambda event: self.move_indicator(event))

    def set_background(self, image_path):
        self.background_image = self.open_image(image_path)
        self.background_image = self.background_image.resize((self.window_size, self.window_size), Image.ANTIALIAS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.canvas.itemconfig(self.image_object, image=self.background_photo)






