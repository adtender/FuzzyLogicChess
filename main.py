from tkinter import *
import tkinter as tk

class CHESSBOARD:
    black = "#000000"
    white = "#ffffff"
    highlight = "#77db69"
    rows = 8
    cols = 8
    tileDim = 64

    def __init__(self, parent):
        canvas_width = self.cols * self.tileDim
        canvas_height = self.rows * self.tileDim
        self.canvas = tk.Canvas(parent, width=canvas_width+100, height=canvas_height+200)
        self.canvas.pack(padx=8, pady=8)
        


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