from tkinter import *
import tkinter as tk
import math

class CHESSBOARD:
    x1 = -1
    y1 = -1
    loc = ""
    color1 = "#706677"
    color2 = "#ccb7ae"
    highlight = "#eefaac"
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
        self.add_piece(self.br, lbr1)
        self.add_piece(self.br, lbr2)

        self.bkn = PhotoImage(file="./icons/bkn.png")
        lbkn1, lbkn2 = "21", "71"
        self.add_piece(self.bkn, lbkn1)
        self.add_piece(self.bkn, lbkn2)

        self.bb = PhotoImage(file="./icons/bb.png")
        lbb1, lbb2 = "31", "61"
        self.add_piece(self.bb, lbb1)
        self.add_piece(self.bb, lbb2)

        self.bq = PhotoImage(file="./icons/bq.png")
        lbq = "41"
        self.add_piece(self.bq, lbq)

        self.bk = PhotoImage(file="./icons/bk.png")
        lbk = "51"
        self.add_piece(self.bk, lbk)

        
        self.bp = PhotoImage(file="./icons/bp.png")
        lbp1, lbp2, lbp3, lbp4, lbp5, lbp6, lbp7, lbp8 = "12", "22", "32", "42", "52", "62", "72", "82"
        self.add_piece(self.bp, lbp1)
        self.add_piece(self.bp, lbp2)
        self.add_piece(self.bp, lbp3)
        self.add_piece(self.bp, lbp4)
        self.add_piece(self.bp, lbp5)
        self.add_piece(self.bp, lbp6)
        self.add_piece(self.bp, lbp7)
        self.add_piece(self.bp, lbp8)
        
        
        self.wr = PhotoImage(file='./icons/wr.png')
        lwr1, lwr2 = "18", "88"
        self.add_piece(self.wr, lwr1)
        self.add_piece(self.wr, lwr2)

        self.wkn = PhotoImage(file="./icons/wkn.png")
        lwkn1, lwkn2 = "28", "78"
        self.add_piece(self.wkn, lwkn1)
        self.add_piece(self.wkn, lwkn2)

        self.wb = PhotoImage(file="./icons/wb.png")
        lwb1, lwb2 = "38", "68"
        self.add_piece(self.wb, lwb1)
        self.add_piece(self.wb, lwb2)

        self.wq = PhotoImage(file="./icons/wq.png")
        lwq = "48"
        self.add_piece(self.wq, lwq)

        self.wk = PhotoImage(file="./icons/wk.png")
        lwk = "58"
        self.add_piece(self.wk, lwk)

        self.wp = PhotoImage(file="./icons/wp.png")
        lwp1, lwp2, lwp3, lwp4, lwp5, lwp6, lwp7, lwp8 = "17", "27", "37", "47", "57", "67", "77", "87"
        self.add_piece(self.wp, lwp1)
        self.add_piece(self.wp, lwp2)
        self.add_piece(self.wp, lwp3)
        self.add_piece(self.wp, lwp4)
        self.add_piece(self.wp, lwp5)
        self.add_piece(self.wp, lwp6)
        self.add_piece(self.wp, lwp7)
        self.add_piece(self.wp, lwp8)
    def add_piece(self, img, location):

        posx = int(location[0])
        posy = int(location[1])
        offset_x = 32
        offset_y = 132
        self.canvas.create_image(offset_x * ((posx*2)-1), offset_y + (self.dim_square * (posy-1)), 
            image=img, anchor="center", tag="piece")
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
        #print(loc)
        CHESSBOARD.x1 = over-64
        CHESSBOARD.y1 = abs(down-9)
        chessboard.canvas.create_rectangle(((chessboard.x1 - 1) * 64) +4, ((chessboard.y1) * 64) + 37, 
            ((chessboard.x1 - 1) * 64) + chessboard.dim_square, (chessboard.y1 * 64) + chessboard.dim_square + 35, 
            fill = "#eefaac", tag = "hlight")
        chessboard.canvas.tag_raise("piece")

def main():
    root = tk.Tk()
    root.title('Chess Game')
    chessboard = CHESSBOARD(root)
    icon = PhotoImage(file="./icons/mainIcon.png")
    root.iconphoto(False, icon)
    root.resizable(False, False)
    root.bind("<Motion>", lambda event: motion(event, chessboard))
    root.mainloop()

if __name__ == "__main__":
    main()