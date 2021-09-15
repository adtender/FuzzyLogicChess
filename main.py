from tkinter import *
import tkinter as tk
import math

class CHESSBOARD:
    x1 = -1
    y1 = -1
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
        #self.canvas.bind("<Button-1>", self.square_clicked)

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
                                                tags="area")
                intCheck += 1

    def checkerboard_color(self, intCheck):
        if intCheck % 2 == 0:
            return self.color1
        else:
            return self.color2

    #def locToCoords(self, loc):
        

def motion(event, chessboard):
    x, y = event.x - 2, event.y - 100
    over = math.ceil(x/64)+64 
    down = abs(math.ceil(y/64) - 9)
    overChar = chr(over)
    if x > 0 and x <= 512 and y > 0 and y <= 512:
        loc = str(overChar) + str(down)
        #print(over - 64,abs(down-9))
        #print(loc)
        #CHESSBOARD.self.canvas.create_rectangle(1,1, 10, 10, fill=CHESSBOARD.highlight)
        CHESSBOARD.x1 = over-64
        CHESSBOARD.y1 = abs(down-9)
        print(CHESSBOARD.x1)
        chessboard.canvas.delete("hlight")
        chessboard.canvas.create_rectangle(((chessboard.x1 - 1) * 64) +3, ((chessboard.y1) * 64) + 36, 
            ((chessboard.x1 - 1) * 64) + chessboard.dim_square, (chessboard.y1 * 64) + chessboard.dim_square + 35, 
            fill = "#eefaac", tag = "hlight")
        return over - 64, abs(down-9), loc
    return -999, -999, -999

def highlight(event, chessboard):
    chessboard.canvas.create_rectangle(chessboard.x1 +2, chessboard.y1 + 100, chessboard.x1 + chessboard.dim_square, chessboard.y1 + chessboard.dim_square, fill = "#eefaac")

def main():
    root = tk.Tk()
    root.title('Chess Game')
    chessboard = CHESSBOARD(root)
    icon = PhotoImage(file="./icons/mainIcon.png")
    root.iconphoto(False, icon)
    root.resizable(False, False)
    #root.bind('<Motion>', motion)
    root.bind("<Motion>", lambda event: motion(event, chessboard))
    #highlight('<Motion>', chessboard)
    #chessboard.canvas.create_rectangle(chessboard.x1 +2, chessboard.y1 + 100, chessboard.x1 + chessboard.dim_square, chessboard.y1 + chessboard.dim_square, fill = "#eefaac")
    root.mainloop()

if __name__ == "__main__":
    main()