import numpy as np
import pandas as pd
import copy
from collections import deque 
import random

class Piece:

    chessboard = np.empty((8, 8), dtype=object)

    captureData = pd.read_excel("./CaptureMatrix.xlsx", header=None, names=["King", "Queen", "Knight (h)", "Bishop", "Rook", "Pawn"])
    captureMatrix = captureData.to_numpy()

    pieceData = ['k', 'q', 'h', 'b', 'r', 'p']
    activePieces = []
    graveyard = []

    def __init__(self, id, type, team, corps, loc):
        self.pieceID = id
        self.pieceType = type
        self.team = team
        self.corps = corps
        self.location = loc
        self.active = True
        Piece.activePieces.append(self)

        if(type == "h"):
            self.moveDist = 4
        elif(type == "q" or type == "k"):
            self.moveDist = 3
        elif(type == "b"):
            self.moveDist = 2

        self.availMoves = []
        self.availAttacks = []
        self.check_moves()

    def check_moves(self):
        # function to check available moves. updates avail_moves array
        # moves array is a chessboard that shows available moves right now. Will show captures as piece values in future
        moves = copy.copy(Piece.chessboard)
        
        # self.location is array of 2 numbers [y, x] that gives piece location
        pieceLocY = self.location[0]
        pieceLocX = self.location[1]
        self.availMoves = []
        self.availAttacks = []
        team = self.team

        

        if(self.pieceType == 'p'):
            rowToCheck = pieceLocY + self.team
            # checking pawn moves
            for col in range(pieceLocX-1, pieceLocX+2):
                if(col < 0 or col >= 8):
                    continue
                if(rowToCheck < 0 or rowToCheck >= 8):
                    continue
                # if space not occupied, then legal move
                if moves[rowToCheck][col] == None:
                    # a legal move is represented by the number 'legal' Can change this later if confusing
                    # will likely need two for loop sets, one for black pieces, one for white. 
                    # Can solve this by using piece ID instead of number, and checking for team based on that
                    moves[rowToCheck][col] = "lg"
                    self.availMoves.append([rowToCheck, col])
                if (isinstance(moves[rowToCheck][col], Piece) and moves[rowToCheck][col].team is not self.team):
                    self.availAttacks.append([rowToCheck, col])
                    self.availMoves.append([rowToCheck, col])
        
        if(self.pieceType == 'b' or self.pieceType == 'k' or self.pieceType == 'q' or self.pieceType == 'h'):
            
            R, C = 8, 8

            start = [pieceLocY, pieceLocX]

            # use queue to track moves
            queue = deque()
            queue.appendleft((start[0], start[1], 0))
            directions = [[0, 1], [0, -1], [1, 0], [-1, 0], [-1, 1], [1, 1], [1, -1], [-1, -1]]
            visited = [[False] * C for _ in range(R)]


            while len(queue) != 0:
                coord = queue.pop()
                visited[coord[0]][coord[1]] = True

                for dir in directions:
                    nr, nc = coord[0]+dir[0], coord[1]+dir[1]
                    if (nr < 0 or nr >= R or nc < 0 or nc >= C or 
                    (isinstance(moves[nr][nc], Piece) and moves[nr][nc].team is self.team) 
                    or visited[nr][nc]): continue 
                    queue.appendleft((nr, nc, coord[2]+1))
                    if(queue[0][2] <= self.moveDist):
                        
                        self.availMoves.append([nr,nc])
                        # print(moves[nr][nc].team)
                        if(isinstance(moves[nr][nc], Piece) and moves[nr][nc].team is not self.team):
                            self.availAttacks.append([nr, nc])
                        else:
                            moves[nr][nc] = "lg"
                    # if(self.pieceType == 'h' and queue[0][2] == self.moveDist and moves[nr][nc].team is not self.team):
                     #   self.availAttacks.append([nr, nc])

        
        if(self.pieceType == 'r'):
            pieceLocX = self.location[0]
            pieceLocY = self.location[1]
            cr =   [[0, -1, 1],  # N
                    [1, -1, 1],  # NE
                    [1, 0, 1],   # E
                    [1, 1, 1],   # SE
                    [0, 1, 1],   # S
                    [-1, 1, 1],  # SW
                    [-1, 0, 1],  # W
                    [-1, -1, 1]] # NW

            for col in range (1, 3): # counter clockwise search that starts at the center and radiates out 2
                for x, i in enumerate(cr):
                    if (col == 2): x = x + 8
                    xSearch = pieceLocX + (col * i[1])
                    ySearch = pieceLocY + (col * i[0])
                    if (xSearch < 0 or xSearch > 7 or ySearch < 0 or ySearch > 7): # break if out of bounds
                        continue

                    #if piece is there, if on first ring of outward radiation, if on same team
                    if (moves[xSearch][ySearch] != None and col != 2 and moves[xSearch][ySearch].team == team):
                        i[2] = 0 # block availMoves for further rings
                    #if piece is there, if on first ring of outward radiation, if NOT on same team
                    if (moves[xSearch][ySearch] != None and col != 2 and moves[xSearch][ySearch].team != team):
                        self.availMoves.append([xSearch, ySearch])
                        self.availAttacks.append([xSearch, ySearch])
                        i[2] = 0
                    if (moves[xSearch][ySearch] == None and col != 2): # if no piece on first outward radiation
                        self.availMoves.append([xSearch, ySearch])

                    if (moves[xSearch][ySearch] != None and x > 7 and cr[x-8][2] == 0 
                        and moves[xSearch][ySearch].team != team):
                            self.availAttacks.append([xSearch, ySearch])
                    if (moves[xSearch][ySearch] == None and x > 7 and cr[x-8][2] == 1):
                        self.availMoves.append([xSearch, ySearch])
                    if (moves[xSearch][ySearch] != None and x > 7 and cr[x-8][2] == 1 and moves[xSearch][ySearch].team != team):
                        self.availMoves.append([xSearch, ySearch])
                        self.availAttacks.append([xSearch, ySearch])
            print("Avail Moves Rook: ", self.availMoves)
            print("Avail Attacks Rook: ", self.availAttacks)
        self.availMoves = self.remove_deuplicates(self.availMoves)
        self.availAttacks = self.remove_deuplicates(self.availAttacks)

        return moves

    def remove_deuplicates(self, lst):
        return [t for t in (set(tuple(i) for i in lst))]

    # takes board and moveLoc tuple (row, col)
    def move(self, newRow, newCol):
        # function that moves the piece
        # returns a new board
        newBoard = Piece.chessboard
        # print("New Board: ", newBoard)



        if((newRow, newCol) in self.availMoves):
            # clear current space
            newBoard[self.location[0]][self.location[1]] = None

            self.location = [newRow, newCol]
            
            newBoard[newRow][newCol] = self
        elif((newRow, newCol) in self.availAttacks):
            self.capture(newBoard[newRow][newCol])

        return newBoard

    def capture(self, defender):
        print("In capture")
        # return boolean and new board?
        newBoard = Piece.chessboard
        result = False
        testDiceRoll = 6
        # realDiceRoll = CHESSBOARD.roll_value()
        # find index to use
        attackIndex = Piece.pieceData.index(self.pieceType)
        defenderIndex = Piece.pieceData.index(defender.pieceType)

        # use capture matrix with dice roll function to attempt capture,
        # on capture, set attacked square to null and call move on that square
        # unsuccessful, just return board

        if(str(testDiceRoll) in str(Piece.captureMatrix[attackIndex][defenderIndex])): # and self.pieceType != 'r'):
            result = True
            # then replace piece with attacker.
            
            defender.replace_piece(self)
            
            ''' OLD REPLACE CODE
            Piece.graveyard.append(defender)
            Piece.chessboard[defender.location[0]][defender.location[1]] = self
            '''

        '''# Rook exception done in main ?
        elif self.pieceType == 'r':
            
            Piece.graveyard.append(defender)
            Piece.chessboard[defender.location[0]][defender.location[1]] = None
            '''

        print("Graveyard: ", Piece.graveyard)
        print("Chessboard: \n", Piece.chessboard)

        return result, newBoard

    # use this for rook special case?
    def kill_piece(self):
        Piece.graveyard.append(self)
        Piece.activePieces.remove(self)
        Piece.chessboard[self.location[0]][self.location[1]] = None
        self.active = False
        return self

    # TAKES IN ATTACKER, NOT DEFENDER (defender is self)
    def replace_piece(self, attacker):
        Piece.graveyard.append(self)
        Piece.activePieces.remove(self)
        Piece.chessboard[self.location[0]][self.location[1]] = attacker
        Piece.chessboard[attacker.location[0]][attacker.location[1]] = None
        attacker.location = [self.location[0], self.location[1]]
        self.active = False
        return self

    ### update moves... all pieces that are active, check their moves.
    ## def update moves?


    ### Piece scraper, scrapes chessboard for piece matching pieceID and returns Piece.chessboard[loc][loc]

    def eval_moves(self):
        # evaluates moves based on a heuristic
        # put wesley function here

        return 

    
    def gen_new_board():
        # [Row, Column], [Down, Over]

        # id, type, team (-1 = white, 1 = black), corps (1, 2, 3), loc (array)
        Piece.chessboard[6, 0] = Piece("wp1", "p", -1, 1, [6, 0])
        Piece.chessboard[6, 1] = Piece("wp2", "p", -1, 1, [6, 1]) 
        Piece.chessboard[6, 2] = Piece("wp3", "p", -1, 1, [6, 2]) 
        Piece.chessboard[6, 3] = Piece("wp4", "p", -1, 2, [6, 3]) # white pawns
        Piece.chessboard[6, 4] = Piece("wp5", "p", -1, 2, [6, 4]) 
        Piece.chessboard[6, 5] = Piece("wp6", "p", -1, 3, [6, 5])
        Piece.chessboard[6, 6] = Piece("wp7", "p", -1, 3, [6, 6])
        Piece.chessboard[6, 7] = Piece("wp8", "p", -1, 3, [6, 7])

        Piece.chessboard[7, 0] = Piece("wr1", "r", -1, 2, [7, 0])
        Piece.chessboard[7, 7] = Piece("wr2", "r", -1, 2, [7, 7])
        Piece.chessboard[7, 1] = Piece("wh1", "h", -1, 1, [7, 1])
        Piece.chessboard[7, 6] = Piece("wh2", "h", -1, 3, [7, 6]) # white back row
        Piece.chessboard[7, 2] = Piece("wb1", "b", -1, 1, [7, 2]) 
        Piece.chessboard[7, 5] = Piece("wb2", "b", -1, 3, [7, 5])
        Piece.chessboard[7, 4] = Piece("wk1", "k", -1, 2, [7, 4])
        Piece.chessboard[7, 3] = Piece("wq1", "q", -1, 2, [7, 3])

        Piece.chessboard[1, 0] = Piece("bp1", "p", 1, 1, [1, 0])
        Piece.chessboard[1, 1] = Piece("bp2", "p", 1, 1, [1, 1])
        Piece.chessboard[1, 2] = Piece("bp3", "p", 1, 1, [1, 2]) 
        Piece.chessboard[1, 3] = Piece("bp4", "p", 1, 2, [1, 3]) # black pawns
        Piece.chessboard[1, 4] = Piece("bp5", "p", 1, 2, [1, 4])
        Piece.chessboard[1, 5] = Piece("bp6", "p", 1, 3, [1, 5])
        Piece.chessboard[1, 6] = Piece("bp7", "p", 1, 3, [1, 6])
        Piece.chessboard[1, 7] = Piece("bp8", "p", 1, 3, [1, 7])

        Piece.chessboard[0, 0] = Piece("br1", "r", 1, 2, [0, 0])
        Piece.chessboard[0, 7] = Piece("br2", "r", 1, 2, [0, 7])
        Piece.chessboard[0, 1] = Piece("bh1", "k", 1, 1, [0, 1])
        Piece.chessboard[0, 6] = Piece("bh2", "k", 1, 3, [0, 6]) # black back row
        Piece.chessboard[0, 2] = Piece("bb1", "b", 1, 1, [0, 2])
        Piece.chessboard[0, 5] = Piece("bb2", "b", 1, 3, [0, 5])
        Piece.chessboard[0, 4] = Piece("bk1", "k", 1, 2, [0, 4])
        Piece.chessboard[0, 3] = Piece("bq1", "q", 1, 2, [0, 3])
    

    def set_board(newBoard):
        Piece.chessboard = newBoard
    
    def __str__(self):
        return self.pieceID

    def __repr__(self):
        return self.pieceID

### board inside class testing

######## Piece.gen_new_board()

#print("Moving wp4\n", Piece.chessboard[6][3].move(5, 3))

# testing capture with replace_piece

# print(Piece.chessboard, "\nGraveyard:", Piece.graveyard, "\nActive Pieces", Piece.activePieces)
