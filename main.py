from tkinter import *
import tkinter as tk
import numpy as np
import math
from PIL import ImageTk, Image
from pieces import Piece

class CHESSBOARD:
    board= np.empty((8,8), dtype="<U10")
    x1, y1 = -1, -1
    br, bkn, bb, bq, bk, bp, wr, wkn, wb, wq, wk, wp = "", "", "", "", "", "", "", "", "", "", "", ""
    color1, color2, color3, color4, color5 = "#706677", "#ccb7ae", "#eefaac", "#4bc96c", "#9c1e37"
    rows, columns = 8, 8
    dim_square = 64
    top_offset, side_offset = 200, 100
    width = columns * dim_square + side_offset
    height = rows * dim_square + top_offset
    # note for heuristic
    # have a variable called board weight which holds the sum of all piece weights on the board?
    # may make heuristic calculations easier...
    piecesBoard = np.empty((8, 8), dtype=Piece)


    def __init__(self, parent):
        canvas_width = self.width
        canvas_height = self.height
        self.canvas = tk.Canvas(parent, width=canvas_width, height=canvas_height)
        self.canvas.pack(padx=8, pady=8)
        self.add_piece_objects()
        self.draw_board()
        self.pieces()
        self.init_dice()

    def draw_board(self):
        intCheck = 0
        for row in range(self.rows):
            intCheck += 1
            for col in range(self.columns):
                x1 = (col * self.dim_square) + 2
                y1 = (row * self.dim_square) + 100
                x2 = x1 + self.dim_square
                y2 = y1 + self.dim_square
                self.canvas.create_rectangle(x1, y1, x2, y2,
                                                fill=self.checkerboard_color(intCheck),
                                                tags="board")
                intCheck += 1
        print("White horse 1----------------------\n", self.piecesBoard[7, 1].check_moves(self.piecesBoard))

    def checkerboard_color(self, intCheck):
        if intCheck % 2 == 0:
            return self.color1
        else:
            return self.color2

    def add_piece_objects(self):
        self.piecesBoard[6, 0] = Piece("wp1", "p", -1, 1, [6, 0])
        self.piecesBoard[6, 1] = Piece("wp2", "p", -1, 1, [6, 1]) 
        self.piecesBoard[6, 2] = Piece("wp3", "p", -1, 1, [6, 2]) 
        self.piecesBoard[6, 3] = Piece("wp4", "p", -1, 2, [6, 3]) # white pawns
        self.piecesBoard[6, 4] = Piece("wp5", "p", -1, 2, [6, 4]) 
        self.piecesBoard[6, 5] = Piece("wp6", "p", -1, 3, [6, 5])
        self.piecesBoard[6, 6] = Piece("wp7", "p", -1, 3, [6, 6])
        self.piecesBoard[6, 7] = Piece("wp8", "p", -1, 3, [6, 7])

        self.piecesBoard[7, 0] = Piece("wr1", "r", -1, 2, [7, 0])
        self.piecesBoard[7, 7] = Piece("wr2", "r", -1, 2, [7, 7])
        self.piecesBoard[7, 1] = Piece("wh1", "h", -1, 1, [7, 1])
        self.piecesBoard[7, 6] = Piece("wh2", "h", -1, 3, [7, 6]) # white back row
        self.piecesBoard[7, 2] = Piece("wb1", "b", -1, 1, [7, 2]) 
        self.piecesBoard[7, 5] = Piece("wb2", "b", -1, 3, [7, 5])
        self.piecesBoard[7, 4] = Piece("wk1", "k", -1, 2, [7, 4])
        self.piecesBoard[7, 3] = Piece("wq1", "q", -1, 2, [7, 3])

        self.piecesBoard[1, 0] = Piece("bp1", "p", 1, 1, [1, 0])
        self.piecesBoard[1, 1] = Piece("bp2", "p", 1, 1, [1, 1])
        self.piecesBoard[1, 2] = Piece("bp3", "p", 1, 1, [1, 2])
        self.piecesBoard[1, 3] = Piece("bp4", "p", 1, 2, [1, 3]) # black pawns
        self.piecesBoard[1, 4] = Piece("bp5", "p", 1, 2, [1, 4])
        self.piecesBoard[1, 5] = Piece("bp6", "p", 1, 3, [1, 5])
        self.piecesBoard[1, 6] = Piece("bp7", "p", 1, 3, [1, 6])
        self.piecesBoard[1, 7] = Piece("bp8", "p", 1, 3, [1, 7])

        self.piecesBoard[0, 0] = Piece("br1", "r", 1, 2, [0, 0])
        self.piecesBoard[0, 7] = Piece("br2", "r", 1, 2, [0, 7])
        self.piecesBoard[0, 1] = Piece("bh1", "k", 1, 1, [0, 1])
        self.piecesBoard[0, 6] = Piece("bh2", "k", 1, 3, [0, 6]) # black back row
        self.piecesBoard[0, 2] = Piece("bb1", "b", 1, 1, [0, 2])
        self.piecesBoard[0, 5] = Piece("bb2", "b", 1, 3, [0, 5])
        self.piecesBoard[0, 4] = Piece("bk1", "k", 1, 2, [0, 4])
        self.piecesBoard[0, 3] = Piece("bq1", "q", 1, 2, [0, 3])

    def pieces(self):
        self.br = PhotoImage(file="./data/pieces/br.png")
        self.bh = PhotoImage(file="./data/pieces/bkn.png")
        self.bb = PhotoImage(file="./data/pieces/bb.png")
        self.bq = PhotoImage(file="./data/pieces/bq.png")
        self.bk = PhotoImage(file="./data/pieces/bk.png")
        self.bp = PhotoImage(file="./data/pieces/bp.png")
        self.wr = PhotoImage(file="./data/pieces/wr.png")
        self.wh = PhotoImage(file="./data/pieces/wkn.png")
        self.wb = PhotoImage(file="./data/pieces/wb.png")
        self.wq = PhotoImage(file="./data/pieces/wq.png")
        self.wk = PhotoImage(file="./data/pieces/wk.png")
        self.wp = PhotoImage(file="./data/pieces/wp.png")

        self.add_piece(self.br, self.piecesBoard[0][0].location, "br1")
        self.add_piece(self.br, self.piecesBoard[0][7].location, "br2")
        self.add_piece(self.bh, self.piecesBoard[0][1].location, "bh1")
        self.add_piece(self.bh, self.piecesBoard[0][6].location, "bh2")
        self.add_piece(self.bb, self.piecesBoard[0][2].location, "bb1")
        self.add_piece(self.bb, self.piecesBoard[0][5].location, "bb2")
        self.add_piece(self.bq, self.piecesBoard[0][3].location, "bq1")
        self.add_piece(self.bk, self.piecesBoard[0][4].location, "bk2")

        self.add_piece(self.bp, self.piecesBoard[1][0].location, "bp1")
        self.add_piece(self.bp, self.piecesBoard[1][1].location, "bp2")
        self.add_piece(self.bp, self.piecesBoard[1][2].location, "bp3")
        self.add_piece(self.bp, self.piecesBoard[1][3].location, "bp4")
        self.add_piece(self.bp, self.piecesBoard[1][4].location, "bp5")
        self.add_piece(self.bp, self.piecesBoard[1][5].location, "bp6")
        self.add_piece(self.bp, self.piecesBoard[1][6].location, "bp7")
        self.add_piece(self.bp, self.piecesBoard[1][7].location, "bp8")

        self.add_piece(self.wr, self.piecesBoard[7][0].location, "wr1")
        self.add_piece(self.wr, self.piecesBoard[7][7].location, "wr2")
        self.add_piece(self.wh, self.piecesBoard[7][1].location, "wh1")
        self.add_piece(self.wh, self.piecesBoard[7][6].location, "wh2")
        self.add_piece(self.wb, self.piecesBoard[7][2].location, "wb1")
        self.add_piece(self.wb, self.piecesBoard[7][5].location, "wb2")
        self.add_piece(self.wq, self.piecesBoard[7][3].location, "wq1")
        self.add_piece(self.wk, self.piecesBoard[7][4].location, "wk2")

        self.add_piece(self.wp, self.piecesBoard[6][0].location, "wp1")
        self.add_piece(self.wp, self.piecesBoard[6][1].location, "wp2")
        self.add_piece(self.wp, self.piecesBoard[6][2].location, "wp3")
        self.add_piece(self.wp, self.piecesBoard[6][3].location, "wp4")
        self.add_piece(self.wp, self.piecesBoard[6][4].location, "wp5")
        self.add_piece(self.wp, self.piecesBoard[6][5].location, "wp6")
        self.add_piece(self.wp, self.piecesBoard[6][6].location, "wp7")
        self.add_piece(self.wp, self.piecesBoard[6][7].location, "wp8")
        
    def init_dice(self):
        # beginning image
        self.dice1 = ImageTk.PhotoImage(Image.open("data/die/dice1.png").resize((64, 64), Image.ANTIALIAS))
        self.canvas.create_image(self.width - 50, self.height / 2, image=self.dice1 , tag="dice")

    def highlight_green(self, x, y, color):
        self.canvas.create_rectangle(((x - 1) * 64) +4, ((y) * 64) + 37, 
            ((x - 1) * 64) + self.dim_square, (y * 64) + self.dim_square + 35, 
            fill = color, tag = "move_locations")
        self.canvas.tag_lower("move_locations")
        self.canvas.tag_lower("board")

    def add_piece(self, img, location, piece):
        self.canvas.delete("piece_selected")
        self.canvas.delete("move_locations")
        posx = int(location[1])
        posy = int(location[0])
        self.board[posy][posx] = piece
        print(self.board)
        offset_x = 32
        offset_y = 132
        self.canvas.create_image(offset_x * (((posx+1)*2)-1), offset_y + (self.dim_square * ((posy+1)-1)), 
            image=img, anchor="center", tag=piece)             

def on_click(event, chessboard):
    print(chessboard.board)
    print()

def motion(event, chessboard):
    x, y = event.x - 2, event.y - 100
    downcoord = math.floor(y/64)
    overcoord = math.floor(x/64)
    over = math.ceil(x/64)+64 
    down = abs(math.ceil(y/64) - 9)
    overChar = chr(over)
    chessboard.canvas.delete("hlight")
    print(chessboard.x1, chessboard.y1)
    if x > 0 and x < 512 and y > 0 and y < 512:
        piece = chessboard.board[downcoord][overcoord]
        chessboard.loc = str(overChar) + str(down)
        CHESSBOARD.x1 = over-64
        CHESSBOARD.y1 = abs(down-9)
        chessboard.canvas.create_rectangle(((chessboard.x1 - 1) * 64) +4, ((chessboard.y1) * 64) + 37, 
            ((chessboard.x1 - 1) * 64) + chessboard.dim_square, (chessboard.y1 * 64) + chessboard.dim_square + 35, 
            fill = chessboard.color3, tag = "hlight")
        chessboard.canvas.tag_raise("move_locations")
        chessboard.canvas.tag_raise(piece)
        chessboard.canvas.lower("move_locations")
        chessboard.canvas.lower("board")
        #print(downcoord, overcoord)

def main():
    root = tk.Tk()
    root.title('Fuzzy-Logic Medieval Chess')
    chessboard = CHESSBOARD(root)
    icon = PhotoImage(file="./data/misc/mainIcon.png")
    root.iconphoto(False, icon)
    root.resizable(False, False)
    root.bind("<Motion>", lambda event: motion(event, chessboard))
    root.bind("<Button-1>", lambda event: on_click(event, chessboard))

    # [Row, Column], [Down, Over]

    # id, type, team (-1 = white, 1 = black), corps (1, 2, 3), loc (array)

    root.mainloop()

if __name__ == "__main__":
    main()