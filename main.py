from tkinter import *
import tkinter as tk
import numpy as np
import os
import math
import time
import random
import sqlite3
import random
from PIL import ImageTk, Image
from pieces import Piece
from chessAI import ChessAI, RandomAI
from data.misc.tkinter_custom_button import TkinterCustomButton
import sys

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
    white_kill, black_kill = 1, 1
    whiteAI, BlackAI = False, False
    db_loc = './data/db/'
    cursor = ""
    conn = ""
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
        self.dice1 = ImageTk.PhotoImage(Image.open("data/die/dice1.png").resize((80, 80), Image.ANTIALIAS))
        self.dice2 = ImageTk.PhotoImage(Image.open("data/die/dice2.png").resize((80, 80), Image.ANTIALIAS))
        self.dice3 = ImageTk.PhotoImage(Image.open("data/die/dice3.png").resize((80, 80), Image.ANTIALIAS))
        self.dice4 = ImageTk.PhotoImage(Image.open("data/die/dice4.png").resize((80, 80), Image.ANTIALIAS))
        self.dice5 = ImageTk.PhotoImage(Image.open("data/die/dice5.png").resize((80, 80), Image.ANTIALIAS))
        self.dice6 = ImageTk.PhotoImage(Image.open("data/die/dice6.png").resize((80, 80), Image.ANTIALIAS))
        self.canvas.create_image(self.width - 350, self.height / 5, image=self.dice2 , tag="dice2")
        self.canvas.create_image(self.width - 350, self.height / 5, image=self.dice3 , tag="dice3")
        self.canvas.create_image(self.width - 350, self.height / 5, image=self.dice4 , tag="dice4")
        self.canvas.create_image(self.width - 350, self.height / 5, image=self.dice5 , tag="dice5")
        self.canvas.create_image(self.width - 350, self.height / 5, image=self.dice6 , tag="dice6")
        self.canvas.create_image(self.width - 350, self.height / 5, image=self.dice1 , tag="dice1")

    def rand_dice(self):
        return random.randrange(1,6)

    def add_piece(self, img, location, piece): # places an image of a certain piece on the canvas
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

    '''
    function
        rng 1-3

        if blackAI = True
            if black corps 1 is active
                ai = RandomAI()
                ...
            if black corps 2 is active
                ai = RandomAI()
                ...
            if black corps 3 is active
                time.sleep(3)
                ai = RandomAI() # returns piece id, array of 2
                ai.set_alive_pieces()
                ai.set_legal_moves()
                moveInfo = ai.move(randomCorps)
                pieceHeld = Piece.find_piece(moveInfo[0]) #pieceHeld is an object
                piece_move(pieceHeld, moveInfo[1]) # moveInfo[1] is a tuple
                delete ai
    '''

    def ai_function(self):
        print("Invoked")
        corpsOrder = []
        if self.BlackAI == False and self.whiteAI == False:
            return

        if self.BlackAI == True:
            c1Active = False
            c2Active = False
            c3Active = False
            for i in range(8):
                for j in range(8):
                    if Piece.chessboard[i][j] and Piece.chessboard[i][j].team == 1:
                        if Piece.chessboard[i][j].corps == 1 and Piece.chessboard[i][j].active == True: c1Active = True
                        if Piece.chessboard[i][j].corps == 2 and Piece.chessboard[i][j].active == True: c2Active = True
                        if Piece.chessboard[i][j].corps == 3 and Piece.chessboard[i][j].active == True: c3Active = True
            ai = RandomAI(1) # returns piece id, array of 2
            while True:
                if (c1Active == False and c2Active == False and c3Active == False): break
                randomCorps = random.randint(1, 3)
                if randomCorps not in corpsOrder:
                    corpsOrder.append(randomCorps)
                if len(corpsOrder) == 3:
                    break
            for i in range(3):
                if (c1Active == False and c2Active == False and c3Active == False): break
                #try:
                    #piece = self.return_corps(i+1, -1)
                time.sleep(0.5)
                ai.set_alive_pieces()
                ai.set_legal_moves()
                moveInfo = ai.move(corpsOrder[i])
                pieceHeld = Piece.find_piece(moveInfo[0]) #pieceHeld is an object
                if corpsOrder[i] == 1 and c1Active == True:
                    self.piece_move(list(moveInfo[1]), pieceHeld) # moveInfo[1] is a tuple
                elif corpsOrder[i] == 2 and c2Active == True:
                    self.piece_move(list(moveInfo[1]), pieceHeld)
                elif corpsOrder[i] == 3 and c3Active == True:
                    self.piece_move(list(moveInfo[1]), pieceHeld)
                #except:
                #    print("black shit's broke")
            corpsOrder = []
            del ai
        
        if self.whiteAI == True:
            c1Active = False
            c2Active = False
            c3Active = False
            for i in range(8):
                for j in range(8):
                    if Piece.chessboard[i][j] and Piece.chessboard[i][j].team == -1:
                        if Piece.chessboard[i][j].corps == 1 and Piece.chessboard[i][j].active == True: c1Active = True
                        if Piece.chessboard[i][j].corps == 2 and Piece.chessboard[i][j].active == True: c2Active = True
                        if Piece.chessboard[i][j].corps == 3 and Piece.chessboard[i][j].active == True: c3Active = True
            ai = RandomAI(-1) # returns piece id, array of 2
            while True:
                if (c1Active == False and c2Active == False and c3Active == False): break
                randomCorps = random.randint(1, 3)
                if randomCorps not in corpsOrder:
                    corpsOrder.append(randomCorps)
                if len(corpsOrder) == 3:
                    break
            for i in range(3):
                if (c1Active == False and c2Active == False and c3Active == False): break
                #try:
                    #piece = self.return_corps(i+1, -1)
                time.sleep(0.5)
                ai.set_alive_pieces()
                ai.set_legal_moves()
                moveInfo = ai.move(corpsOrder[i])
                pieceHeld = Piece.find_piece(moveInfo[0]) #pieceHeld is an object
                if corpsOrder[i] == 1 and c1Active == True:
                    self.piece_move(list(moveInfo[1]), pieceHeld) # moveInfo[1] is a tuple
                elif corpsOrder[i] == 2 and c2Active == True:
                    self.piece_move(list(moveInfo[1]), pieceHeld)
                elif corpsOrder[i] == 3 and c3Active == True:
                    self.piece_move(list(moveInfo[1]), pieceHeld)
                #except:
                #    print("white shit's broke")
            corpsOrder = []
            del ai

    # moveToCoords is a tuple
    def piece_move(self, moveToCoords, heldPiece):
        print("Move to coords: ", moveToCoords)
        print("Held piece: ", heldPiece)
        print("Held piece avail moves", heldPiece.availMoves)
        moveCheck = False
        attackCheck = False
        if tuple(moveToCoords) in heldPiece.availMoves: moveCheck = True
        if tuple(moveToCoords) in heldPiece.availAttacks: attackCheck = True
        
        print("moveCheck = ", moveCheck)
        print("attackCheck = ", attackCheck)

        Piece.diceVal = self.rand_dice()

        if (tuple(moveToCoords) not in heldPiece.availMoves and 
        tuple(moveToCoords) not in heldPiece.availAttacks):
            print("AAAAAAAAAAAAAAAAAAA")
            return

        #self.turn_forward(heldPiece)
        print("BBBBBBBBBBBB")

        if attackCheck == False and moveCheck: # moves with no attacks
            img = eval("self." # TODO: send to new method
                + heldPiece.pieceID[:-1])
            self.canvas.delete(heldPiece.pieceID)
            self.add_piece(img, tuple(moveToCoords), str(heldPiece.pieceID))
            heldPiece.move(moveToCoords[0], moveToCoords[1])
            self.cursor.execute("INSERT INTO HISTORY VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                                    (heldPiece.pieceID, str(heldPiece.corps), str(self.locationLock), str(moveToCoords), str(False), None, None, None, None, str(False), None))
            self.conn.commit()
        if moveCheck and attackCheck: # moves with attacks
            self.canvas.tag_raise("dice" + str(Piece.diceVal))
            pieceAttackedID = Piece.chessboard[moveToCoords[0]][moveToCoords[1]].pieceID
            b = heldPiece.capture(Piece.chessboard[moveToCoords[0]][moveToCoords[1]], False, False)
            if b:
                img = eval("self." # TODO: send to new method
                    + heldPiece.pieceID[:-1])
                gimg = eval("self." + Piece.chessboard[moveToCoords[0]][moveToCoords[1]].pieceID[:-1])
                self.graveyard(gimg, Piece.chessboard[moveToCoords[0]][moveToCoords[1]])
                self.canvas.delete(heldPiece.pieceID)

                self.canvas.delete(Piece.chessboard[moveToCoords[0]][moveToCoords[1]].pieceID)
                self.add_piece(img, tuple(moveToCoords), str(heldPiece.pieceID))
                heldPiece.capture(Piece.chessboard[moveToCoords[0]][moveToCoords[1]], True, False)
            self.cursor.execute("INSERT INTO HISTORY VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                                (heldPiece.pieceID, str(heldPiece.corps), str(self.locationLock), str(moveToCoords), str(True), Piece.diceVal, pieceAttackedID, None, None, str(False), None))
            self.conn.commit()
            
        if moveCheck == False and attackCheck: #rook attack from afar
            b = heldPiece.capture(Piece.chessboard[moveToCoords[0]][moveToCoords[1]], False, True)
            pieceAttackedID = Piece.chessboard[moveToCoords[0]][moveToCoords[1]].pieceID
            if b:
                gimg = eval("self." + Piece.chessboard[moveToCoords[0]][moveToCoords[1]].pieceID[:-1])
                self.graveyard(gimg, Piece.chessboard[moveToCoords[0]][moveToCoords[1]])
                self.canvas.delete(Piece.chessboard[moveToCoords[0]][moveToCoords[1]].pieceID)
                #Piece.chessboard[moveToCoords[0]][moveToCoords[1]].kill_piece()
                heldPiece.capture(Piece.chessboard[moveToCoords[0]][moveToCoords[1]], True, True)
            self.cursor.execute("INSERT INTO HISTORY VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                                (heldPiece.pieceID, str(heldPiece.corps), str(self.locationLock), str(self.locationLock), str(True), Piece.diceVal, pieceAttackedID, None, None, str(True), None))
            self.conn.commit()
        #print(Piece.chessboard)
        self.turn_forward(heldPiece)
        
        self.bishop_death("wb1")
        self.bishop_death("wb2")
        self.bishop_death("bb1")
        self.bishop_death("bb2")

        if ("wk1" in Piece.graveyard or "bk1" in Piece.graveyard):
            for i in range(8):
                for j in range(8):
                    if Piece.chessboard[i][j]:
                        Piece.chessboard[i][j].active = False
            print("Game over")
            ### TODO On Game Over, have a popup that lets the user know who won, and gives 2 buttons to click to restart or view history
            self.game_over_popup()
            self.canvas.tag_raise("corpsw1r")
            self.canvas.tag_raise("corpsw2r")
            self.canvas.tag_raise("corpsw3r")
            self.canvas.tag_raise("corpsb1r")
            self.canvas.tag_raise("corpsb2r")
            self.canvas.tag_raise("corpsb3r")

        
        self.locationLockedIn = False

    def bishop_death(self, piece):
        x, y = 0, 0
        if piece[0] == "w": x = -1
        if piece[0] == "b": x = 1
        if piece[2] == "1": y = 1
        if piece[2] == "2": y = 3
        if (piece in Piece.graveyard):
            for i in range(len(Piece.chessboard)):
                for j in range(len(Piece.chessboard[0])):
                    if Piece.chessboard[i][j] and Piece.chessboard[i][j].team == x and Piece.chessboard[i][j].corps == y:
                        Piece.chessboard[i][j].corps = 2
        

    def game_over_popup(self):
        win = Tk()
        win.geometry("375x100")
        win.title("")
        if ("wk1" in Piece.graveyard):
            Label(win, text= "Game over, black wins!", font=('Helvetica 18 bold')).place(x=20,y=20)
        if("bk1" in Piece.graveyard):
            Label(win, text= "Game over, white wins!", font=('Helvetica 18 bold')).place(x=20,y=20)

    def graveyard(self, img, piece):
        if piece.team == -1:
            self.canvas.create_image(32 * (self.white_kill) - 15, 50, 
                image=img, anchor="center")
            self.white_kill += 1.6
        if piece.team == 1:
            self.canvas.create_image(32 * (self.black_kill) - 15, 675, 
                image=img, anchor="center")
            self.black_kill += 1.6  
        
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
            
        if teamLetter + "b1" in Piece.graveyard:
            self.corpsPlayed[0] = 2
        if teamLetter + "b2" in Piece.graveyard:
            self.corpsPlayed[2] = 2

        self.canvas.lower(corpsIndicatorTag)

        if (self.corpsPlayed[0]==2 and self.corpsPlayed[1]==2 and self.corpsPlayed[2]==2):
            self.change_active_status(pieceObject.team * -1, pieceObject.corps, True)
            self.reset_corps_inidcator(pieceObject.team * -1)
         
        self.history_box_text()
        
    def history_box_text(self):
        self.canvas.delete("HistoryText")
        for i in range (1, 11):
            try:
                lastEntry = self.cursor.execute('select * from HISTORY').fetchall()[-1 * i]
                displayText = ""
                if lastEntry[0] == None:
                    displayText = "Turn over"
                print( lastEntry[3], lastEntry[4], lastEntry[8], lastEntry[9])
                if lastEntry[3] and lastEntry[4] == str(False) and lastEntry[7] == None and lastEntry[8] == None:
                    displayText = "Piece " + lastEntry[0] + " of corps " + lastEntry[1] + " moved from " + lastEntry[2] + " to " + lastEntry[3]
                if lastEntry[3] and lastEntry[4] == str(True) and lastEntry[7] == None and lastEntry[8] == None:
                    displayText = "Piece " + lastEntry[0] + " of corps " + lastEntry[1] + " attacked " + lastEntry[6] + " with a " + str(lastEntry[5]) + " roll on " + lastEntry[3] + " from " + lastEntry[2]
                if lastEntry[8] == str(True):
                    displayText = "Piece " + lastEntry[0] + " of corps " + lastEntry[1] + " passed their turn"
                if lastEntry[9] == str(True):
                    displayText = "Rook " + lastEntry[0] + " of corps " + lastEntry[1] + " attacked " + lastEntry[6] + " from afar with a roll of " + str(lastEntry[5])
                if lastEntry[7] != None:
                    displayText = "Piece " + lastEntry[0] + " of corps " + lastEntry[1] + " transfered to corps " + lastEntry[7]
                if "wk1" in Piece.graveyard:
                    displayText = "Game over! Black wins."
                if "bk1" in Piece.graveyard:
                    displayText = "Game over! White wins."
                self.canvas.create_text(530,285 + (i * 30),fill="black",font="Times 10",anchor="w",
                                        text=displayText, tag="HistoryText")
                # Game over overwrites everything here, maybe fix
            except Exception as e:
                print(e)
                return

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
        if "wb1" in Piece.graveyard:
            self.canvas.delete("corpsw1g")
            self.canvas.tag_raise("corpsw1r")
        if "wb2" in Piece.graveyard:
            self.canvas.delete("corpsw3g")
            self.canvas.tag_raise("corpsw3r")
        if "bb1" in Piece.graveyard:
            self.canvas.delete("corpsb1g")
            self.canvas.tag_raise("corpsw1r")
        if "bb2" in Piece.graveyard:
            self.canvas.delete("corpsb3g")
            self.canvas.tag_raise("corpsw3r")
        self.cursor.execute("INSERT INTO HISTORY VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (None, None, None, None, None, None, None, None, None, None, str(True)))
        self.conn.commit()

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
        
    def pass_turn(self):
        if(self.locationLockedIn):
            self.cursor.execute("INSERT INTO HISTORY VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                                    (Piece.chessboard[self.locationLock[0]][self.locationLock[1]].pieceID, str(Piece.chessboard[self.locationLock[0]][self.locationLock[1]].corps), None, None, None, None, None, None, str(True), None, None))
            self.conn.commit()
            self.turn_forward(Piece.chessboard[self.locationLock[0]][self.locationLock[1]])
        return
    
    def transfer_action(self, corpsToMoveTo, locLockX, locLockY, top):
        self.cursor.execute("INSERT INTO HISTORY VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                        (Piece.chessboard[locLockX][locLockY].pieceID, str(Piece.chessboard[locLockX][locLockY].corps), None, None, None, None, None, str(corpsToMoveTo), None, None, None))
        self.conn.commit()
        self.turn_forward(Piece.chessboard[locLockX][locLockY])
        Piece.chessboard[locLockX][locLockY].corps = corpsToMoveTo
        
        for i in range(len(Piece.chessboard)):
                for j in range(len(Piece.chessboard[0])):
                    if Piece.chessboard[i][j] and Piece.chessboard[i][j].team == Piece.chessboard[locLockX][locLockY].team:
                        if Piece.chessboard[i][j].corps == Piece.chessboard[locLockX][locLockY].corps and Piece.chessboard[i][j].pieceID != Piece.chessboard[locLockX][locLockY].pieceID:
                            if Piece.chessboard[i][j].active:
                                Piece.chessboard[locLockX][locLockY].active = True
                                break
        top.destroy()
        return
    
    def transfer(self):
        k, l = 0, 0
        kBool, lBool = False, False
        coreList = [1, 2, 3]
        if(self.locationLockedIn):
            if "wk1" in Piece.chessboard[self.locationLock[0]][self.locationLock[1]].pieceID or "bk1" in Piece.chessboard[self.locationLock[0]][self.locationLock[1]].pieceID:
                return
            coreList.remove(Piece.chessboard[self.locationLock[0]][self.locationLock[1]].corps)
            print(coreList)
            top = Toplevel()
            top.geometry("325x50")
            top.title('Transfer from corps ' + str(Piece.chessboard[self.locationLock[0]][self.locationLock[1]].corps))
            for i in range(len(Piece.chessboard)):
                for j in range(len(Piece.chessboard[0])):
                    if Piece.chessboard[i][j]:
                        if (Piece.chessboard[i][j].corps == coreList[0] and
                            Piece.chessboard[i][j].team == Piece.chessboard[self.locationLock[0]][self.locationLock[1]].team):
                            k+=1
                            if k >= 6:
                                kBool = True
                        if (Piece.chessboard[i][j].corps == coreList[1] and
                            Piece.chessboard[i][j].team == Piece.chessboard[self.locationLock[0]][self.locationLock[1]].team):
                            l+=1
                            if l >= 6:
                                lBool = True
            if not kBool:
                if (Piece.chessboard[self.locationLock[0]][self.locationLock[1]].pieceID[0] + "b1" not in Piece.graveyard):
                    tk.Button(top,text="Transfer to corps " + str(coreList[0]), width = 22, 
                            command=lambda: self.transfer_action(coreList[0], self.locationLock[0], self.locationLock[1], top)).pack(side=LEFT)
            if not lBool:
                if (Piece.chessboard[self.locationLock[0]][self.locationLock[1]].pieceID[0] + "b2" not in Piece.graveyard):
                    tk.Button(top,text="Transfer to corps " + str(coreList[1]), width = 22, 
                            command=lambda: self.transfer_action(coreList[1], self.locationLock[0], self.locationLock[1], top)).pack(side=RIGHT)
            if Piece.chessboard[self.locationLock[0]][self.locationLock[1]].corps == 1:
                tk.Button(top,text="Transfer to corps " + str(coreList[0]), width = 22, 
                          command=lambda: self.transfer_action(coreList[0], self.locationLock[0], self.locationLock[1], top)).pack(side=LEFT)
            if Piece.chessboard[self.locationLock[0]][self.locationLock[1]].corps == 3:
                tk.Button(top,text="Transfer to corps " + str(coreList[1]), width = 22, 
                          command=lambda: self.transfer_action(coreList[1], self.locationLock[0], self.locationLock[1], top)).pack(side=RIGHT)

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
        # chessboard.canvas.delete("copsHlight")      # typo?
        return
    if chessboard.locationLockedIn:
        # chessboard.piece_move([yLoc, xLoc])
        chessboard.piece_move([yLoc, xLoc], Piece.chessboard[chessboard.locationLock[0]][chessboard.locationLock[1]])
        chessboard.locationLock = [None]
        chessboard.locationLockedIn = False

def motion(event, chessboard): # creates a unique yellow tile over the currently highlighted tile
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

# TODO: restart game, 
# create a function outside of CHESSBOARD that gets called in game_over_popup
# this function deletes the old board, generates a new board, and displays it
# without extending the canvas

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
        chessboard.conn = sqlite3.connect(chessboard.db_loc + 'history.db')
        chessboard.cursor = chessboard.conn.cursor()
        try:
            chessboard.cursor.execute('DROP TABLE HISTORY;')
            chessboard.conn.commit
        except:
            print("No table")
        table = """CREATE TABLE IF NOT EXISTS HISTORY(PIECEID, CORPS, PIECEFROM, PIECETO, ATTACKORNO, DICE, ATTACKEDPIECE, TRANSFERTO, PASS, ROOKEXCEPTION, NEXTTURN);"""
        chessboard.cursor.execute(table)
        root.bind("<Motion>", lambda event: motion(event, chessboard))
        root.bind("<Button-1>", lambda event: on_click(event, chessboard))

        def white_ai():
            '''
            if chessboard.whiteAI == False:
                white_ai_button.set_text("White AI: On")
                chessboard.whiteAI = True
                chessboard.ai_function()
            elif chessboard.whiteAI == True:
                white_ai_button.set_text("White AI: Off") 
                chessboard.whiteAI = False
            '''
            
            if chessboard.whiteAI == False:
                chessboard.whiteAI = True
                chessboard.ai_function()
                chessboard.whiteAI = False
            
        


        def black_ai():
            '''
            if chessboard.BlackAI == False:
                black_ai_button.set_text("Black AI: On")
                chessboard.BlackAI = True
                chessboard.ai_function()
            elif chessboard.BlackAI == True:
                black_ai_button.set_text("Black AI: Off")
                chessboard.BlackAI = False
            '''
            if chessboard.BlackAI == False:
                chessboard.BlackAI = True
                chessboard.ai_function()
                chessboard.BlackAI = False

        rules_button = TkinterCustomButton(text="Rules", 
                                            bg_color=None,
                                            fg_color="#58636F",
                                            border_color=None,
                                            hover_color="#808B96",
                                            corner_radius=10,
                                            border_width=0,
                                            width= chessboard.width/4.64,
                                            hover=True,
                                            command=chessboard.rules_window)
        history_button = TkinterCustomButton(text="History", 
                                            bg_color=None,
                                            fg_color="#58636F",
                                            border_color=None,
                                            hover_color="#808B96",
                                            corner_radius=10,
                                            border_width=0,
                                            width= chessboard.width/4.64,
                                            hover=True)
        pass_button = TkinterCustomButton(text="Pass Turn", 
                                            bg_color=None,
                                            fg_color="#58636F",
                                            border_color=None,
                                            hover_color="#808B96",
                                            corner_radius=10,
                                            border_width=0,
                                            width= chessboard.width/4.75,
                                            hover=True,
                                            command=chessboard.pass_turn)
        transfer_button = TkinterCustomButton(text="Transfer", 
                                            bg_color=None,
                                            fg_color="#58636F",
                                            border_color=None,
                                            hover_color="#808B96",
                                            corner_radius=10,
                                            border_width=0,
                                            width= chessboard.width/4.75,
                                            hover=True,
                                            command=chessboard.transfer)
        black_ai_button = TkinterCustomButton(text="Black AI", 
                                            bg_color=None,
                                            fg_color="#58636F",
                                            border_color=None,
                                            hover_color="#808B96",
                                            corner_radius=10,
                                            border_width=0,
                                            width= chessboard.width/3,
                                            hover=True,
                                            command=black_ai)
        white_ai_button = TkinterCustomButton(text="White AI", 
                                            bg_color=None,
                                            fg_color="#58636F",
                                            border_color=None,
                                            hover_color="#808B96",
                                            corner_radius=10,
                                            border_width=0,
                                            width= chessboard.width/3,
                                            hover=True,
                                            command=white_ai)
        rules_button.place(relx=0.568, rely=0.26)
        history_button.place(relx=0.568, rely=0.32)
        transfer_button.place(relx=0.782, rely=0.26)
        pass_button.place(relx=0.782, rely=0.32)
        black_ai_button.place(relx=0.663, rely= 0.135)
        white_ai_button.place(relx=0.663, rely= 0.195)
        
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