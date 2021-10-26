import random
from pieces import Piece 

class ChessAI:


    chessboard = Piece.chessboard       # do i need this

    def __init__(self, team) -> None:
        self.team = team
        self.alivePieces = []
        self.set_alive_pieces()
        self.attackedPieces = []
        self.legalMoves = []        # list of tuples [(pieceID, location of move)]
        self.set_legal_moves()            
        

    def set_alive_pieces(self):
        alive = []
        for row in Piece.chessboard:
            for piece in row:
                if isinstance(piece, Piece) and piece.team == self.team:
                    alive.append(piece)
        
        self.alivePieces = alive
        return alive

    def set_legal_moves(self):
        allMoves = []
        for piece in self.alivePieces:
            allMoves.append((piece.pieceID, piece.availMoves))

        self.legalMoves = allMoves
        return allMoves

    def set_attacked_pieces(self):
        return
    
    def move(self):
        # call move on the piece that has the highest heuristic value
        # should this include corps? 
            # like should it account for all 3 moves separately, or will that be a main.py function?
        print("move")

    ## make random move function if heuristic is tied?


# randomAI inherits ChessAI
class RandomAI(ChessAI):

    def __init__(self, team) -> None:
        super().__init__(team)

    def move(self):
        
        # perform loop until either 
            # finds a piece with moves
            # or all pieces have no moves
        while True:

            # Generate random piece index to find in legalMoves
            randIndex = random.randint(0, len(self.legalMoves)-1)
            randPiece = self.legalMoves[randIndex][0]                   # ID of randPiece
            moveList = self.legalMoves[randIndex][1]                    # set of legal moves based on randPiece

            print("~~~~~~~~Current Piece to Check: ", randPiece)

            # if no moves at all
            if (len(Piece.find_piece(randPiece).availMoves) == 0 
                and len(Piece.find_piece(randPiece).availAttacks) == 0 
                and len(Piece.find_piece(randPiece).specialAttacks) == 0):
                continue 

            # does the current piece have availmoves
            # implement Rook exception
            noMoves = len(moveList) == 0

            # if there are moves at current piece, set randMove and break out of loop
            if(not noMoves):
                randMove = moveList[random.randint(0, len(moveList)-1)]         # set of coordinates that is a legal move
                # find piece in board and call move...
                # will this cause issues? should move be only called in main.py/CHESSBOARD?
                Piece.find_piece(randPiece).move(randMove[0], randMove[1])      # call move?
                break
            elif noMoves and len(Piece.find_piece(randPiece).availAttacks) != 0:
                randMove = moveList[random.randint(0, len(moveList)-1)]         # set of coordinates that is a legal move
                Piece.find_piece(randPiece).move(randMove[0], randMove[1])      # call move?
                break
            else:
                return "Move not found"


        Piece.check_all_moves()
        self.set_alive_pieces()
        self.set_legal_moves()
        print("###########", randPiece, " to ", randMove, "###########\n", Piece.chessboard)
        return (randPiece, randMove)



### driver code ###
Piece.gen_new_board()

ai1 = RandomAI(1)
print(RandomAI.chessboard)
ai1.set_alive_pieces()
ai1.set_legal_moves()

print("Alive pieces: ", ai1.alivePieces)
print("Legal Moves: ", ai1.legalMoves)

for i in range(3):
    print("Move: ", ai1.move())

print("-----------------------------------\nRandom AI Chessboard after 3 random moves\n", RandomAI.chessboard)

print("-----------------------------------\nPiece.chessboard after 3 random moves\n", Piece.chessboard)

