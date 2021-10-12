from tkinter import *
import tkinter as tk
import numpy as np
import math
import random
from PIL import ImageTk, Image
from numpy.core.numerictypes import obj2sctype
from data.misc.tkinter_custom_button import TkinterCustomButton
import sqlite3
import pandas as pd

class CHESSBOARD:
    board, valid_moves_array = np.empty((9,9), dtype="<U10"), np.empty((9,9), dtype="<U10")
    x1, y1 = -1, -1
    br, bkn, bb, bq, bk, bp, wr, wkn, wb, wq, wk, wp = "", "", "", "", "", "", "", "", "", "", "", ""
    color1, color2, color3, color4, color5 = "#706677", "#ccb7ae", "#eefaac", "#4bc96c", "#9c1e37"
    rows, columns = 8, 8
    dim_square = 64
    top_offset, side_offset = 200, 400
    width = columns * dim_square + side_offset
    height = rows * dim_square + top_offset
    dice_val = "5"
    fake_roll_val, fake_roll_time_interval = 5, 1
    turn = 0
    selected_piece = ["", ""]
    white_kill, black_kill = 1, 1
    db_loc = './data/db/'
    conn = ""
    cursor = ""
    table = ""

    def __init__(self, parent):
        canvas_width = self.width
        canvas_height = self.height
        self.canvas = tk.Canvas(parent, width=canvas_width, height=canvas_height)
        self.canvas.pack(padx=8, pady=8)
        self.draw_board()
        self.pieces()
        self.corps_rectangles()
        self.history_box()
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

    def checkerboard_color(self, intCheck):
        if intCheck % 2 == 0:
            return self.color1
        else:
            return self.color2

    def pieces(self):
        self.br = PhotoImage(file="./data/pieces/br.png")
        lbr1, lbr2 = "11", "81"
        self.add_piece(self.br, lbr1, "br1")
        self.add_piece(self.br, lbr2, "br2")

        self.bkn = PhotoImage(file="./data/pieces/bkn.png")
        lbkn1, lbkn2 = "21", "71"
        self.add_piece(self.bkn, lbkn1, "bkn1")
        self.add_piece(self.bkn, lbkn2, "bkn2")

        self.bb = PhotoImage(file="./data/pieces/bb.png")
        lbb1, lbb2 = "31", "61"
        self.add_piece(self.bb, lbb1, "bb1")
        self.add_piece(self.bb, lbb2, "bb2")

        self.bq = PhotoImage(file="./data/pieces/bq.png")
        lbq = "41"
        self.add_piece(self.bq, lbq, "bq")

        self.bk = PhotoImage(file="./data/pieces/bk.png")
        lbk = "51"
        self.add_piece(self.bk, lbk, "bk")

        
        self.bp = PhotoImage(file="./data/pieces/bp.png")
        lbp1, lbp2, lbp3, lbp4, lbp5, lbp6, lbp7, lbp8 = "12", "22", "32", "42", "52", "62", "72", "82"
        self.add_piece(self.bp, lbp1, "bp1")
        self.add_piece(self.bp, lbp2, "bp2")
        self.add_piece(self.bp, lbp3, "bp3")
        self.add_piece(self.bp, lbp4, "bp4")
        self.add_piece(self.bp, lbp5, "bp5")
        self.add_piece(self.bp, lbp6, "bp6")
        self.add_piece(self.bp, lbp7, "bp7")
        self.add_piece(self.bp, lbp8, "bp8")
        
        
        self.wr = PhotoImage(file='./data/pieces/wr.png')
        lwr1, lwr2 = "18", "88"
        self.add_piece(self.wr, lwr1, "wr1")
        self.add_piece(self.wr, lwr2, "wr2")

        self.wkn = PhotoImage(file="./data/pieces/wkn.png")
        lwkn1, lwkn2 = "28", "78"
        self.add_piece(self.wkn, lwkn1, "wkn1")
        self.add_piece(self.wkn, lwkn2, "wkn2")

        self.wb = PhotoImage(file="./data/pieces/wb.png")
        lwb1, lwb2 = "38", "68"
        self.add_piece(self.wb, lwb1, "wb1")
        self.add_piece(self.wb, lwb2, "wb2")

        self.wq = PhotoImage(file="./data/pieces/wq.png")
        lwq = "48"
        self.add_piece(self.wq, lwq, "wq")

        self.wk = PhotoImage(file="./data/pieces/wk.png")
        lwk = "58"
        self.add_piece(self.wk, lwk, "wk")

        self.wp = PhotoImage(file="./data/pieces/wp.png")
        lwp1, lwp2, lwp3, lwp4, lwp5, lwp6, lwp7, lwp8 = "17", "27", "37", "47", "57", "67", "77", "87"
        self.add_piece(self.wp, lwp1, "wp1")
        self.add_piece(self.wp, lwp2, "wp2")
        self.add_piece(self.wp, lwp3, "wp3")
        self.add_piece(self.wp, lwp4, "wp4")
        self.add_piece(self.wp, lwp5, "wp5")
        self.add_piece(self.wp, lwp6, "wp6")
        self.add_piece(self.wp, lwp7, "wp7")
        self.add_piece(self.wp, lwp8, "wp8")

    def corps_rectangles(self):
        self.canvas.create_rectangle(2, 90, 190, 85, fill = '#a60314', tag = "corpsb1g")
        self.canvas.create_rectangle(195, 90, 320, 85, fill = '#a60314', tag = "corpsb2g") # black red
        self.canvas.create_rectangle(325, 90, 510, 85, fill = '#a60314', tag = "corpsb3g")
        self.canvas.create_rectangle(2, 90, 190, 85, fill = '#00a835', tag = "corpsb1r")
        self.canvas.create_rectangle(195, 90, 320, 85, fill = '#00a835', tag = "corpsb2r") # black green
        self.canvas.create_rectangle(325, 90, 510, 85, fill = '#00a835', tag = "corpsb3r")

        self.canvas.create_rectangle(2, 625, 190, 620, fill = '#a60314', tag = "corpsw1g")
        self.canvas.create_rectangle(195, 625, 320, 620, fill = '#a60314', tag = "corpsw2g") # white red
        self.canvas.create_rectangle(325, 625, 510, 620, fill = '#a60314', tag = "corpsw3g")
        self.canvas.create_rectangle(2, 625, 190, 620, fill = '#00a835', tag = "corpsw1r")
        self.canvas.create_rectangle(195, 625, 320, 620, fill = '#00a835', tag = "corpwb2r") # white green
        self.canvas.create_rectangle(325, 625, 510, 620, fill = '#00a835', tag = "corpwb3r")
    
    def history_box(self):
        self.canvas.create_rectangle(525, 291, 913, 612, outline='black')

    def roll_value(self):
        self.dice_val = random.randrange(1,6)
        return self.dice_val

    def init_dice(self):
        # beginning image
        self.dice1 = ImageTk.PhotoImage(Image.open("data/die/dice1.png").resize((64, 64), Image.ANTIALIAS))
        self.canvas.create_image(self.width - 192, self.height / 5.4, image=self.dice1 , tag="dice")

    def rule_set(self, spiece):
        if(spiece[0][:-1] == "bp"):
            if(int(spiece[0][2]) <= 3):
                return [1, spiece[0][0], spiece[0][1], 1] #distance can travel, team, piece, corps
            if(int(spiece[0][2]) == 4 or int(spiece[0][2]) == 5):
                return [1, spiece[0][0], spiece[0][1], 2]
            if(int(spiece[0][2]) >= 6):
                return [1, spiece[0][0], spiece[0][1], 3]

        if(spiece[0][:-1] == "wp"):
            if(int(spiece[0][2]) <= 3):
                return [1, spiece[0][0], spiece[0][1], 1]
            if(int(spiece[0][2]) == 4 or int(spiece[0][2]) == 5):
                return [1, spiece[0][0], spiece[0][1], 2]
            if(int(spiece[0][2]) >= 6):
                return [1, spiece[0][0], spiece[0][1], 3]

        if(spiece[0][:-1] == "br"):
            return [2, spiece[0][0], spiece[0][1], 2]


        if(spiece[0][:-1] == "wr"):
            return [2, spiece[0][0], spiece[0][1], 2]


        if(spiece[0][:-1] == "bkn"):
            if(int(spiece[0][3]) == 1):
                return [4, spiece[0][0], str(spiece[0][1]) + str(spiece[0][2]), 1]
            if(int(spiece[0][3]) == 2):
                return [4, spiece[0][0], str(spiece[0][1]) + str(spiece[0][2]), 3]

        if(spiece[0][:-1] == "wkn"):
            if(int(spiece[0][3]) == 1):
                return [4, spiece[0][0], str(spiece[0][1]) + str(spiece[0][2]), 1]
            if(int(spiece[0][3]) == 2):
                return [4, spiece[0][0], str(spiece[0][1]) + str(spiece[0][2]), 3]

        if(spiece[0][:-1] == "bb"):
            if(int(spiece[0][2]) == 1):
                return [2, spiece[0][0], spiece[0][1], 1]
            if(int(spiece[0][2]) == 2):
                return [2, spiece[0][0], spiece[0][1], 3]

        if(spiece[0][:-1] == "wb"):
            if(int(spiece[0][2]) == 1):
                return [2, spiece[0][0], spiece[0][1], 1]
            if(int(spiece[0][2]) == 2):
                return [2, spiece[0][0], spiece[0][1], 3]

        if(spiece[0] == "bq"):
            return [3, spiece[0][0], spiece[0][1], 2]

        if(spiece[0] == "wq"):
            return [3, spiece[0][0], spiece[0][1], 2]

        if(spiece[0] == "bk"):
            return [3, spiece[0][0], spiece[0][1], 2]

        if(spiece[0] == "wk"):
            return [3, spiece[0][0], spiece[0][1], 2]

    def highlight_green(self, x, y, color):
        self.canvas.create_rectangle(((x - 1) * 64) +4, ((y) * 64) + 37, 
            ((x - 1) * 64) + self.dim_square, (y * 64) + self.dim_square + 35, 
            fill = color, tag = "move_locations")
        self.canvas.tag_lower("move_locations")
        self.canvas.tag_lower("board")

    def valid_moves(self, dist):

        '''
        nw, n, ne, e, se, s, sw, w = [1, -1, -1], [1, 0, 1], [1, 1, -1], [1, 1, 0], [1, 1, 1], [1, 0, -1], [1, -1, 1], [1, -1, 0]
        #spiece = [self.board[self.x1][self.y1], str(self.x1) + str(self.y1)]
        #team = dist[1]
        #spiece = ""
        self.valid_moves_arrayF(nw, dist)
        self.valid_moves_arrayF(n, dist)
        self.valid_moves_arrayF(ne, dist)
        self.valid_moves_arrayF(e, dist)
        self.valid_moves_arrayF(se, dist)
        self.valid_moves_arrayF(s, dist)
        self.valid_moves_arrayF(sw, dist)
        self.valid_moves_arrayF(w, dist)
        '''

        if(dist[2] == 'p'):
            self.valid_moves_arrayP(dist)
            return

        elif(dist[2] == 'r'):
            self.valid_moves_arrayP(dist)
            return

        else:
            self.valid_moves_arrayE(dist)
            return

    def valid_moves_arrayP(self, dist):
        tmodifier = 0
        if (dist[1] == "w"): tmodifier = -1
        if (dist[1] == "b"): tmodifier = 1
        try:
            for x in range(-1, 2, 1):
                xsearch = str(self.x1 + x)
                ysearch = str(self.y1 + tmodifier)
                xysearch = xsearch + ysearch
                if (self.bounds_check(xsearch) == True):
                    if (self.bounds_check(ysearch) == True):
                        print("xysearch: ", xysearch)
                    
        except:
            return

    def valid_moves_arrayR(self, dist):
        return

    def valid_moves_arrayE(self, dist):
        return

    def bounds_check(self, x):
        if(int(x[0][0]) > 0 and int(x[0][0]) < 9):
            return True

    '''
    def valid_moves_arrayF(self, cr, dist):

        team = dist[1]
        spiece = ""
        try:
            for x in range(1, dist[0] + 1):
                if (cr[0] == 1):
                    spiece = [self.board[self.x1 - (x * cr[1])][self.y1 - (x * cr[2])], str(self.x1 - (x * cr[1])) + str(self.y1 - (x * cr[2]))]
                    if(int(spiece[1][0]) > 0 and int(spiece[1][0]) < 9):
                        if(int(spiece[1][1]) > 0 and int(spiece[1][1]) < 9):
                            if(spiece[0] != ""):
                                if(spiece[0][0] == team):
                                    cr[0] == 0
                                    self.valid_moves_array[self.x1 - (x*cr[1])][self.y1 - (x*cr[2])] = 0
                                    break
                                if(spiece[0][0] != team and spiece[0][0] != ""):
                                    cr[0] == 0
                                    self.valid_moves_array[self.x1 - (x*cr[1])][self.y1 - (x*cr[2])] = 2
                                    self.highlight_green(int(spiece[1][0]), int(spiece[1][1]), self.color5)
                                    break
                            if(spiece[0] == ""):
                                self.valid_moves_array[self.x1 - (x*cr[1])][self.y1 - (x*cr[2])] = 1
                                self.highlight_green(int(spiece[1][0]), int(spiece[1][1]), self.color4)
        except:
            return
    '''

    def ret_piece_name(self, x): # method for returning piece name without number, ie wb1 returns wb, bk returns bk
        if(x[-1:].isnumeric()):
            return x[:-1]
        else:
            return x

    def add_piece(self, img, location, piece): # places an image of a certain piece on the canvas
        self.canvas.delete("piece_selected")
        self.canvas.delete("move_locations")
        posx = int(location[0])
        posy = int(location[1])
        self.board[posx][posy] = piece
        offset_x = 32
        offset_y = 132
        self.canvas.create_image(offset_x * ((posx*2)-1), offset_y + (self.dim_square * (posy-1)), 
            image=img, anchor="center", tag=piece)
        
    def del_piece(self, old_piece):
        # del_piece is invoked twice if an attacking move, once if a valid move
        # on an attacking move, the second conditional is invoked first to delete the attacked piece's image and then recreate it in the graveyard
        # and then a second time on the first conditional to delete the image of the piece being moved 
        # and then clear it's former location from the 'board' logic array that shows all pieces names
        # on a non-attacking move it only hits the first conditional
        if(old_piece[0].isnumeric() != True): 
            x, y = int(old_piece[1][0]), int(old_piece[1][1]) # select the coordinates of the piece that is being moved
            self.canvas.delete(old_piece[0]) # delete the picture of the piece from the previous slot
            self.board[x][y] = "" # clear the piece's former location from the logic array 'board' that shows all pieces names
        else: 
            self.canvas.delete(self.board[int(old_piece[0])][int(old_piece[1])])
            print(self.ret_piece_name(self.board[int(old_piece[0])][int(old_piece[1])]))
            img = eval("self." + self.ret_piece_name(self.board[int(old_piece[0])][int(old_piece[1])]))
            if(self.board[int(old_piece[0])][int(old_piece[1])][0] == "b"):
                self.canvas.create_image(32 * (self.black_kill) - 15, 675, 
                    image=img, anchor="center", tag=self.board[int(old_piece[0])][int(old_piece[1])][0] + "graveyard")
                self.black_kill += 1.6
            if(self.board[int(old_piece[0])][int(old_piece[1])][0] == "w"):
                self.canvas.create_image(32 * (self.white_kill) - 15, 50, 
                        image=img, anchor="center", tag=self.board[int(old_piece[0])][int(old_piece[1])][0] + "graveyard")
                self.white_kill += 1.6

    def coord_convert(self, x): # converts the integer based arry method used in this program to A-H horizontally and 8-1 vertically
        y = str(chr(int(x[0])+64))
        z = str(abs(int(x[1]) - 9))
        return y + z

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


def on_click(event, chessboard):

    chessboard.conn = sqlite3.connect(chessboard.db_loc + 'history.db') #DB set up
    chessboard.cursor = chessboard.conn.cursor()
    chessboard.table = """CREATE TABLE IF NOT EXISTS HISTORY(PIECE, PFROM, PTO, DEVCOORDS, PKILL, DICEROLL, KILLORNO);"""
    chessboard.cursor.execute(chessboard.table)

    # If the location clicked has a value of 1 or 2 on the valid_moves_array array (1 being free space, 2 being attack option)
    if(chessboard.valid_moves_array[chessboard.x1][chessboard.y1] == str(1) or chessboard.valid_moves_array[chessboard.x1][chessboard.y1] == str(2)):
        if(chessboard.valid_moves_array[chessboard.x1][chessboard.y1] == str(2)):
            chessboard.del_piece(str(chessboard.x1) + str(chessboard.y1)) # invokes del_piece method for removing the attacked piece visually and recreating it in the graveyard
        proper_loc_from = chessboard.coord_convert(chessboard.selected_piece[1]) # convert 'from' tile to Letter Number format
        proper_loc_to = chessboard.coord_convert(str(chessboard.x1) + str(chessboard.y1)) # 'to' tile to Letter Number format
        chessboard.cursor.execute("INSERT INTO HISTORY VALUES (?, ?, ?, ?, ?, ?, ?)", # insert data into db
                                (chessboard.selected_piece[0], proper_loc_from, proper_loc_to, str(chessboard.x1) + str(chessboard.y1), 
                                    chessboard.board[chessboard.x1][chessboard.y1], "", ""))
        chessboard.conn.commit()
        chessboard.conn.close()
        img = eval("chessboard." + chessboard.ret_piece_name(chessboard.selected_piece[0])) 
        chessboard.del_piece(chessboard.selected_piece) # removes piece from it's former location visually and clears it's location from the 'board' array
        chessboard.add_piece(img, str(chessboard.x1) + str(chessboard.y1), chessboard.selected_piece[0]) # recreates the piece visually in the new location
        chessboard.valid_moves_array = np.empty((9,9), dtype="<U10") # clears the array of valid moves
        print(np.rot90(np.fliplr(chessboard.board)))
        return

    # portion of on_click selecting pieces rather than moving them
    chessboard.conn.close()
    chessboard.valid_moves_array = np.empty((9,9), dtype="<U10") # clears the array of valid moves
    chessboard.canvas.delete("piece_selected") # deletes the yellow highlight
    chessboard.canvas.delete("move_locations") # deletes the green highlight
    chessboard.selected_piece = ["", ""]
    x, y = event.x - 2, event.y - 100 # adjusts the x and y clicks within the board itself
    if x > 0 and x <= 512 and y > 0 and y <= 512: # check if the click is within the board
        if(chessboard.board[chessboard.x1][chessboard.y1] != ""): # if the tile selected has a piece create a yellow rectangle around the tile highlighting it
            chessboard.canvas.create_rectangle(((chessboard.x1 - 1) * 64) +4, ((chessboard.y1) * 64) + 37, 
                ((chessboard.x1 - 1) * 64) + chessboard.dim_square, (chessboard.y1 * 64) + chessboard.dim_square + 35, 
                fill = chessboard.color3, tag = "piece_selected")
            chessboard.selected_piece = [chessboard.board[chessboard.x1][chessboard.y1], str(chessboard.x1) + str(chessboard.y1)] # piece name and location, ie wp7, 27
            dist = chessboard.rule_set(chessboard.selected_piece) # gather distance can move, team, piece name and corps
            print("dist:" , dist)
            chessboard.valid_moves(dist) # updates the valid_moves_array which shows what tiles the piece that's selected can move to
        piece = chessboard.board[chessboard.x1][chessboard.y1]
        chessboard.canvas.tag_raise(piece) # makes sure the piece isn't overlapped by highlighted tiles visually
        #print(np.rot90(np.fliplr(chessboard.board)))
    #print("chessboard.selected_piece:" , chessboard.selected_piece)
    print("", np.rot90(np.fliplr(chessboard.valid_moves_array)))

#def on_right_click(event, chessboard):
    #piece = chessboard.board[chessboard.x1][chessboard.y1]
    #chessboard.canvas.delete(piece)
    #chessboard.board[chessboard.x1][chessboard.y1] = ""

def motion(event, chessboard): # creates a unique yellow tile over the currently highlighted tile
    x, y = event.x - 2, event.y - 100
    over = math.ceil(x/64)+64 
    down = abs(math.ceil(y/64) - 9)
    overChar = chr(over)
    chessboard.canvas.delete("hlight")
    piece = chessboard.board[chessboard.x1][chessboard.y1]
    if x > 0 and x <= 512 and y > 0 and y <= 512:
        chessboard.loc = str(overChar) + str(down)
        CHESSBOARD.x1 = over-64
        CHESSBOARD.y1 = abs(down-9)
        chessboard.canvas.create_rectangle(((chessboard.x1 - 1) * 64) +4, ((chessboard.y1) * 64) + 37, 
            ((chessboard.x1 - 1) * 64) + chessboard.dim_square, (chessboard.y1 * 64) + chessboard.dim_square + 35, 
            fill = chessboard.color3, tag = "hlight")
        chessboard.canvas.tag_raise("move_locations")
        chessboard.canvas.tag_raise(piece)
        chessboard.canvas.lower("move_locations")
        chessboard.canvas.lower("board")

def main():
    root = tk.Tk()
    root.title('Fuzzy-Logic Medieval Chess')
    chessboard = CHESSBOARD(root)
    icon = PhotoImage(file="./data/misc/mainIcon.png")
    root.iconphoto(False, icon)
    root.resizable(False, False)
    chessboard.conn = sqlite3.connect(chessboard.db_loc + 'history.db')
    chessboard.cursor = chessboard.conn.cursor()
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
    rules_button.place(relx=0.57, rely=0.26)
    history_button.place(relx=0.57, rely=0.33)
    try:
        chessboard.cursor.execute('DROP TABLE HISTORY;')
        chessboard.conn.commit
    except:
            print("No table")
    chessboard.conn.close
    root.bind("<Motion>", lambda event: motion(event, chessboard))
    root.bind("<Button-1>", lambda event: on_click(event, chessboard))
    #root.bind('<Button-3>', lambda event: on_right_click(event, chessboard))
    root.mainloop()

if __name__ == "__main__":
    main()