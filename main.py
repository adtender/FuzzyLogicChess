from tkinter import *
import tkinter as tk
import numpy as np
import math
import random
from PIL import ImageTk, Image

class CHESSBOARD:
    board = np.empty((9,9), dtype="<U10")
    vMove = [""]
    selectedPieceLocation = ""
    x1 = -1
    y1 = -1
    loc = ""
    color1 = "#706677"
    color2 = "#ccb7ae"
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
        self.br = PhotoImage(file="./icons/br.png")
        lbr1, lbr2 = "11", "81"
        self.add_piece(self.br, lbr1, "br1")
        self.add_piece(self.br, lbr2, "br2")

        self.bkn = PhotoImage(file="./icons/bkn.png")
        lbkn1, lbkn2 = "21", "71"
        self.add_piece(self.bkn, lbkn1, "bkn1")
        self.add_piece(self.bkn, lbkn2, "bkn2")

        self.bb = PhotoImage(file="./icons/bb.png")
        lbb1, lbb2 = "31", "61"
        self.add_piece(self.bb, lbb1, "bb1")
        self.add_piece(self.bb, lbb2, "bb2")

        self.bq = PhotoImage(file="./icons/bq.png")
        lbq = "41"
        self.add_piece(self.bq, lbq, "bq")

        self.bk = PhotoImage(file="./icons/bk.png")
        lbk = "51"
        self.add_piece(self.bk, lbk, "bk")

        
        self.bp = PhotoImage(file="./icons/bp.png")
        lbp1, lbp2, lbp3, lbp4, lbp5, lbp6, lbp7, lbp8 = "12", "22", "32", "42", "52", "62", "72", "82"
        self.add_piece(self.bp, lbp1, "bp1")
        self.add_piece(self.bp, lbp2, "bp2")
        self.add_piece(self.bp, lbp3, "bp3")
        self.add_piece(self.bp, lbp4, "bp4")
        self.add_piece(self.bp, lbp5, "bp5")
        self.add_piece(self.bp, lbp6, "bp6")
        self.add_piece(self.bp, lbp7, "bp7")
        self.add_piece(self.bp, lbp8, "bp8")
        
        
        self.wr = PhotoImage(file='./icons/wr.png')
        lwr1, lwr2 = "18", "88"
        self.add_piece(self.wr, lwr1, "wr1")
        self.add_piece(self.wr, lwr2, "wr2")

        self.wkn = PhotoImage(file="./icons/wkn.png")
        lwkn1, lwkn2 = "28", "78"
        self.add_piece(self.wkn, lwkn1, "wkn1")
        self.add_piece(self.wkn, lwkn2, "wkn2")

        self.wb = PhotoImage(file="./icons/wb.png")
        lwb1, lwb2 = "38", "68"
        self.add_piece(self.wb, lwb1, "wb1")
        self.add_piece(self.wb, lwb2, "wb2")

        self.wq = PhotoImage(file="./icons/wq.png")
        lwq = "48"
        self.add_piece(self.wq, lwq, "wq")

        self.wk = PhotoImage(file="./icons/wk.png")
        lwk = "58"
        self.add_piece(self.wk, lwk, "wk")

        self.wp = PhotoImage(file="./icons/wp.png")
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
        print(img, location, piece)
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
            fill = "#4bc96c", tag = "move_locations")
        self.canvas.lower("move_locations")
        self.canvas.lower("board")
        self.valid_move(x, y, piece)
    
    def piece_logic(self, piece, x, y):
        if(piece=="bp1" or piece=="bp2" or piece=="bp3" or piece=="bp4" or piece=="bp5" or piece=="bp6" or piece=="bp7" or piece=="bp8"):
            if(y<8):
                self.highlight_green(x-1, y+1, piece)
                self.highlight_green(x, y+1, piece)
                if(x<8):
                    self.highlight_green(x+1, y+1, piece)

        if(piece=="wp1" or piece=="wp2" or piece=="wp3" or piece=="wp4" or piece=="wp5" or piece=="wp6" or piece=="wp7" or piece=="wp8"):
            if(y<8):
                self.highlight_green(x-1, y-1, piece)
                self.highlight_green(x, y-1, piece)
                if(x<8):
                    self.highlight_green(x+1, y-1, piece)

        if(piece=="br1" or piece=="br2"):
            return
        
        if(piece=="wr1" or piece=="wr2"):
            return

        if(piece=="bkn1" or piece=="bkn2"):
            return

        if(piece=="wkn1" or piece=="wkn2"):
            return

        if(piece=="bb1" or piece=="bb2"):

            return

        if(piece=="wb1" or piece=="wb2"):
            return
        
        if(piece=="bq"):
            return

        if(piece=="wq"):
            return

        if(piece=="bk"):
            return

        if(piece=="wk"):
            return

    def piece_check(self):
        self.canvas.delete("move_locations")
        if (self.board[self.x1][self.y1] != ""):
            self.canvas.delete("piece_selected")
            self.canvas.create_rectangle(((self.x1 - 1) * 64) +4, ((self.y1) * 64) + 37, 
                ((self.x1 - 1) * 64) + self.dim_square, (self.y1 * 64) + self.dim_square + 35, 
                fill = "#eefaac", tag = "piece_selected")
            self.piece_logic(self.board[self.x1][self.y1], self.x1, self.y1)
            self.selectedPieceLocation = str(self.x1) + str(self.y1)
            #print(self.board[self.x1][self.y1])
            return 1
        else:
            for i in self.vMove:
                if(str(self.x1) + str(self.y1) == i):
                    piece_name = self.vMove[0][-1]
                    #piece_name = piece_name[-1]
                    if (piece_name.isnumeric()):
                        piece_name = self.vMove[0][:-1]
                    relPath = "./icons/" + piece_name + ".png"
                    img = eval("self." + piece_name)
                    self.canvas.delete(self.vMove[0])
                    self.add_piece(img, str(self.x1) + str(self.y1), self.vMove[0])
                    self.canvas.delete("piece_selected")
                    #print(self.x1, self.y1)
                    self.board[int(self.selectedPieceLocation[0])][int(self.selectedPieceLocation[1])] = ""

            
        return 0

    def valid_move(self, x, y, piece):
        self.vMove[0] = piece
        self.vMove.append(str(x)+str(y))
        #print(self.vMove)

    def roll_value(self):
        self.dice_val = random.randrange(1,6)
        #print(self.dice_val)
        return self.dice_val

    def show_dice(self):
        self.dice1 = ImageTk.PhotoImage(Image.open("icons/dice1.png").resize((64, 64), Image.ANTIALIAS))
        self.dice2 = ImageTk.PhotoImage(Image.open("icons/dice2.png").resize((64, 64), Image.ANTIALIAS))
        self.dice3 = ImageTk.PhotoImage(Image.open("icons/dice3.png").resize((64, 64), Image.ANTIALIAS))
        self.dice4 = ImageTk.PhotoImage(Image.open("icons/dice4.png").resize((64, 64), Image.ANTIALIAS))
        self.dice5 = ImageTk.PhotoImage(Image.open("icons/dice5.png").resize((64, 64), Image.ANTIALIAS))
        self.dice6 = ImageTk.PhotoImage(Image.open("icons/dice6.png").resize((64, 64), Image.ANTIALIAS))

        self.canvas.create_image(self.width - 50, self.height / 2, image=self.dice1 , tag="dice")

        for roll in range(0, self.fake_roll_val):
            print(roll)
            self.roll_value()
            print(self.dice_val)
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
        

def on_right_click(event, chessboard):
    piece = chessboard.board[chessboard.x1][chessboard.y1]
    chessboard.canvas.delete(piece)
    chessboard.board[chessboard.x1][chessboard.y1] = ""

def on_click(event, chessboard):
    x, y = event.x - 2, event.y - 100
    if x > 0 and x <= 512 and y > 0 and y <= 512:
        #chessboard.canvas.create_rectangle(((chessboard.x1 - 1) * 64) +4, ((chessboard.y1) * 64) + 37, 
        #    ((chessboard.x1 - 1) * 64) + chessboard.dim_square, (chessboard.y1 * 64) + chessboard.dim_square + 35, 
        #    fill = "#4bc96c", tag = "move_locations")
        
        piece = chessboard.board[chessboard.x1][chessboard.y1]
        chessboard.piece_check()
        chessboard.canvas.tag_raise(piece)
        print(chessboard.board)

def motion(event, chessboard):
    x, y = event.x - 2, event.y - 100
    over = math.ceil(x/64)+64 
    down = abs(math.ceil(y/64) - 9)
    overChar = chr(over)
    chessboard.canvas.delete("hlight")
    piece = chessboard.board[chessboard.x1][chessboard.y1]
    if x > 0 and x <= 512 and y > 0 and y <= 512:
        chessboard.loc = str(overChar) + str(down)
        #print(over - 64,abs(down-9))
        #print(chessboard.loc)
        CHESSBOARD.x1 = over-64
        CHESSBOARD.y1 = abs(down-9)
        chessboard.canvas.create_rectangle(((chessboard.x1 - 1) * 64) +4, ((chessboard.y1) * 64) + 37, 
            ((chessboard.x1 - 1) * 64) + chessboard.dim_square, (chessboard.y1 * 64) + chessboard.dim_square + 35, 
            fill = "#eefaac", tag = "hlight")
        chessboard.canvas.tag_raise("move_locations")
        chessboard.canvas.tag_raise(piece)
        chessboard.canvas.lower("move_locations")
        chessboard.canvas.lower("board")

def main():
    root = tk.Tk()
    root.title('Fuzzy-Logic Medieval Chess')
    chessboard = CHESSBOARD(root)
    icon = PhotoImage(file="./icons/mainIcon.png")
    root.iconphoto(False, icon)
    root.resizable(False, False)
    root.bind("<Motion>", lambda event: motion(event, chessboard))
    root.bind("<Button-1>", lambda event: on_click(event, chessboard))
    root.bind('<Button-3>', lambda event: on_right_click(event, chessboard))
    root.mainloop()

if __name__ == "__main__":
    main()
