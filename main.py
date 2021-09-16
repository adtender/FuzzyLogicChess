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
        self.add_pieces()

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

    def add_pieces(self):
        self.bb = PhotoImage(file="./icons/bb.png")
        self.bk = PhotoImage(file="./icons/bk.png")
        self.bkn = PhotoImage(file="./icons/bkn.png")
        self.bp = PhotoImage(file="./icons/bp.png")
        self.bq = PhotoImage(file="./icons/bq.png")
        self.br = PhotoImage(file="./icons/br.png")
        self.wb = PhotoImage(file="./icons/wb.png")
        self.wk = PhotoImage(file="./icons/wk.png")
        self.wkn = PhotoImage(file="./icons/wkn.png")
        self.wp = PhotoImage(file="./icons/wp.png")
        self.wq = PhotoImage(file="./icons/wq.png")
        self.wr = PhotoImage(file='./icons/wr.png')
        self.canvas.create_image(32, 132, image=self.wr, anchor="center", tag="piece")
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
        #chessboard.canvas.tag_lower("hlight")

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