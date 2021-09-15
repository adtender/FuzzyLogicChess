from tkinter import *
import tkinter as tk

class CHESSBOARD:
    color1 = "#706677"
    color2 = "#ccb7ae"
    highlight = "#77db69"
    rows = 8
    columns = 8
    dim_square = 64

    def __init__(self, parent):
        canvas_width = self.columns * self.dim_square + 100
        canvas_height = self.rows * self.dim_square + 200
        self.canvas = tk.Canvas(parent, width=canvas_width, height=canvas_height)
        self.canvas.pack(padx=8, pady=8)
        self.draw_board()

    def draw_board(self):
        intCheck = 0
        for row in range(self.rows):
            intCheck += 1
            for col in range(self.columns):
                x1 = (col * self.dim_square) + 2
                y1 = ((row) * self.dim_square) + 100
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

def main():
    root = tk.Tk()
    root.title('Chess Game')
    chessboard = CHESSBOARD(root)
    icon = PhotoImage(file="./icons/mainIcon.png")
    root.iconphoto(False, icon)
    root.resizable(False, False)
    root.mainloop()

if __name__ == "__main__":
    main()