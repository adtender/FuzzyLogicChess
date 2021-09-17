from tkinter import *
import tkinter as tk
import numpy as np
import math

class CHESSBOARD:
    board = np.empty((9,9), dtype="<U10")
    x1 = -1
    y1 = -1
    loc = ""
    color1 = "#706677"
    color2 = "#ccb7ae"
    rows = 8
    columns = 8
    dim_square = 64

    def __init__(self, parent):
        canvas_width = self.columns * self.dim_square + 100
        canvas_height = self.rows * self.dim_square + 200
        self.canvas = tk.Canvas(parent, width=canvas_width, height=canvas_height)
        self.canvas.pack(padx=8, pady=8)
        self.draw_board()
        self.pieces()

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
        self.add_piece(self.br, lbr1, "br")
        self.add_piece(self.br, lbr2, "br")

        self.bkn = PhotoImage(file="./icons/bkn.png")
        lbkn1, lbkn2 = "21", "71"
        self.add_piece(self.bkn, lbkn1, "bkn")
        self.add_piece(self.bkn, lbkn2, "bkn")

        self.bb = PhotoImage(file="./icons/bb.png")
        lbb1, lbb2 = "31", "61"
        self.add_piece(self.bb, lbb1, "bb")
        self.add_piece(self.bb, lbb2, "bb")

        self.bq = PhotoImage(file="./icons/bq.png")
        lbq = "41"
        self.add_piece(self.bq, lbq, "bq")

        self.bk = PhotoImage(file="./icons/bk.png")
        lbk = "51"
        self.add_piece(self.bk, lbk, "bk")

        
        self.bp = PhotoImage(file="./icons/bp.png")
        lbp1, lbp2, lbp3, lbp4, lbp5, lbp6, lbp7, lbp8 = "12", "22", "32", "42", "52", "62", "72", "82"
        self.add_piece(self.bp, lbp1, "bp")
        self.add_piece(self.bp, lbp2, "bp")
        self.add_piece(self.bp, lbp3, "bp")
        self.add_piece(self.bp, lbp4, "bp")
        self.add_piece(self.bp, lbp5, "bp")
        self.add_piece(self.bp, lbp6, "bp")
        self.add_piece(self.bp, lbp7, "bp")
        self.add_piece(self.bp, lbp8, "bp")
        
        
        self.wr = PhotoImage(file='./icons/wr.png')
        lwr1, lwr2 = "18", "88"
        self.add_piece(self.wr, lwr1, "wr")
        self.add_piece(self.wr, lwr2, "wr")

        self.wkn = PhotoImage(file="./icons/wkn.png")
        lwkn1, lwkn2 = "28", "78"
        self.add_piece(self.wkn, lwkn1, "wkn")
        self.add_piece(self.wkn, lwkn2, "wkn")

        self.wb = PhotoImage(file="./icons/wb.png")
        lwb1, lwb2 = "38", "68"
        self.add_piece(self.wb, lwb1, "wb")
        self.add_piece(self.wb, lwb2, "wb")

        self.wq = PhotoImage(file="./icons/wq.png")
        lwq = "48"
        self.add_piece(self.wq, lwq, "wq")

        self.wk = PhotoImage(file="./icons/wk.png")
        lwk = "58"
        self.add_piece(self.wk, lwk, "wk")

        self.wp = PhotoImage(file="./icons/wp.png")
        lwp1, lwp2, lwp3, lwp4, lwp5, lwp6, lwp7, lwp8 = "17", "27", "37", "47", "57", "67", "77", "87"
        self.add_piece(self.wp, lwp1, "wp")
        self.add_piece(self.wp, lwp2, "wp")
        self.add_piece(self.wp, lwp3, "wp")
        self.add_piece(self.wp, lwp4, "wp")
        self.add_piece(self.wp, lwp5, "wp")
        self.add_piece(self.wp, lwp6, "wp")
        self.add_piece(self.wp, lwp7, "wp")
        self.add_piece(self.wp, lwp8, "wp")

    def add_piece(self, img, location, piece):
        posx = int(location[0])
        posy = int(location[1])
        self.board[posx][posy] = piece
        offset_x = 32
        offset_y = 132
        self.canvas.create_image(offset_x * ((posx*2)-1), offset_y + (self.dim_square * (posy-1)), 
            image=img, anchor="center", tag="piece")

    def highlight_green(self, x, y):
        #self.canvas.delete("move_locations")
        self.canvas.create_rectangle(((x - 1) * 64) +4, ((y) * 64) + 37, 
            ((x - 1) * 64) + self.dim_square, (y * 64) + self.dim_square + 35, 
            fill = "#4bc96c", tag = "move_locations")
    
    def piece_logic(self, piece, x, y):
        if(piece=="bp"):
            if(y<8):
                self.highlight_green(x-1, y+1)
                self.highlight_green(x, y+1)
                if(x<8):
                    self.highlight_green(x+1, y+1)

        if(piece=="wp"):
            if(y<8):
                self.highlight_green(x-1, y-1)
                self.highlight_green(x, y-1)
                if(x<8):
                    self.highlight_green(x+1, y-1)

        return

    def piece_check(self):
        self.canvas.delete("move_locations")
        if (self.board[self.x1][self.y1] != ""):
            self.canvas.delete("piece_selected")
            self.canvas.create_rectangle(((self.x1 - 1) * 64) +4, ((self.y1) * 64) + 37, 
                ((self.x1 - 1) * 64) + self.dim_square, (self.y1 * 64) + self.dim_square + 35, 
                fill = "#eefaac", tag = "piece_selected")
            self.piece_logic(self.board[self.x1][self.y1], self.x1, self.y1)
            #print(self.board[self.x1][self.y1])

def on_click(event, chessboard):
    x, y = event.x - 2, event.y - 100
    if x > 0 and x <= 512 and y > 0 and y <= 512:
        #chessboard.canvas.create_rectangle(((chessboard.x1 - 1) * 64) +4, ((chessboard.y1) * 64) + 37, 
        #    ((chessboard.x1 - 1) * 64) + chessboard.dim_square, (chessboard.y1 * 64) + chessboard.dim_square + 35, 
        #    fill = "#4bc96c", tag = "move_locations")
        
        chessboard.piece_check()
        chessboard.canvas.tag_raise("piece")
        #print(chessboard.board)
    return

def motion(event, chessboard):
    x, y = event.x - 2, event.y - 100
    over = math.ceil(x/64)+64 
    down = abs(math.ceil(y/64) - 9)
    overChar = chr(over)
    chessboard.canvas.delete("hlight")
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
        chessboard.canvas.tag_raise("piece")

def main():
    root = tk.Tk()
    root.title('Fuzzy-Logic Medieval Chess')
    chessboard = CHESSBOARD(root)
    icon = PhotoImage(file="./icons/mainIcon.png")
    root.iconphoto(False, icon)
    root.resizable(False, False)
    root.bind("<Motion>", lambda event: motion(event, chessboard))
    root.bind("<Button-1>", lambda event: on_click(event, chessboard))
    root.mainloop()

if __name__ == "__main__":
    main()
