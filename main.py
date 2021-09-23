from tkinter import *
import tkinter as tk
import numpy as np
import math
import random
from PIL import ImageTk, Image

class CHESSBOARD:
    board = np.empty((9,9), dtype="<U10")
    x1 = -1
    y1 = -1
    color1 = "#706677"
    color2 = "#ccb7ae"
    color3 = "#eefaac"
    color4 = "#4bc96c"
    rows = 8
    columns = 8
    dim_square = 64
    top_offset = 200
    side_offset = 100
    width = columns * dim_square + side_offset
    height = rows * dim_square + top_offset
    dice_val = ""
    fake_roll_val = 5
    fake_roll_time_interval = 200
    turn = 0
    selected_piece = ["", ""]

    def __init__(self, parent):
        canvas_width = self.width
        canvas_height = self.height
        self.canvas = tk.Canvas(parent, width=canvas_width, height=canvas_height)
        self.canvas.pack(padx=8, pady=8)
        self.draw_board()
        self.pieces()
        self.show_dice()


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

    def checkerboard_color(self, intCheck):
        if intCheck % 2 == 0:
            return self.color1
        else:
            return self.color2

    def pieces(self):
        self.br = PhotoImage(file="./data/pieces/br.png")
        lbr1, lbr2 = "11", "81"
        self.add_piece(self.br, lbr1, "br1")
        self.add_piece(self.br, lbr2, "br2")

        self.bkn = PhotoImage(file="./data/pieces/bkn.png")
        lbkn1, lbkn2 = "21", "71"
        self.add_piece(self.bkn, lbkn1, "bkn1")
        self.add_piece(self.bkn, lbkn2, "bkn2")

        self.bb = PhotoImage(file="./data/pieces/bb.png")
        lbb1, lbb2 = "31", "61"
        self.add_piece(self.bb, lbb1, "bb1")
        self.add_piece(self.bb, lbb2, "bb2")

        self.bq = PhotoImage(file="./data/pieces/bq.png")
        lbq = "41"
        self.add_piece(self.bq, lbq, "bq")

        self.bk = PhotoImage(file="./data/pieces/bk.png")
        lbk = "51"
        self.add_piece(self.bk, lbk, "bk")

        
        self.bp = PhotoImage(file="./data/pieces/bp.png")
        lbp1, lbp2, lbp3, lbp4, lbp5, lbp6, lbp7, lbp8 = "12", "22", "32", "42", "52", "62", "72", "82"
        self.add_piece(self.bp, lbp1, "bp1")
        self.add_piece(self.bp, lbp2, "bp2")
        self.add_piece(self.bp, lbp3, "bp3")
        self.add_piece(self.bp, lbp4, "bp4")
        self.add_piece(self.bp, lbp5, "bp5")
        self.add_piece(self.bp, lbp6, "bp6")
        self.add_piece(self.bp, lbp7, "bp7")
        self.add_piece(self.bp, lbp8, "bp8")
        
        
        self.wr = PhotoImage(file='./data/pieces/wr.png')
        lwr1, lwr2 = "18", "88"
        self.add_piece(self.wr, lwr1, "wr1")
        self.add_piece(self.wr, lwr2, "wr2")

        self.wkn = PhotoImage(file="./data/pieces/wkn.png")
        lwkn1, lwkn2 = "28", "78"
        self.add_piece(self.wkn, lwkn1, "wkn1")
        self.add_piece(self.wkn, lwkn2, "wkn2")

        self.wb = PhotoImage(file="./data/pieces/wb.png")
        lwb1, lwb2 = "38", "68"
        self.add_piece(self.wb, lwb1, "wb1")
        self.add_piece(self.wb, lwb2, "wb2")

        self.wq = PhotoImage(file="./data/pieces/wq.png")
        lwq = "48"
        self.add_piece(self.wq, lwq, "wq")

        self.wk = PhotoImage(file="./data/pieces/wk.png")
        lwk = "58"
        self.add_piece(self.wk, lwk, "wk")

        self.wp = PhotoImage(file="./data/pieces/wp.png")
        lwp1, lwp2, lwp3, lwp4, lwp5, lwp6, lwp7, lwp8 = "17", "27", "37", "47", "57", "67", "77", "87"
        self.add_piece(self.wp, lwp1, "wp1")
        self.add_piece(self.wp, lwp2, "wp2")
        self.add_piece(self.wp, lwp3, "wp3")
        self.add_piece(self.wp, lwp4, "wp4")
        self.add_piece(self.wp, lwp5, "wp5")
        self.add_piece(self.wp, lwp6, "wp6")
        self.add_piece(self.wp, lwp7, "wp7")
        self.add_piece(self.wp, lwp8, "wp8")

    def add_piece(self, img, location, piece):
        posx = int(location[0])
        posy = int(location[1])
        self.board[posx][posy] = piece
        offset_x = 32
        offset_y = 132
        self.canvas.create_image(offset_x * ((posx*2)-1), offset_y + (self.dim_square * (posy-1)), 
            image=img, anchor="center", tag=piece)

    def highlight_green(self, x, y, piece):
        #self.canvas.delete("move_locations")
        self.canvas.create_rectangle(((x - 1) * 64) +4, ((y) * 64) + 37, 
            ((x - 1) * 64) + self.dim_square, (y * 64) + self.dim_square + 35, 
            fill = self.color4, tag = "move_locations")
        self.canvas.lower("move_locations")
        self.canvas.lower("board")
        self.valid_move(x, y, piece)
    

    def roll_value(self):
        self.dice_val = random.randrange(1,6)
        return self.dice_val

    def show_dice(self):
        self.dice1 = ImageTk.PhotoImage(Image.open("./data/die/dice1.png").resize((64, 64), Image.ANTIALIAS))
        self.dice2 = ImageTk.PhotoImage(Image.open("./data/die/dice2.png").resize((64, 64), Image.ANTIALIAS))
        self.dice3 = ImageTk.PhotoImage(Image.open("./data/die/dice3.png").resize((64, 64), Image.ANTIALIAS))
        self.dice4 = ImageTk.PhotoImage(Image.open("./data/die/dice4.png").resize((64, 64), Image.ANTIALIAS))
        self.dice5 = ImageTk.PhotoImage(Image.open("./data/die/dice5.png").resize((64, 64), Image.ANTIALIAS))
        self.dice6 = ImageTk.PhotoImage(Image.open("./data/die/dice6.png").resize((64, 64), Image.ANTIALIAS))

        self.canvas.create_image(self.width - 50, self.height / 2, image=self.dice1 , tag="dice")

        for roll in range(0, self.fake_roll_val):
            self.roll_value()
            if self.dice_val == 1:
                self.canvas.create_image(self.width - 50, self.height / 2, image=self.dice1 , tag="dice")
            elif self.dice_val == 2:
                self.canvas.create_image(self.width - 50, self.height / 2, image=self.dice2 , tag="dice")
            elif self.dice_val == 3:
                self.canvas.create_image(self.width - 50, self.height / 2, image=self.dice3 , tag="dice")
            elif self.dice_val == 4:
                self.canvas.create_image(self.width - 50, self.height / 2, image=self.dice4 , tag="dice")
            elif self.dice_val == 5:
                self.canvas.create_image(self.width - 50, self.height / 2, image=self.dice5 , tag="dice")
            elif self.dice_val == 6:
                self.canvas.create_image(self.width - 50, self.height / 2, image=self.dice6 , tag="dice")

    def rule_set(self):
        if(self.selected_piece[0][:-1] == "bp"):
            if(int(self.selected_piece[0][2]) <= 3):
                return [1, self.selected_piece[0][0], self.selected_piece[0][1], 1] #distance can travel, team, piece, core
            if(int(self.selected_piece[0][2]) == 4 or int(self.selected_piece[0][2]) == 5):
                return [1, self.selected_piece[0][0], self.selected_piece[0][1], 2]
            if(int(self.selected_piece[0][2]) >= 6):
                return [1, self.selected_piece[0][0], self.selected_piece[0][1], 3]

        if(self.selected_piece[0][:-1] == "wp"):
            if(int(self.selected_piece[0][2]) <= 3):
                return [1, self.selected_piece[0][0], self.selected_piece[0][1], 1]
            if(int(self.selected_piece[0][2]) == 4 or int(self.selected_piece[0][2]) == 5):
                return [1, self.selected_piece[0][0], self.selected_piece[0][1], 2]
            if(int(self.selected_piece[0][2]) >= 6):
                return [1, self.selected_piece[0][0], self.selected_piece[0][1], 3]

        if(self.selected_piece[0][:-1] == "br"):
            return [2, self.selected_piece[0][0], self.selected_piece[0][1], 2]


        if(self.selected_piece[0][:-1] == "wr"):
            return [2, self.selected_piece[0][0], self.selected_piece[0][1], 2]


        if(self.selected_piece[0][:-1] == "bkn"):
            if(int(self.selected_piece[0][3]) == 1):
                return [4, self.selected_piece[0][0], str(self.selected_piece[0][1]) + str(self.selected_piece[0][2]), 1]
            if(int(self.selected_piece[0][3]) == 2):
                return [4, self.selected_piece[0][0], str(self.selected_piece[0][1]) + str(self.selected_piece[0][2]), 3]

        if(self.selected_piece[0][:-1] == "wkn"):
            if(int(self.selected_piece[0][3]) == 1):
                return [4, self.selected_piece[0][0], str(self.selected_piece[0][1]) + str(self.selected_piece[0][2]), 1]
            if(int(self.selected_piece[0][3]) == 2):
                return [4, self.selected_piece[0][0], str(self.selected_piece[0][1]) + str(self.selected_piece[0][2]), 3]

        if(self.selected_piece[0][:-1] == "bb"):
            if(int(self.selected_piece[0][2]) == 1):
                return [2, self.selected_piece[0][0], self.selected_piece[0][1], 1]
            if(int(self.selected_piece[0][2]) == 2):
                return [2, self.selected_piece[0][0], self.selected_piece[0][1], 3]

        if(self.selected_piece[0][:-1] == "wb"):
            if(int(self.selected_piece[0][2]) == 1):
                return [2, self.selected_piece[0][0], self.selected_piece[0][1], 1]
            if(int(self.selected_piece[0][2]) == 2):
                return [2, self.selected_piece[0][0], self.selected_piece[0][1], 3]

        if(self.selected_piece[0] == "bq"):
            return [3, self.selected_piece[0][0], self.selected_piece[0][1], 2]

        if(self.selected_piece[0] == "wq"):
            return [3, self.selected_piece[0][0], self.selected_piece[0][1], 2]

        if(self.selected_piece[0] == "bk"):
            return [3, self.selected_piece[0][0], self.selected_piece[0][1], 2]

        if(self.selected_piece[0] == "wk"):
            return [3, self.selected_piece[0][0], self.selected_piece[0][1], 2]
            
        return

    def valid_moves(self, ):
        return
        

def on_right_click(event, chessboard):
    piece = chessboard.board[chessboard.x1][chessboard.y1]
    chessboard.canvas.delete(piece)
    chessboard.board[chessboard.x1][chessboard.y1] = ""

def on_click(event, chessboard):
    chessboard.canvas.delete("piece_selected")
    chessboard.selected_piece = ["", ""]
    x, y = event.x - 2, event.y - 100
    if x > 0 and x <= 512 and y > 0 and y <= 512:
        if(chessboard.board[chessboard.x1][chessboard.y1] != ""):
            chessboard.canvas.create_rectangle(((chessboard.x1 - 1) * 64) +4, ((chessboard.y1) * 64) + 37, 
                ((chessboard.x1 - 1) * 64) + chessboard.dim_square, (chessboard.y1 * 64) + chessboard.dim_square + 35, 
                fill = chessboard.color3, tag = "piece_selected")
            chessboard.selected_piece = [chessboard.board[chessboard.x1][chessboard.y1], str(chessboard.x1) + str(chessboard.y1)]
            dist = chessboard.rule_set()
            print(dist)
        piece = chessboard.board[chessboard.x1][chessboard.y1]
        chessboard.canvas.tag_raise(piece)
        #print(np.rot90(np.fliplr(chessboard.board)))
    #print(chessboard.selected_piece)

def motion(event, chessboard):
    x, y = event.x - 2, event.y - 100
    over = math.ceil(x/64)+64 
    down = abs(math.ceil(y/64) - 9)
    overChar = chr(over)
    chessboard.canvas.delete("hlight")
    piece = chessboard.board[chessboard.x1][chessboard.y1]
    if x > 0 and x <= 512 and y > 0 and y <= 512:
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

def main():
    root = tk.Tk()
    root.title('Fuzzy-Logic Medieval Chess')
    chessboard = CHESSBOARD(root)
    icon = PhotoImage(file="./data/misc/mainIcon.png")
    root.iconphoto(False, icon)
    root.resizable(False, False)
    root.bind("<Motion>", lambda event: motion(event, chessboard))
    root.bind("<Button-1>", lambda event: on_click(event, chessboard))
    root.bind('<Button-3>', lambda event: on_right_click(event, chessboard))
    root.mainloop()

if __name__ == "__main__":
    main()
