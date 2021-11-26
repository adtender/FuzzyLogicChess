import random
from pieces import Piece 
import time
import math

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

    #TODO: Add attacked pieces in consideration for heuristic. Maybe a thing for Hard AI
    def set_attacked_pieces(self):
        return
    
    # returns score of move 
    def eval_move(self, piece, move):
        score = 0
        
        pieceName = Piece.find_piece(piece[0])
        
        # distance from enemy king (the closer the better)
        oppKingDist = self.dist_from_enemy_king(move)
        if(oppKingDist <= 3):
            score += 7
        elif(oppKingDist <= 5):
            score += 4
            
        # If its an attack, add corresponding values to score
        # 4 tiers:
        # If success likely (if 5+ numbers in capturematrix): +5
        # If slightly likely: (if 3-4 numbers in capture matrix): +3
        # If unlikely: (2 numbers in capturematrix): +2
        # If almost impossible: (1 number): +1
        if(move in pieceName.availAttacks):
            
            defender = Piece.chessboard[move[0]][move[1]]
            attackIndex = Piece.pieceData.index(pieceName.pieceType)
            defenderIndex = Piece.pieceData.index(defender.pieceType)
            captureInfo = Piece.captureMatrix[attackIndex][defenderIndex]
            if(len(captureInfo) >= 5):
                score += 5
            elif(len(captureInfo) >= 3):
                score += 3
            elif(len(captureInfo) == 2):
                score += 2
            elif(len(captureInfo) < 2):
                score += 1
       

            
        return score
    
    # returns array of tuples (pieceID, move [row, col], score)
    def score_pieces(self):
        
        allMoves = self.legalMoves
        piecesWithMoves = []
    
        scores = []
        
        # loop through active pieces, score
        for piece in allMoves:
            if len(piece[1]) > 0:
                piecesWithMoves.append(piece)
                
        print("\nPieces with moves: ", piecesWithMoves)
        
        for piece2 in piecesWithMoves:
            for move in piece2[1]:
                scores.append((piece2[0], move, self.eval_move(piece2, move)))
        
        
        print("\nScores: ", scores)
        return scores
    
    # takes in move coords (row, col)
    # returns distance from king in cartesian coordinates
    def dist_from_enemy_king(self, move):
        dist = 0
        
        if(self.team == 1):
            kingLoc = [Piece.find_piece("wk1").location[0], Piece.find_piece("wk1").location[1]]
        if(self.team == -1):
            kingLoc = [Piece.find_piece("bk1").location[0], Piece.find_piece("bk1").location[1]]
            
        dist = abs(math.dist(move, kingLoc))
        # print("Distance from king: ", dist)
        
        return dist
    
    
    
    def move(self):
        # call move on the piece that has the highest heuristic value
        # should this include corps? 
            # like should it account for all 3 moves separately, or will that be a main.py function?
            
        # TODO: Iterate through scores array, keep best move for each corps and move that piece. 
        #       If a corps commander is dead, (this shouldnt be an issue when we get corps transfers implemented), then nothing moves for that corps.
        #       bestMoveCorps1, bestMoveCorps2. bestMoveCorps3 = ~~~~~, ~~~~~, ~~~~~
        print("move")

    ## make random move function if heuristic is tied?


# randomAI inherits ChessAI
class RandomAI(ChessAI):

    def __init__(self, team) -> None:
        super().__init__(team)

    def move(self, corps):
        
        # perform loop until either 
            # finds a piece with moves
            # or all pieces have no moves

        corpsMoves = [] # new array of tuples corresponding to corps
        for piece in self.legalMoves:
            if Piece.find_piece(piece[0]).corps == corps:
                corpsMoves.append(piece)

        while True:

            # Generate random piece index to find in legalMoves
            randIndex = random.randint(0, len(corpsMoves)-1)
            randPiece = corpsMoves[randIndex][0]                   # ID of randPiece
            moveList = corpsMoves[randIndex][1]                    # set of legal moves based on randPiece

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
                #Piece.find_piece(randPiece).move(randMove[0], randMove[1])      # call move?
                break
            elif noMoves and len(Piece.find_piece(randPiece).availAttacks) != 0:
                randMove = moveList[random.randint(0, len(moveList)-1)]         # set of coordinates that is a legal move
                #Piece.find_piece(randPiece).move(randMove[0], randMove[1])      # call move?
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

print(Piece.chessboard)

aiTest = ChessAI(1)

aiTest.score_pieces()


'''
i = -1
while True:

    ai1 = RandomAI(i)
    ai1.set_alive_pieces()
    ai1.set_legal_moves()

    activeCorps = [1, 1, 1]

    # print("Alive pieces: ", ai1.alivePieces)
    # print("Legal Moves: ", ai1.legalMoves)

    while activeCorps != [2, 2, 2]:
        randomCorps = random.randint(1, 3)
        if(activeCorps[randomCorps-1] == 1):
            time.sleep(3)
            print("Move: ", ai1.move(randomCorps))
            activeCorps[randomCorps-1] += 1
            print("\n\n\n")
    
    i *= -1
    print("____________________________________")
'''
