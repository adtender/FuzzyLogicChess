import numpy as np


class Piece:

    pieceID = ""
    team = 0        # 0 for white, 1 for black
    corps = 0       # 0 left bishop, 1 king, 2 right king
    active = 0      # 0 dead, 1 alive
    availMoves = [[0,0], [-1,-1]]
    availAttacks = [[0,0], [-1,-1]]
    location = [-1, -1]
    # chessboard = parent # piece should have parent chessboard
    # possibly include update board function

    def __init__(self, id, team, corps, loc, board):
        self.pieceID = id
        self.team = team
        self.corps = corps
        self.location = loc
        self.chessboard = board

    def check_moves(self, chessboard):
        # function to check available moves. updates avail_moves array
        # moves array is a chessboard that shows available moves right now. Will show captures as piece values in future
        moves = chessboard
        
        # self.location is array of 2 numbers [x, y] that gives piece location
        pieceLocX = self.location[0]
        pieceLocY = self.location[1]

        # checking pawn moves
        for col in range(pieceLocX-1, pieceLocX+2):
            for row in range(pieceLocY-1, pieceLocY+2):
                # if space not occupied, then legal move
                if chessboard[row][col] == 0:
                    # a legal move is represented by the number -10 for black, and 10 for white. Can change this later if confusing
                    # will likely need two for loop sets, one for black pieces, one for white. 
                    # Can solve this by using piece ID instead of number, and checking for team based on that
                    moves[row][col] = 10
                    print("legal move")
        self.availMoves = moves
        return moves

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

#positives represent white, negatives represent black
board = np.array([   [-2, -2, -2, -2, -2, -2, -2, -2],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [2, 2, 2, 2, 2, 2, 2, 2]
        ], order="C")

print(board)
print("board[0][1]: ", board[0][1])

pawn = Piece("wp5", 0, 0, [4, 6])
print(pawn.location)
print(pawn.check_moves(board))