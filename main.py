from tkinter import *
import tkinter as tk
import numpy as np
import os
import json
import math
import random
from PIL import ImageTk, Image
from pieces import Piece
from data.misc.tkinter_custom_button import TkinterCustomButton

class CHESSBOARD:
    x1, y1 = None, None
    br, bkn, bb, bq, bk, bp, wr, wkn, wb, wq, wk, wp = "", "", "", "", "", "", "", "", "", "", "", ""
    color1, color2, color3, color4, color5, color6 = "#706677", "#ccb7ae", "#eefaac", "#4bc96c", "#9c1e37", "#b9c288"
    rows, columns = 8, 8
    dim_square = 64
    top_offset, side_offset = 200, 400
    width = columns * dim_square + side_offset
    height = rows * dim_square + top_offset
    turns = -1 # -1 for white, 1 for black
    corpsPlayed = [1,1,1] # 1 for able to be played, 2 for unable
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
        self.history_box()

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

    def history_box(self):
        self.canvas.create_rectangle(525, 291, 913, 612, outline='black')

    def corps_rectangles(self):
        self.canvas.create_rectangle(2, 90, 190, 85, fill = self.color3, tag =      "corpsb1y")
        self.canvas.create_rectangle(195, 90, 320, 85, fill = self.color3, tag =    "corpsb2y")             # black yellow
        self.canvas.create_rectangle(325, 90, 510, 85, fill = self.color3, tag =    "corpsb3y")
        self.canvas.create_rectangle(2, 90, 190, 85, fill = '#00a835', tag =        "corpsb1g")
        self.canvas.create_rectangle(195, 90, 320, 85, fill = '#00a835', tag =      "corpsb2g")             # black green
        self.canvas.create_rectangle(325, 90, 510, 85, fill = '#00a835', tag =      "corpsb3g")
        self.canvas.create_rectangle(2, 90, 190, 85, fill = '#a60314', tag =        "corpsb1r")
        self.canvas.create_rectangle(195, 90, 320, 85, fill = '#a60314', tag =      "corpsb2r")             # black red
        self.canvas.create_rectangle(325, 90, 510, 85, fill = '#a60314', tag =      "corpsb3r")
        

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
        self.dice2 = ImageTk.PhotoImage(Image.open("data/die/dice2.png").resize((64, 64), Image.ANTIALIAS))
        self.dice3 = ImageTk.PhotoImage(Image.open("data/die/dice3.png").resize((64, 64), Image.ANTIALIAS))
        self.dice4 = ImageTk.PhotoImage(Image.open("data/die/dice4.png").resize((64, 64), Image.ANTIALIAS))
        self.dice5 = ImageTk.PhotoImage(Image.open("data/die/dice5.png").resize((64, 64), Image.ANTIALIAS))
        self.dice6 = ImageTk.PhotoImage(Image.open("data/die/dice6.png").resize((64, 64), Image.ANTIALIAS))
        self.canvas.create_image(self.width - 192, self.height / 5.4, image=self.dice2 , tag="dice2")
        self.canvas.create_image(self.width - 192, self.height / 5.4, image=self.dice3 , tag="dice3")
        self.canvas.create_image(self.width - 192, self.height / 5.4, image=self.dice4 , tag="dice4")
        self.canvas.create_image(self.width - 192, self.height / 5.4, image=self.dice5 , tag="dice5")
        self.canvas.create_image(self.width - 192, self.height / 5.4, image=self.dice6 , tag="dice6")
        self.canvas.create_image(self.width - 192, self.height / 5.4, image=self.dice1 , tag="dice1")

    def rand_dice(self):
        return random.randrange(1,6)

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
        if Piece.chessboard[locationLock[0]][locationLock[1]].active == False: return
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

        Piece.diceVal = self.rand_dice()

        if (tuple(moveToCoords) not in Piece.chessboard[self.locationLock[0]][self.locationLock[1]].availMoves and 
        tuple(moveToCoords) not in Piece.chessboard[self.locationLock[0]][self.locationLock[1]].availAttacks):
            return

        self.turn_forward(Piece.chessboard[self.locationLock[0]][self.locationLock[1]])

        if attackCheck == False and moveCheck: # moves with no attacks
            img = eval("self." # TODO: send to new method
                + Piece.chessboard[self.locationLock[0]][self.locationLock[1]].pieceID[:-1])
            self.canvas.delete(Piece.chessboard[self.locationLock[0]][self.locationLock[1]].pieceID)
            self.add_piece(img, tuple(moveToCoords), str(Piece.chessboard[self.locationLock[0]][self.locationLock[1]].pieceID))
            Piece.chessboard[self.locationLock[0]][self.locationLock[1]].move(moveToCoords[0], moveToCoords[1])
        if moveCheck and attackCheck: # moves with attacks
            self.canvas.tag_raise("dice" + str(Piece.diceVal))
            b = Piece.chessboard[self.locationLock[0]][self.locationLock[1]].capture(Piece.chessboard[moveToCoords[0]][moveToCoords[1]], False, False)
            if b:
                img = eval("self." # TODO: send to new method
                    + Piece.chessboard[self.locationLock[0]][self.locationLock[1]].pieceID[:-1])
                self.canvas.delete(Piece.chessboard[self.locationLock[0]][self.locationLock[1]].pieceID)
                self.canvas.delete(Piece.chessboard[moveToCoords[0]][moveToCoords[1]].pieceID)
                self.add_piece(img, tuple(moveToCoords), str(Piece.chessboard[self.locationLock[0]][self.locationLock[1]].pieceID))
                Piece.chessboard[self.locationLock[0]][self.locationLock[1]].capture(Piece.chessboard[moveToCoords[0]][moveToCoords[1]], True, False)
        if moveCheck == False and attackCheck: #rook attack from afar
            b = Piece.chessboard[self.locationLock[0]][self.locationLock[1]].capture(Piece.chessboard[moveToCoords[0]][moveToCoords[1]], False, True)
            if b:
                self.canvas.delete(Piece.chessboard[moveToCoords[0]][moveToCoords[1]].pieceID)
                #Piece.chessboard[moveToCoords[0]][moveToCoords[1]].kill_piece()
                Piece.chessboard[self.locationLock[0]][self.locationLock[1]].capture(Piece.chessboard[moveToCoords[0]][moveToCoords[1]], True, True)
        #print(Piece.chessboard)

        if ("wk1" in Piece.graveyard or "bk1" in Piece.graveyard):
            for i in range(8):
                for j in range(8):
                    if Piece.chessboard[i][j]:
                        Piece.chessboard[i][j].active = False
            print("Game over")
            self.canvas.tag_raise("corpsw1r")
            self.canvas.tag_raise("corpsw2r")
            self.canvas.tag_raise("corpsw3r")
            self.canvas.tag_raise("corpsb1r")
            self.canvas.tag_raise("corpsb2r")
            self.canvas.tag_raise("corpsb3r")

        
        self.locationLockedIn = False

    def graveyard(self):
        print

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

    def turn_forward(self, pieceObject):

        teamLetter = "z"

        if pieceObject.team == -1: teamLetter = "w"
        if pieceObject.team == 1: teamLetter = "b"

        corpsIndicatorTag = "corps" + teamLetter + str(pieceObject.corps) + "g"
        
        if pieceObject.corps == 1:
            self.change_active_status(pieceObject.team, pieceObject.corps, False)
            self.corpsPlayed[0] = 2
        if pieceObject.corps == 2:
            self.change_active_status(pieceObject.team, pieceObject.corps, False)
            self.corpsPlayed[1] = 2
        if pieceObject.corps == 3:
            self.change_active_status(pieceObject.team, pieceObject.corps, False)
            self.corpsPlayed[2] = 2

        self.canvas.lower(corpsIndicatorTag)

        if (self.corpsPlayed[0]==2 and self.corpsPlayed[1]==2 and self.corpsPlayed[2]==2):
            self.change_active_status(pieceObject.team * -1, pieceObject.corps, True)
            self.reset_corps_inidcator(pieceObject.team * -1)

    def change_active_status(self, team, corps, reset):
        for i in range(8):
            for j in range(8):
                if Piece.chessboard[i][j]:
                    if Piece.chessboard[i][j].team == team:
                        if reset:
                            Piece.chessboard[i][j].active = True
                            self.corpsPlayed = [1, 1, 1]
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

    def rules_window(self):
        
        global rule1, rule2
        top = Toplevel()
        top.title('Rule Set')
        
        rule1 = ImageTk.PhotoImage(Image.open("./data/misc/FL-MCR1.jpg").resize((680, 880), Image.ANTIALIAS))
        rule2 = ImageTk.PhotoImage(Image.open("./data/misc/FL-MCR2.jpg").resize((680, 880), Image.ANTIALIAS))
        #Label(top, image=rule1).pack()
        #Label(top, image=rule2).pack()
        Label(top, image=rule1).grid(row=0, column=0)
        Label(top, image=rule2).grid(row=0, column=1)


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
        if xLoc == -101:
            chessboard.locationLockedIn = False
            return
    except:
        return
    if Piece.chessboard[yLoc][xLoc] and chessboard.locationLockedIn == False and Piece.chessboard[yLoc][xLoc].active == True:
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
    if x > 0 and x < 512 and y > 0 and y < 512 and not btnState:
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
    else:
        x, y = -1, -1
        chessboard.x1, chessboard.y1 = -100, -100

def main():
    window = Tk()
    window.geometry("1200x634+400+0")
    window.title("Fuzzy-Logic Medieval Chess")

    img = PhotoImage(file="./data/Image/checkmate.gif")
    label = Label(window, image=img)
    window.resizable(False, False)
    label.place(x=0, y=0, relwidth=1, relheight=1)

    def restart():
        os.execl(sys.executable, sys.executable, *sys.argv)
    def load():
        pass

    def save():
        pass

    def credit():
        pass

   
    def start():
        window.destroy()
        root = Tk()
        root.title('Fuzzy-Logic Medieval Chess')
        chessboard = CHESSBOARD(root)
        icon = PhotoImage(file="./data/misc/mainIcon.png")
        root.iconphoto(False, icon)
        root.resizable(False, False)
        root.bind("<Motion>", lambda event: motion(event, chessboard))
        root.bind("<Button-1>", lambda event: on_click(event, chessboard))

        rules_button = TkinterCustomButton(text="Rules", 
                                            bg_color=None,
                                            fg_color="#58636F",
                                            border_color=None,
                                            hover_color="#808B96",
                                            corner_radius=10,
                                            border_width=0,
                                            width= chessboard.width/2.32,
                                            hover=True,
                                            command=chessboard.rules_window)
        history_button = TkinterCustomButton(text="History", 
                                            bg_color=None,
                                            fg_color="#58636F",
                                            border_color=None,
                                            hover_color="#808B96",
                                            corner_radius=10,
                                            border_width=0,
                                            width= chessboard.width/2.32,
                                            hover=True)
        rules_button.place(relx=0.568, rely=0.26)
        history_button.place(relx=0.568, rely=0.32)
        
        #root.mainloop()
        navIcon = PhotoImage(file="./data/Image/menu.png")
        closeIcon = PhotoImage(file="./data/Image/close.png")
        global btnState
        btnState = False
            # setting switch function:
        def switch():
                global btnState
                if btnState:
                    # create animated Navbar closing:
                    #for x in range(301):
                    navRoot.place(x=-301, y=0)
                    # topFrame.update()

                    # resetting widget colors:
                    homeLabel.config(bg="#58636F")
                    topFrame.config(bg="#58636F")
                    root.config(bg="gray17")

                    # turning button OFF:
                    btnState = False
                else:
                    # make root dim:
                    homeLabel.config(bg="#58636F")
                    topFrame.config(bg="#58636F")
                    root.config(bg="#58636F")

                    # created animated Navbar opening:
                  #  for x in range(-300, 0):
                    navRoot.place(x=0, y=0)
                      #  topFrame.update()

                    # turing button ON:
                    btnState = True

            # top Navigation bar:
        topFrame = tk.Frame(root, bg="#58636F")
        topFrame.pack(side="top", fill=tk.X)

            # Header label text:
        homeLabel = tk.Label(topFrame, text="Fuzzy-Logic Medieval Chess", font="Bahnschrift 15", bg="#58636F", fg="white", height=2, padx=20)
        homeLabel.pack(side="right")
       
            # Navbar button:
        navbarBtn = tk.Button(topFrame, image=navIcon, bg="#58636F", activebackground="#58636F", bd=0, padx=20, command=switch)
        navbarBtn.place(x=10, y=10)

            # setting Navbar frame
        navRoot = tk.Frame(root, bg="gray17", height=1000, width=300)
        navRoot.place(x=-300, y=0)
        tk.Label(navRoot, font="Bahnschrift 15", bg="#58636F", fg="black", height=2, width=300, padx=20).place(x=0, y=0)

            # set y-coordinate of Navbar widgets:
        y = 80
  
        tk.Button(navRoot, text="Restart", font="17",bg="gray17", fg="white", activebackground="gray17", activeforeground="green", bd=0, command=restart).place(x=25, y=y)
        tk.Button(navRoot, text="Save", font="17",bg="gray17", fg="white", activebackground="gray17", activeforeground="green", bd=0,command =save).place(x=25, y=115) 
        tk.Button(navRoot, text="Load", font="17",bg="gray17", fg="white", activebackground="gray17", activeforeground="green", bd=0,command=load).place(x=25, y=150)
        tk.Button(navRoot, text="About", font="17",bg="gray17", fg="white", activebackground="gray17", activeforeground="green", bd=0,command=credit).place(x=25, y=185)
        tk.Button(navRoot, text="Exit", font="17",bg="gray17", fg="white", activebackground="gray17", activeforeground="green", bd=0,command=root.quit).place(x=25, y=220)
       
        y += 40 

            # Navbar Close Button:
        closeBtn = tk.Button(navRoot, image=closeIcon, bg="#58636F", activebackground="#58636F", bd=0, command=switch)
        closeBtn.place(x=250, y=10)   
                             
        root.mainloop()



    endSplash = Button(window, text="NEW GAME",background ="#58636F", fg ="#33B5E5", height = 3,width=15, command=start, borderwidth=2)
    endSplash.place(x=500, y=295)

    endSplash1 = Button(window, text="LOAD GAME",background ="#58636F", fg ="#33B5E5", height = 3,width=15,command=load, borderwidth=2)
    endSplash1.place(x=500, y=375)

    endSplash2 = Button(window, text="EXIT", background ="#58636F", fg ="#33B5E5", height = 3,width=15,borderwidth=2, command=window.quit)
    endSplash2.place(x=500, y=455)

    window.mainloop()




if __name__ == "__main__":
    main()