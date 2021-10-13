import numpy as np
import copy


class Piece:

    pieceID = ""
    pieceType = ""
    team = 0        # -1 for white, 1 for black
    corps = 0       # 0 left bishop, 1 king, 2 right king
    active = 0      # 0 dead, 1 alive
    availMoves = []  ### changed these, use self.availMoves.append([_, _])
    availAttacks = [] ### changed these, use self.availAttacks.append([_, _])
    location = [-1, -1]
    # chessboard = parent # piece should have parent chessboard
    # possibly include update board function

    def __init__(self, id, type, team, corps, loc):
        self.pieceID = id
        self.pieceType = type
        self.team = team
        self.corps = corps
        self.location = loc
        # self.chessboard = board

    def check_moves(self, chessboard):
        # function to check available moves. updates avail_moves array
        # moves array is a chessboard that shows available moves right now 
        # Will show captures as piece values in future
        moves = copy.copy(chessboard)
        
        # self.location is array of 2 numbers [x, y] that gives piece location

        pieceLocY = self.location[0]
        pieceLocX = self.location[1]
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
                    moves[rowToCheck][col] = "legal"
                    self.availMoves.append([rowToCheck, col])

        if(self.pieceType == 'h'):
            print()
        if(self.pieceType == 'b'):
            print()
        if(self.pieceType == 'r'):
            pieceLocX = self.location[0]
            pieceLocY = self.location[1]
            #print(moves[pieceLocX][pieceLocY].pieceType)
            print("Selected piece location: ", pieceLocX, pieceLocY)
            cr =   [[0, -1, 1],  # N
                    [1, -1, 1],  # NE
                    [1, 0, 1],   # E
                    [1, 1, 1],   # SE
                    [0, 1, 1],   # S
                    [-1, 1, 1],  # SW
                    [-1, 0, 1],  # W
                    [-1, -1, 1]] # NW

            for col in range (1, 3): # counter clockwise search that starts at the center and radiates out 2
                #print("aaaaaa", len(col[0]))
                for x, i in enumerate(cr):
                    if (col == 2): x = x + 8
                    #print(x)
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
                    if (moves[xSearch][ySearch] == None and col != 2): # if no piece on first outward radiation
                        self.availMoves.append([xSearch, ySearch])

                    if (moves[xSearch][ySearch] != None and x > 7 and cr[x-8][2] == 0 
                        and moves[xSearch][ySearch].team != team):
                            self.availAttacks.append([xSearch, ySearch])
                    if (moves[xSearch][ySearch] == None and x > 7 and cr[x-8][2] == 1):
                        self.availMoves.append([xSearch, ySearch])
            
        if(self.pieceType == 'k'):
            print()
        if(self.pieceType == 'q'):
            print()

        print(self.availMoves, "availMoves")
        print(self.availAttacks, "availAttacks")
        
        return moves

        '''
        Good logic for other pieces
         for col in range(pieceLocX-1, pieceLocX+2):
            if(col < 0 or col > 8):
                continue
            for row in range(pieceLocY-1, pieceLocY+2):
                if(row < 0 or row > 8):
                    continue
                # if space not occupied, then legal move
                if chessboard[row][col] == None:
                    # a legal move is represented by the number -10 for black, and 10 for white. Can change this later if confusing
                    # will likely need two for loop sets, one for black pieces, one for white. 
                    # Can solve this by using piece ID instead of number, and checking for team based on that
                    moves[row][col] = "legal"
        self.availMoves = moves
        return moves
        '''

    def move(self, chessboard):
        # function that moves the piece
        # returns a new board


        return

    def capture(self, defender):
        # return true or false or new board?
        
        return

    def eval_moves(self):
        # evaluates moves based on a heuristic
        # put wesley function here

        return 
    
    def __str__(self):
        return self.pieceID

    def __repr__(self):
        return self.pieceID

piecesBoard = np.empty((8, 8), dtype=Piece)

# [Row, Column], [Down, Over]

# id, type, team (-1 = white, 1 = black), corps (1, 2, 3), loc (array)
piecesBoard[6, 0] = Piece("wp1", "p", -1, 1, [6, 0])
#piecesBoard[6, 1] = Piece("wp2", "p", -1, 1, [6, 1]) # commented out to test availAttacks on wr1
piecesBoard[6, 2] = Piece("wp3", "p", -1, 1, [6, 2])
piecesBoard[6, 3] = Piece("wp4", "p", -1, 2, [6, 3]) # white pawns
piecesBoard[6, 4] = Piece("wp5", "p", -1, 2, [6, 4])
piecesBoard[6, 5] = Piece("wp6", "p", -1, 3, [6, 5])
piecesBoard[6, 6] = Piece("wp7", "p", -1, 3, [6, 6])
piecesBoard[6, 7] = Piece("wp8", "p", -1, 3, [6, 7])

piecesBoard[7, 0] = Piece("wr1", "r", -1, 2, [7, 0])
piecesBoard[7, 7] = Piece("wr2", "r", -1, 2, [7, 7])
piecesBoard[7, 1] = Piece("wh1", "h", -1, 1, [7, 1])
piecesBoard[7, 6] = Piece("wh2", "h", -1, 3, [7, 6]) # white back row
piecesBoard[7, 2] = Piece("wb1", "b", -1, 1, [7, 2]) 
piecesBoard[7, 5] = Piece("wb2", "b", -1, 3, [7, 5])
piecesBoard[7, 4] = Piece("wk1", "k", -1, 2, [7, 4])
piecesBoard[7, 3] = Piece("wq1", "q", -1, 2, [7, 3])

piecesBoard[1, 0] = Piece("bp1", "p", 1, 1, [1, 0])
piecesBoard[1, 1] = Piece("bp2", "p", 1, 1, [1, 1])
piecesBoard[1, 2] = Piece("bp3", "p", 1, 1, [1, 2])
piecesBoard[1, 3] = Piece("bp4", "p", 1, 2, [1, 3]) # black pawns
piecesBoard[1, 4] = Piece("bp5", "p", 1, 2, [1, 4])
piecesBoard[1, 5] = Piece("bp6", "p", 1, 3, [1, 5])
piecesBoard[1, 6] = Piece("bp7", "p", 1, 3, [1, 6])
piecesBoard[1, 7] = Piece("bp8", "p", 1, 3, [1, 7])

piecesBoard[5, 0] = Piece("br1", "r", 1, 2, [5, 0]) # dev change: initially 0, 0
piecesBoard[0, 7] = Piece("br2", "r", 1, 2, [0, 7])
piecesBoard[0, 1] = Piece("bh1", "k", 1, 1, [0, 1])
piecesBoard[0, 6] = Piece("bh2", "k", 1, 3, [0, 6]) # black back row
piecesBoard[0, 2] = Piece("bb1", "b", 1, 1, [0, 2])
piecesBoard[0, 5] = Piece("bb2", "b", 1, 3, [0, 5])
piecesBoard[0, 4] = Piece("bk1", "k", 1, 2, [0, 4])
piecesBoard[0, 3] = Piece("bq1", "q", 1, 2, [0, 3])


#print(piecesBoard)

print("----------------------\n", piecesBoard[6, 3].check_moves(piecesBoard)) # test check_moves print statement