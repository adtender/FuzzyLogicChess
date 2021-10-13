import numpy as np
import copy


class Piece:

    pieceID = ""
    pieceType = ""
    team = 0        # -1 for white, 1 for black
    corps = 0       # 0 left bishop, 1 king, 2 right king
    active = 0      # 0 dead, 1 alive
    availMoves = [[0,0], [-1,-1]]
    availAttacks = [[0,0], [-1,-1]]
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
        # moves array is a chessboard that shows available moves right now. Will show captures as piece values in future
        moves = copy.copy(chessboard)
        
        # self.location is array of 2 numbers [x, y] that gives piece location
        pieceLocY = self.location[0]
        pieceLocX = self.location[1]

        

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
            # check for moves, add into availmoves
            # loop through availmoves, check if move is an attack, add into availAttacks and remove from moves
            print()
        if(self.pieceType == 'k'):
            print()
        if(self.pieceType == 'q'):
            print()
        
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

# [Row, Column]

piecesBoard[6, 0] = Piece("wp1", "p", -1, 1, [6, 0])
piecesBoard[6, 1] = Piece("wp2", "p", -1, 1, [6, 1])
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

piecesBoard[0, 0] = Piece("br1", "r", 1, 2, [0, 0])
piecesBoard[0, 7] = Piece("br2", "r", 1, 2, [0, 7])
piecesBoard[0, 1] = Piece("bh1", "k", 1, 1, [0, 1])
piecesBoard[0, 6] = Piece("bh2", "k", 1, 3, [0, 6]) # black back row
piecesBoard[0, 2] = Piece("bb1", "b", 1, 1, [0, 2])
piecesBoard[0, 5] = Piece("bb2", "b", 1, 3, [0, 5])
piecesBoard[0, 4] = Piece("bk1", "k", 1, 2, [0, 4])
piecesBoard[0, 3] = Piece("bq1", "q", 1, 2, [0, 3])


print(piecesBoard)

print("----------------------\n", piecesBoard[6, 7].check_moves(piecesBoard)) # test check_moves print statement