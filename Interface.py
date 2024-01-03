from tkinter import * # User Interface
from PIL import ImageTk # Image Manipulation
import MovementPattern as Pattern
import Pieces as Piece
from ImageManager import *
from ImageManager import ImageManager as IM

class Interface:
    # Constants
    BOARD_TAG = "board_tag" # Used order canvas items
    BORDER_SIZE = 0
    CONTRAST_COLOR = "gray50" # Used for transparency usage
    FONT_PATTERN = "comicsansms {}"
    INTERFACE_START_POS = 2
    MOVEMENT_TAG = "movement" # Used order canvas items
    PIXELS_DROPPED = -12 # Pixels to the bottom
    PIXELS_SLID = 0 # Pixels to the left
    PIECE_TAG = "piece" # Used order canvas items
    PROMOTIONS = ["Knight", "Bishop", "Rook", "Queen"]

    # Changeable
    background_image = Image.open(f"{CDIRECTORY}" + r"images/darkWood.png")
    canvas = None
    image_object = None
    is_pawn_promotion = False
    menu_bar = None
    moves_displayed = []
    piece_indicator = None
    player_indicator_display = None
    references = []
    selected = None
    show_moves = True


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
        self.enable_binds()
        self.root.mainloop()

    @staticmethod
    def calculate_board_pos(pos, spacer, offset=0): # Returns the position on the game board
        return int(((pos - offset) / spacer)+.5)

    @staticmethod
    def calculate_interface_pos(index, spacer, offset=0): # Returns the position on the interface
        return index * spacer + offset

    def check(self, event):
        if event:
            opp = self.game.PM.get_next_player()
            pieces_opp = opp.get_pieces()
            user = self.game.PM.get_current_player()
            pieces_user = user.get_pieces()
            user_king = [p for p in pieces_user if p.get_piece_name() == Piece.King().get_piece_name() and p.get_color() == user.get_color()]
            king_location = self.game.get_piece_pos(*user_king)
            movable = []
            for p in pieces_opp:
                try:
                    for pat in p.patterns:
                        movable += pat.return_positions(p, self.game)
                except TypeError:
                    try:
                        movable += p.patterns.return_positions(p, self.game)
                    except AttributeError as e:
                        print(e)

            movable = sorted(list(set(map(tuple, movable))))
            print("Movable Spaces : " ,movable)
            print("King's Location : ", king_location)
            print("King Location is Movable : ", king_location in movable)

    def check_enpassant(self):
        last_move = self.game.get_last_move_made()
        if Pattern.EnPassant().get_pattern_name() in last_move.get_pattern_used():
            self.canvas.delete(last_move.get_captured().get_interface_ref())

    def choose_promotion(self, event):
        col, row = self.get_col_row_with_xy(event.x, event.y)
        start_point = int(self.game.get_board_size() / 2 - 1)
        end_point = start_point + 1
        if (col, row).count(start_point) + (col, row).count(end_point) == 2:
            col -= start_point  # 1 or 0
            row -= start_point  # 1 or 0
            index = end_point - (row * 2 + col)
            piece = self.game.create_piece(self.PROMOTIONS[-index])
            row, col = self.game.get_piece_pos(self.selected)
            self.canvas.delete(self.selected.get_interface_ref())
            self.game.set_piece(piece, row, col, self.selected.get_color())
            for count in range(6):  # 6 is items added for canvas object
                self.canvas.delete(self.references.pop())
            self.draw_piece(row, col, piece)
        else:
            return
        self.selected = None
        self.is_pawn_promotion = False

    def controller(self, event):
        if self.is_pawn_promotion:
            self.choose_promotion(event)
        elif self.selected:
            self.display_clear_movable()
            self.de_indicate_piece(self.selected)
            if self.selected.get_color() == self.game.PM.get_current_color():
                self.move_piece(event)
            if not self.is_pawn_promotion:
                self.selected = None
        else:
            self.select_piece(event)

    def create_interface(self):
        self.draw_board()
        self.draw_squares()
        self.draw_pieces()
        indicator_size = self.get_offset() / 2
        self.player_indicator_display = self.canvas.create_rectangle(0, 0, indicator_size, indicator_size,
                                                                     fill=self.game.PM.get_current_color())
        self.root.resizable(width=False, height=False)
        self.root.title(type(self.game).__name__)
        self.root.iconbitmap(self.icon_ref)
        self.create_menu()

    def create_menu(self):
        self.menu_bar = Menu(self.root)

        background_menu = Menu(self.menu_bar, tearoff=0)
        for image_path in IM.get_background_paths(): # Loops through the image paths
            label = IM.get_image_name(image_path)
            background_menu.add_radiobutton(label=f"{label}", command=lambda path=image_path: self.set_background(path))

        display_menu = Menu(self.menu_bar, tearoff=0)
        display_menu.add_radiobutton(label="Show Moves", command=lambda : self.set_show_moves(True))
        display_menu.add_radiobutton(label="Hide Moves", command=lambda : self.set_show_moves(False))

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
        self.canvas.move(ref, -1 * self.PIXELS_SLID, -1 * self.PIXELS_DROPPED)
        self.canvas.delete(self.piece_indicator)

    def display_clear_movable(self): # Removes all canvas objects that display moves
        for move in self.moves_displayed:
            self.canvas.delete(move)
        self.moves_displayed = []

    def display_moves(self, piece):
        move_able = self.get_pattern_and_moves(piece)
        if not move_able: # Empty List
            self.selected = None
            return

        if not self.show_moves:
            return
        color = self.game.get_movement_color()
        for path in move_able:
            moves = move_able[path]
            for move in moves:
                row, col = move
                x, y = self.get_xy_with_col_row(col, row)
                offset = self.get_offset()
                self.moves_displayed.append(self.canvas.create_rectangle(x - offset, y - offset,
                                                                         x + offset, y + offset,
                                                                         fill=color,
                                                                         stipple=self.CONTRAST_COLOR))
            self.canvas.lift(self.PIECE_TAG)

    def draw_board(self):
        self.canvas = Canvas(self.root, height=self.window_size, width=self.window_size, bd=self.BORDER_SIZE)
        self.image_object = self.canvas.create_image(0, 0, anchor=NW, image=self.background_photo)
        board_size = self.game.get_board_size()
        spacer = self.get_spacer()
        self.root.geometry("{0}x{0}".format(self.window_size))

        for line in range(board_size):
            #  Rows
            self.canvas.create_line(self.INTERFACE_START_POS, line * spacer,
                                    self.window_size, line * spacer,
                                    tags=self.BOARD_TAG)

            # Columns
            self.canvas.create_line(line * spacer, self.INTERFACE_START_POS,
                                    line * spacer, self.window_size,
                                    tags=self.BOARD_TAG)

        # Border
        self.canvas.create_rectangle(self.INTERFACE_START_POS, self.INTERFACE_START_POS,
                                     self.window_size, self.window_size,
                                     tags=self.BOARD_TAG)

        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)  # Centers the canvas in Root Window

    def draw_pawn_promotion(self):
        spacer = self.get_spacer()
        offset = self.get_offset()
        sq_2 = spacer * 2
        sq_3 = spacer * 3
        colors = self.game.get_board_colors()
        outline_color = "black"
        half_window = self.window_size / 2
        # Design window
        self.references.append(self.canvas.create_polygon(half_window - sq_2, half_window - sq_2,
                                   half_window + sq_3, half_window - sq_2,
                                   half_window + sq_2, half_window + sq_2,
                                   half_window - sq_3, half_window + sq_2,
                                   fill=colors[0], outline=outline_color,
                                   width=3, stipple=self.CONTRAST_COLOR)) # Stipple is used for transparency

        self.references.append(self.canvas.create_polygon(half_window - sq_2 + offset, half_window - sq_2 + offset,
                                   half_window + sq_3 - offset, half_window - sq_2 + offset,
                                   half_window + sq_2 - offset, half_window + sq_2 - offset,
                                   half_window - sq_3 + offset, half_window + sq_2 - offset,
                                   fill=colors[1], outline=outline_color,
                                   width=3))
        # Draw Pieces
        self.draw_promotion_pieces(spacer, offset)

    def draw_piece(self, row, col, piece):
        spacer = self.get_spacer()
        offset = self.get_offset()
        self.references.append(self.canvas.create_text(self.calculate_interface_pos(col, spacer, offset),
                                                       self.calculate_interface_pos(row, spacer, offset),
                                                       text=piece.get_unicode(),
                                                       font=self.FONT_PATTERN.format(offset),
                                                       tags=self.PIECE_TAG,
                                                       fill=piece.get_color()))
        piece.set_interface_ref(self.references[-1])

    def draw_pieces(self):
        board = self.game.get_board()
        for row in board:
            for piece in row:
                if piece:
                    row, col = self.game.get_piece_pos(piece)
                    self.draw_piece(row, col, piece)

    def draw_promotion_pieces(self, spacer, offset):
        for piece in self.PROMOTIONS:
            index = self.PROMOTIONS.index(piece)
            row = int(self.game.get_board_size() / 2 - 1) + int(index / 2)
            col = int(self.game.get_board_size() / 2 - 1) +  index % 2
            self.references.append(self.canvas.create_text(self.calculate_interface_pos(col, spacer, offset),
                                                           self.calculate_interface_pos(row, spacer, offset),
                                                           text=Piece.Piece.pieces[piece],
                                                           font=self.FONT_PATTERN.format(offset),
                                                           tags=self.PIECE_TAG,
                                                           fill=self.game.PM.get_current_color()))

    def draw_squares(self):
        board_size = self.game.get_board_size()
        offset = self.get_offset()
        colors = self.game.get_board_colors()
        for row in range(board_size):
            for col in range(board_size):
                x, y = self.get_xy_with_col_row(col, row)
                color = colors[0]
                if row % 2 == col % 2: # Creates checkered Pattern
                    color = colors[1]

                self.canvas.create_rectangle(x - offset, y - offset,
                                             x + offset, y + offset,
                                             fill=color,
                                             tags=self.BOARD_TAG,
                                             stipple=self.CONTRAST_COLOR) # Stipple is used for transparency

    def enable_binds(self):
        self.root.bind("<Button-1>", lambda event: self.controller(event))
        self.root.bind("<Motion>", lambda event: self.player_indicator(event))
        self.root.bind("<a>", lambda event: self.check(event))

    def get_col_row_with_xy(self, x, y):
        spacer = self.get_spacer()
        offset = self.get_offset()
        return self.calculate_board_pos(x, spacer, offset), self.calculate_board_pos(y, spacer, offset)


    def get_offset(self):
        return int(self.get_spacer() / 2)

    def get_pattern_and_moves(self, piece):
        return self.game.get_pattern_and_moves(piece)

    def get_spacer(self):
        return int(self.window_size / self.game.get_board_size())

    def get_xy_with_col_row(self, col, row):
        spacer = self.get_spacer()
        offset = self.get_offset()
        x, y = self.calculate_interface_pos(col, spacer, offset), self.calculate_interface_pos(row, spacer, offset)
        return x, y

    def indicate_piece(self, piece):  # Adjusts piece to display a small shadow giving effect of piece being raised
        ref = piece.get_interface_ref()
        offset = self.get_offset() / 2
        x, y = self.canvas.coords(ref)
        self.piece_indicator = self.canvas.create_oval(x+offset,y+offset,
                                                       x-offset,y+offset + offset/self.game.get_board_size())
        self.canvas.move(ref, self.PIXELS_SLID, self.PIXELS_DROPPED)

    def interface_adjust_piece(self, row, col):
        x, y = self.get_xy_with_col_row(col, row)  # Centers the position on the board
        self.canvas.coords(self.selected.get_interface_ref(), x, y)

    def is_movable_position(self, piece, row, col):
        return self.game.is_movable_position(piece, row, col)

    def move_piece(self, event=None):
        if event:
            self.display_clear_movable()
            col, row = self.get_col_row_with_xy(event.x, event.y)
            pattern_name = self.game.get_move_pattern([row, col], self.game.get_move_able()) # If Any positions are possible
            if self.is_movable_position(self.selected, row, col) and pattern_name: # Determines if possible Moves and a piece
                location = self.game.get_space(row, col)
                self.interface_adjust_piece(row, col)
                if location:
                    self.canvas.delete(location.get_interface_ref())
                self.game.move_piece_on_board(self.selected, pattern_name, row, col, location)
                if self.game.check_pawn_promotion():
                    self.draw_pawn_promotion()
                    self.is_pawn_promotion = True
                self.check_enpassant() # Removes pawn's canvas object that got enpassant
                self.game.PM.switch_current_player() # Switch player in game
                self.switch_player() # Switch player indicator

    def player_indicator(self, event=None): # Indicator that follows the mouse
        size = self.get_offset() / 2
        offset = self.get_offset() / 4
        x_pos, y_pos = event.x + offset, event.y + offset
        self.canvas.coords(self.player_indicator_display, x_pos, y_pos, x_pos + size, y_pos + size)

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

    def set_background(self, image_path):
        self.background_image = IM.open_image(image_path)
        self.background_image = self.background_image.resize((self.window_size, self.window_size), Image.ANTIALIAS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.canvas.itemconfig(self.image_object, image=self.background_photo)

    def set_show_moves(self, boolean):
        self.show_moves = boolean

    def switch_player(self):
        self.canvas.itemconfigure(self.player_indicator_display, fill=self.game.PM.get_current_color())
