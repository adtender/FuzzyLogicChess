from tkinter import *
import tkinter as tk
import numpy as np
import math
from PIL import ImageTk, Image
from pieces import Piece

class CHESSBOARD:
    x1, y1 = None, None
    br, bkn, bb, bq, bk, bp, wr, wkn, wb, wq, wk, wp = "", "", "", "", "", "", "", "", "", "", "", ""
    color1, color2, color3, color4, color5, color6 = "#706677", "#ccb7ae", "#eefaac", "#4bc96c", "#9c1e37", "#b9c288"
    rows, columns = 8, 8
    dim_square = 64
    top_offset, side_offset = 200, 100
    width = columns * dim_square + side_offset
    height = rows * dim_square + top_offset
    turns = -1 # -1 for white, 1 for black
    corpsPlayed = 111 # 1 for able to be played, 2 for unable
    locationLock = []
    locationLockedIn = False
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
        self.corps_rectangles()
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
        #print("White horse 1----------------------\n", Piece.chessboard[7, 1].check_moves(self.piecesBoard))

    def checkerboard_color(self, intCheck):
        if intCheck % 2 == 0:
            return self.color1
        else:
            return self.color2

    def add_piece_objects(self):
        Piece.gen_new_board()

    def corps_rectangles(self):
        self.canvas.create_rectangle(2, 90, 190, 85, fill = '#a60314', tag =        "corpsb1r")
        self.canvas.create_rectangle(195, 90, 320, 85, fill = '#a60314', tag =      "corpsb2r")             # black red
        self.canvas.create_rectangle(325, 90, 510, 85, fill = '#a60314', tag =      "corpsb3r")
        self.canvas.create_rectangle(2, 90, 190, 85, fill = self.color3, tag =      "corpsb1y")
        self.canvas.create_rectangle(195, 90, 320, 85, fill = self.color3, tag =    "corpsb2y")             # black yellow
        self.canvas.create_rectangle(325, 90, 510, 85, fill = self.color3, tag =    "corpsb3y")
        self.canvas.create_rectangle(2, 90, 190, 85, fill = '#00a835', tag =        "corpsb1g")
        self.canvas.create_rectangle(195, 90, 320, 85, fill = '#00a835', tag =      "corpsb2r")             # black green
        self.canvas.create_rectangle(325, 90, 510, 85, fill = '#00a835', tag =      "corpsb3g")
        

        self.canvas.create_rectangle(2, 625, 190, 620, fill = '#a60314', tag =      "corpsw1r")
        self.canvas.create_rectangle(195, 625, 320, 620, fill = '#a60314', tag =    "corpsw2r")             # white red
        self.canvas.create_rectangle(325, 625, 510, 620, fill = '#a60314', tag =    "corpsw3r")
        self.canvas.create_rectangle(2, 625, 190, 620, fill = self.color3, tag =    "corpsw1y")
        self.canvas.create_rectangle(195, 625, 320, 620, fill = self.color3, tag =  "corpsw2y")             # white yellow
        self.canvas.create_rectangle(325, 625, 510, 620, fill = self.color3, tag =  "corpsw3y")
        self.canvas.create_rectangle(2, 625, 190, 620, fill = '#00a835', tag =      "corpsw1g")
        self.canvas.create_rectangle(195, 625, 320, 620, fill = '#00a835', tag =    "corpsw2g")             # white green
        self.canvas.create_rectangle(325, 625, 510, 620, fill = '#00a835', tag =    "corpsw3g")
        
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

        self.add_piece(self.br, Piece.chessboard[0][0].location, "br1")
        self.add_piece(self.br, Piece.chessboard[0][7].location, "br2")
        self.add_piece(self.bh, Piece.chessboard[0][1].location, "bh1")
        self.add_piece(self.bh, Piece.chessboard[0][6].location, "bh2")
        self.add_piece(self.bb, Piece.chessboard[0][2].location, "bb1")
        self.add_piece(self.bb, Piece.chessboard[0][5].location, "bb2")
        self.add_piece(self.bq, Piece.chessboard[0][3].location, "bq1")
        self.add_piece(self.bk, Piece.chessboard[0][4].location, "bk1")

        self.add_piece(self.bp, Piece.chessboard[1][0].location, "bp1")
        self.add_piece(self.bp, Piece.chessboard[1][1].location, "bp2")
        self.add_piece(self.bp, Piece.chessboard[1][2].location, "bp3")
        self.add_piece(self.bp, Piece.chessboard[1][3].location, "bp4")
        self.add_piece(self.bp, Piece.chessboard[1][4].location, "bp5")
        self.add_piece(self.bp, Piece.chessboard[1][5].location, "bp6")
        self.add_piece(self.bp, Piece.chessboard[1][6].location, "bp7")
        self.add_piece(self.bp, Piece.chessboard[1][7].location, "bp8")

        self.add_piece(self.wr, Piece.chessboard[7][0].location, "wr1")
        self.add_piece(self.wr, Piece.chessboard[7][7].location, "wr2")
        self.add_piece(self.wh, Piece.chessboard[7][1].location, "wh1")
        self.add_piece(self.wh, Piece.chessboard[7][6].location, "wh2")
        self.add_piece(self.wb, Piece.chessboard[7][2].location, "wb1")
        self.add_piece(self.wb, Piece.chessboard[7][5].location, "wb2")
        self.add_piece(self.wq, Piece.chessboard[7][3].location, "wq1")
        self.add_piece(self.wk, Piece.chessboard[7][4].location, "wk1")

        self.add_piece(self.wp, Piece.chessboard[6][0].location, "wp1")
        self.add_piece(self.wp, Piece.chessboard[6][1].location, "wp2")
        self.add_piece(self.wp, Piece.chessboard[6][2].location, "wp3")
        self.add_piece(self.wp, Piece.chessboard[6][3].location, "wp4")
        self.add_piece(self.wp, Piece.chessboard[6][4].location, "wp5")
        self.add_piece(self.wp, Piece.chessboard[6][5].location, "wp6")
        self.add_piece(self.wp, Piece.chessboard[6][6].location, "wp7")
        self.add_piece(self.wp, Piece.chessboard[6][7].location, "wp8")
        
    def init_dice(self):
        # beginning image
        self.dice1 = ImageTk.PhotoImage(Image.open("data/die/dice1.png").resize((64, 64), Image.ANTIALIAS))
        self.canvas.create_image(self.width - 50, self.height / 2, image=self.dice1 , tag="dice")

    def add_piece(self, img, location, piece):
        self.canvas.delete("piece_selected")
        self.canvas.delete("move_locations")
        posx = int(location[1])
        posy = int(location[0])
        offset_x = 32
        offset_y = 132
        self.canvas.create_image(offset_x * (((posx+1)*2)-1), offset_y + (self.dim_square * ((posy+1)-1)), 
            image=img, anchor="center", tag=piece)     

    def piece_select(self, locationLock, chessboard):
        yLoc = locationLock[0]
        xLoc = locationLock[1]
        Piece.check_moves(Piece.chessboard[yLoc][xLoc])
        availMoves = Piece.chessboard[yLoc][xLoc].availMoves
        availAttacks = Piece.chessboard[yLoc][xLoc].availAttacks
        self.moves_and_attacks_highlight(availMoves, chessboard, self.color4)
        self.moves_and_attacks_highlight(availAttacks, chessboard, self.color5)

    def piece_move(self, moveToCoords):
        moveCheck = self.check_valid_piece_move(Piece.chessboard[self.locationLock[0]][self.locationLock[1]].availMoves, moveToCoords)
        attackCheck = self.check_valid_piece_move(Piece.chessboard[self.locationLock[0]][self.locationLock[1]].availAttacks, moveToCoords)
        print("moveCheck = ", moveCheck)
        print("attackCheck = ", attackCheck)
        if attackCheck == False and moveCheck: # moves with no attacks
            img = eval("self." # TODO: send to new method
                + Piece.chessboard[self.locationLock[0]][self.locationLock[1]].pieceID[:-1])
            self.canvas.delete(Piece.chessboard[self.locationLock[0]][self.locationLock[1]].pieceID)
            self.add_piece(img, tuple(moveToCoords), str(Piece.chessboard[self.locationLock[0]][self.locationLock[1]].pieceID))
            Piece.chessboard[self.locationLock[0]][self.locationLock[1]].move(moveToCoords[0], moveToCoords[1])
        if moveCheck and attackCheck: # moves with attacks
            img = eval("self." # TODO: send to new method
                + Piece.chessboard[self.locationLock[0]][self.locationLock[1]].pieceID[:-1])
            self.canvas.delete(Piece.chessboard[self.locationLock[0]][self.locationLock[1]].pieceID)
            self.canvas.delete(Piece.chessboard[moveToCoords[0]][moveToCoords[1]].pieceID)
            self.add_piece(img, tuple(moveToCoords), str(Piece.chessboard[self.locationLock[0]][self.locationLock[1]].pieceID))
            Piece.chessboard[self.locationLock[0]][self.locationLock[1]].capture(Piece.chessboard[moveToCoords[0]][moveToCoords[1]])
        if moveCheck == False and attackCheck: #rook attack from afar
            self.canvas.delete(Piece.chessboard[moveToCoords[0]][moveToCoords[1]].pieceID)
            Piece.chessboard[moveToCoords[0]][moveToCoords[1]].kill_piece()
        print(Piece.chessboard)
        self.locationLockedIn = False


    def check_valid_piece_move(self, availMovesOrAttacks, moveToCoords):
        for i in range(len(availMovesOrAttacks)):
            if availMovesOrAttacks[i] == tuple(moveToCoords):
                return True
        return False
        
    def moves_and_attacks_highlight(self, array, chessboard, color):
        arrayToParse = len(array)
        for i in range(arrayToParse):
            x = array[i][0]
            y = array[i][1]
            highlight("move_locations", chessboard, x, y, color)

    #def turn_forward(self, pieceObject):
        #if pieceObject.team == -1:

        #print()

    def change_active_status(self, team, corps, reset):
        for i in range(8):
            for j in range(8):
                if Piece.chessboard[i][j]:
                    if Piece.chessboard[i][j].team == team:
                        if reset:
                            Piece.chessboard[i][j].active = True
                        elif Piece.chessboard[i][j].corps == corps:
                            Piece.chessboard[i][j].active = False

    def clear_corps_indicator_highlight(self):
        self.canvas.lower("corpsw1y")
        self.canvas.lower("corpsw2y")
        self.canvas.lower("corpsw3y")
        self.canvas.lower("corpsb1y")
        self.canvas.lower("corpsb2y")
        self.canvas.lower("corpsb3y")

    def reset_corps_inidcator(self, team):
        if team == -1:
            self.canvas.tag_raise("corpsw1g")
            self.canvas.tag_raise("corpsw2g")
            self.canvas.tag_raise("corpsw3g")
        if team == 1:
            self.canvas.tag_raise("corpsb1g")
            self.canvas.tag_raise("corpsb2g")
            self.canvas.tag_raise("corpsb3g")


def highlight(htag, chessboard, yBoard, xBoard, color):
    chessboard.canvas.create_rectangle(((xBoard) * 64) +4, ((yBoard + 1) * 64) + 37, 
        ((xBoard) * 64) + chessboard.dim_square, ((yBoard + 1) * 64) + chessboard.dim_square + 35, 
        fill = color, tag = htag)

    chessboard.canvas.tag_raise(htag)
    chessboard.canvas.lower("piece_selected")
    chessboard.canvas.lower("move_locations")
    chessboard.canvas.lower("board")

def highlight_corps(chessboard, yBoard, xBoard):
    #print(yBoard, xBoard)
    
    for i in range(8):
        for j in range(8):
            if Piece.chessboard[i][j] and Piece.chessboard[i][j].active:
                team, sTeam = Piece.chessboard[i][j].team, Piece.chessboard[yBoard][xBoard].team
                corps, sCorps = Piece.chessboard[i][j].corps, Piece.chessboard[yBoard][xBoard].corps
                if (Piece.chessboard[i][j].corps == Piece.chessboard[yBoard][xBoard].corps and
                Piece.chessboard[i][j].team == Piece.chessboard[yBoard][xBoard].team):
                    highlight("corpsHlight", chessboard, i, j, chessboard.color6)
                    chessboard.canvas.lower("corpsHlight")
                    if team == -1:
                        if corps == 1: chessboard.canvas.tag_raise("corpsw1y")
                        if corps == 2: chessboard.canvas.tag_raise("corpsw2y")
                        if corps == 3: chessboard.canvas.tag_raise("corpsw3y")
                    if team == 1:
                        if corps == 1: chessboard.canvas.tag_raise("corpsb1y")
                        if corps == 2: chessboard.canvas.tag_raise("corpsb2y")
                        if corps == 3: chessboard.canvas.tag_raise("corpsb3y")
    
def on_click(event, chessboard):
    chessboard.canvas.delete("move_locations")
    chessboard.canvas.delete("piece_selected")
    try:
        yLoc = chessboard.y1 -1
        xLoc = chessboard.x1 -1
    except:
        return
    if Piece.chessboard[yLoc][xLoc] and chessboard.locationLockedIn == False:
        highlight("piece_selected", chessboard, yLoc, xLoc, chessboard.color3)
        chessboard.locationLockedIn = True
        chessboard.locationLock = [yLoc, xLoc]
        chessboard.piece_select(Piece.chessboard[yLoc][xLoc].location, chessboard)
        chessboard.canvas.delete("copsHlight")
        return
    if chessboard.locationLockedIn:
        chessboard.piece_move([yLoc, xLoc])
        chessboard.locationLock = [None]
        chessboard.locationLockedIn = False

def motion(event, chessboard):
    x, y = event.x - 2, event.y - 100
    over = math.ceil(x/64)+64 
    down = abs(math.ceil(y/64) - 9)
    overChar = chr(over)

    chessboard.canvas.delete("hlight")
    chessboard.canvas.delete("corpsHlight")
    chessboard.clear_corps_indicator_highlight()
    if x > 0 and x < 512 and y > 0 and y < 512:
        chessboard.loc = str(overChar) + str(down)
        chessboard.x1 = over-64
        chessboard.y1 = abs(down-9)
        yBoard = chessboard.y1 - 1
        xBoard = chessboard.x1 - 1
        piece = Piece.chessboard[yBoard][xBoard]
        highlight("hlight", chessboard, yBoard, xBoard, chessboard.color3)
        #chessboard.canvas.tag_raise("move_locations")
        if Piece.chessboard[yBoard][xBoard]:
            chessboard.canvas.delete("corpsHlight")
            #chessboard.canvas.tag_raise(piece)
            highlight_corps(chessboard, yBoard, xBoard)            
            chessboard.canvas.tag_raise(piece)
        else:
            chessboard.canvas.delete("corpsHlight")
            chessboard.canvas.lower("move_locations")
        #chessboard.canvas.lower("corpsHlight")
        #chessboard.canvas.lower("move_locations")
        
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

    root.mainloop()

if __name__ == "__main__":
    main()