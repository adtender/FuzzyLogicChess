from tkinter import *
import tkinter as tk

class CHESSBOARD:
    color1 = "#adede4"
    color2 = "#e8ebea"
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
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.dim_square)+2
                y1 = ((7 - row) * self.dim_square) + 100
                x2 = x1 + self.dim_square
                y2 = y1 + self.dim_square
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color,
                                                 tags="area")
                color = self.color1 if color == self.color2 else self.color2

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