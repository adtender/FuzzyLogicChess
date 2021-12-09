import numpy as np
import pandas as pd
import copy
from collections import deque 
import random

class Piece:

    chessboard = np.empty((8, 8), dtype=object)

    # captureData = pd.read_excel("./CaptureMatrix.xlsx", header=None, names=["King", "Queen", "Knight (h)", "Bishop", "Rook", "Pawn"])
    # captureMatrix = captureData.to_numpy()

    captureMatrix = [   [654, 654, 654, 654, 65, 654321],
                        [654, 654, 654, 654, 65, 65432],
                        [65, 65, 65, 65, 65, 65432],
                        [65, 65, 65, 654, 65, 6543],
                        [654, 654, 654, 65, 65, 65],
                        [6, 6, 6, 65, 6, 654]
                    ]

    pieceData = ['k', 'q', 'h', 'b', 'r', 'p']
    activePieces = []
    graveyard = []
    diceVal = 0

    def __init__(self, id, type, team, corps, loc, active):
        self.pieceID = id
        self.pieceType = type
        self.team = team
        self.corps = corps
        self.location = loc
        self.active = active        # corps active or not
        Piece.activePieces.append(self)
        self.surprise = False

        if(type == "h"):
            self.moveDist = 4
        elif(type == "q" or type == "k"):
            self.moveDist = 3
        elif(type == "b"):
            self.moveDist = 2

        self.availMoves = []
        self.availAttacks = []

    def check_moves(self):
        # function to check available moves. updates avail_moves array
        # moves array is a chessboard that shows available moves right now. Will show captures as piece values in future
        moves = copy.copy(Piece.chessboard)
        
        # self.location is array of 2 numbers [y, x] that gives piece location
        pieceLocY = self.location[0]
        pieceLocX = self.location[1]
        self.availMoves = []
        self.availAttacks = []
        self.specialAttacks = []
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
                    # Checks for:
                    # is square to check out of bounds
                    # is square to check a friendly piece
                    # is square to check 
                    if (nr < 0 or nr >= R or nc < 0 or nc >= C or 
                    (isinstance(moves[nr][nc], Piece) and moves[nr][nc].team is self.team) 
                    or visited[nr][nc]
                    or ((isinstance(moves[coord[0]][coord[1]], Piece) and moves[coord[0]][coord[1]].team is not self.team))): continue 
                    queue.appendleft((nr, nc, coord[2]+1))
                    if(queue[0][2] <= self.moveDist):
                        
                        self.availMoves.append([nr,nc])
                        # print(moves[nr][nc].team)
                        # TODO Stop pieces from being able to jump in attacks
                        # stop pieces from adding to attacks if blocked? adapt bfs to search 
                        #       have array that tracks enemy active pieces... if currently in square with enemy piece,
                        #       then dont check the next square (cut off node)
                        #          OR change logic of check moves so that avail moves does not overlap with avail attacks at all? 

                        # if queue[0][2] == self.movedist then run another BFS for distance 1 around the current square
                        # remove "and isinstance(moves[nr][nc], Piece) and moves[nr][nc].team is not self.team"
                        
                        if(isinstance(moves[nr][nc], Piece) and moves[nr][nc].team is not self.team):
                            self.availAttacks.append([nr, nc])
                    elif(queue[0][2] == self.moveDist + 1 and self.pieceType == 'h' and isinstance(moves[nr][nc], Piece) and moves[nr][nc].team is not self.team):
                            self.availAttacks.append([nr, nc])
                            self.specialAttacks.append([nr, nc])
                            self.availMoves.append([nr, nc])
                            # self.surprise = True
                    

        
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
                    if (moves[xSearch][ySearch] == None and x > 7 and cr[x-8][2] == 1):
                        self.availMoves.append([xSearch, ySearch])
                    if (moves[xSearch][ySearch] != None and x > 7 and cr[x-8][2] == 1 and moves[xSearch][ySearch].team != team):
                        self.availMoves.append([xSearch, ySearch])
                        self.availAttacks.append([xSearch, ySearch])
            for row in range (-3, 4):
                xSearch = pieceLocX + row
                for col in range (-3, 4):
                    ySearch = pieceLocY + col
                    if (xSearch < 0 or xSearch > 7 or ySearch < 0 or ySearch > 7):
                        continue
                    if(moves[xSearch][ySearch] != None and moves[xSearch][ySearch].team != team):
                        self.availAttacks.append([xSearch, ySearch])
                
        self.availMoves = self.remove_deuplicates(self.availMoves)
        self.availAttacks = self.remove_deuplicates(self.availAttacks)

        return moves

    def remove_deuplicates(self, lst):
        return [t for t in (set(tuple(i) for i in lst))]

    # takes moveLoc tuple (row, col)
    def move(self, newRow, newCol):
        # function that moves the piece
        # returns a new board
        newBoard = Piece.chessboard

        if((newRow, newCol) in self.availMoves):
            # clear current space
            newBoard[self.location[0]][self.location[1]] = None

            self.location = [newRow, newCol]
            
            newBoard[newRow][newCol] = self
        
        return newBoard

    # takes in defender, if dice val is given (should update board or not), and if the attack is a ranged rook attack
    # return true if capture is successful
    def capture(self, defender, shouldUpdate, rookRanged):
        result = False
        roll = Piece.diceVal
        print(roll)
        
        # find index to use
        attackIndex = Piece.pieceData.index(self.pieceType)
        defenderIndex = Piece.pieceData.index(defender.pieceType)

        # use capture matrix with dice roll function to attempt capture,
        # on capture, set attacked square to null and call move on that square
        # unsuccessful, just return board

        # horse surprise attack
        if(defender.location in self.specialAttacks and roll < 6 and shouldUpdate == True):
            roll += 1
            print("If surprise, roll: ", roll)

        if(str(roll) in str(Piece.captureMatrix[attackIndex][defenderIndex])):
            result = True
            # then replace piece with attacker.

            if (shouldUpdate == True and rookRanged): 
                defender.kill_piece()
                return result
            
            if shouldUpdate == True:
                defender.replace_piece(self)
            

        print("Graveyard: ", Piece.graveyard)
        #print("Chessboard: \n", Piece.chessboard)

        return result

    # use this for rook special case?
    def kill_piece(self):
        Piece.graveyard.append(self.pieceID)
        Piece.activePieces.remove(self)
        Piece.chessboard[self.location[0]][self.location[1]] = None
        self.active = False
        return self

    # TAKES IN ATTACKER, NOT DEFENDER (defender is self)
    def replace_piece(self, attacker):
        Piece.graveyard.append(self.pieceID)
        Piece.activePieces.remove(self)
        Piece.chessboard[self.location[0]][self.location[1]] = attacker
        Piece.chessboard[attacker.location[0]][attacker.location[1]] = None
        attacker.location = [self.location[0], self.location[1]]
        self.active = False
        return self
    
    def getAllPieces():
        allPieces = []
        for row in Piece.chessboard:
            for piece in row:
                if isinstance(piece, Piece):
                    allPieces.append(piece)

        return allPieces
    
    def getTeamPieces(teamToGet):
        if(teamToGet == -1 or teamToGet == "white" or teamToGet == "w"):
            team = -1
        elif(teamToGet == 1 or teamToGet == "black" or teamToGet == "b"):
            team = 1
        
        teamPieces = []
        for row in Piece.chessboard:
            for piece in row:
                if(isinstance(piece, Piece) and piece.team == team):
                    teamPieces.append(piece)

        return teamPieces


    ### update moves... all pieces that are active, check their moves.
    ## def update moves?


    ### Piece scraper, scrapes chessboard for piece matching pieceID and returns Piece.chessboard[loc][loc]
    def find_piece(ID):
        for row in Piece.chessboard:
            for piece in row:
                if(isinstance(piece, Piece) and piece.pieceID == ID):
                    return piece

        return None

    # TODO: Remove this?
    def eval_moves(self):
        # evaluates moves based on a heuristic
        

        return 

    
    def gen_new_board():
        # [Row, Column], [Down, Over]

        # id, type, team (-1 = white, 1 = black), corps (1, 2, 3), loc (array), active
        Piece.chessboard[6, 0] = Piece("wp1", "p", -1, 1, [6, 0], True)
        Piece.chessboard[6, 1] = Piece("wp2", "p", -1, 1, [6, 1], True) 
        Piece.chessboard[6, 2] = Piece("wp3", "p", -1, 1, [6, 2], True) 
        Piece.chessboard[6, 3] = Piece("wp4", "p", -1, 2, [6, 3], True) # white pawns
        Piece.chessboard[6, 4] = Piece("wp5", "p", -1, 2, [6, 4], True) 
        Piece.chessboard[6, 5] = Piece("wp6", "p", -1, 3, [6, 5], True)
        Piece.chessboard[6, 6] = Piece("wp7", "p", -1, 3, [6, 6], True)
        Piece.chessboard[6, 7] = Piece("wp8", "p", -1, 3, [6, 7], True)

        Piece.chessboard[7, 0] = Piece("wr1", "r", -1, 2, [7, 0], True)
        Piece.chessboard[7, 7] = Piece("wr2", "r", -1, 2, [7, 7], True)
        Piece.chessboard[7, 1] = Piece("wh1", "h", -1, 1, [7, 1], True)
        Piece.chessboard[7, 6] = Piece("wh2", "h", -1, 3, [7, 6], True) # white back row
        Piece.chessboard[7, 2] = Piece("wb1", "b", -1, 1, [7, 2], True) 
        Piece.chessboard[7, 5] = Piece("wb2", "b", -1, 3, [7, 5], True)
        Piece.chessboard[7, 4] = Piece("wk1", "k", -1, 2, [7, 4], True)
        Piece.chessboard[7, 3] = Piece("wq1", "q", -1, 2, [7, 3], True)

        Piece.chessboard[1, 0] = Piece("bp1", "p", 1, 1, [1, 0], False)
        Piece.chessboard[1, 1] = Piece("bp2", "p", 1, 1, [1, 1], False)
        Piece.chessboard[1, 2] = Piece("bp3", "p", 1, 1, [1, 2], False) 
        Piece.chessboard[1, 3] = Piece("bp4", "p", 1, 2, [1, 3], False) # black pawns
        Piece.chessboard[1, 4] = Piece("bp5", "p", 1, 2, [1, 4], False)
        Piece.chessboard[1, 5] = Piece("bp6", "p", 1, 3, [1, 5], False)
        Piece.chessboard[1, 6] = Piece("bp7", "p", 1, 3, [1, 6], False)
        Piece.chessboard[1, 7] = Piece("bp8", "p", 1, 3, [1, 7], False)

        Piece.chessboard[0, 0] = Piece("br1", "r", 1, 2, [0, 0], False)
        Piece.chessboard[0, 7] = Piece("br2", "r", 1, 2, [0, 7], False)
        Piece.chessboard[0, 1] = Piece("bh1", "h", 1, 1, [0, 1], False)
        Piece.chessboard[0, 6] = Piece("bh2", "h", 1, 3, [0, 6], False) # black back row
        Piece.chessboard[0, 2] = Piece("bb1", "b", 1, 1, [0, 2], False)
        Piece.chessboard[0, 5] = Piece("bb2", "b", 1, 3, [0, 5], False)
        Piece.chessboard[0, 4] = Piece("bk1", "k", 1, 2, [0, 4], False)
        Piece.chessboard[0, 3] = Piece("bq1", "q", 1, 2, [0, 3], False)


        Piece.check_all_moves()

    # calls check moves on all alive pieces 
    def check_all_moves():
        for row in Piece.chessboard:
            for piece in row:
                if(isinstance(piece, Piece)):
                    piece.check_moves()
                
        return

    

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
