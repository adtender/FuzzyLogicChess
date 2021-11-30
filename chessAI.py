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

    # check all enemy moves, if any friendly piece is on location of an enemy attack, add it to a list
    def set_attacked_pieces(self):
        # call set alive pieces just in case
        self.set_alive_pieces()
        
        attacked = []
        enemyPieces = Piece.getTeamPieces(self.team * - 1)
        enemyAttacks = []

        # generating enemy attacks 
        for piece in enemyPieces:
            if len(piece.availAttacks) > 0:
                for attack in piece.availAttacks:
                    enemyAttacks.append(attack)
            
        # check if friendly pieces are attacked
        for friendlyPiece in self.alivePieces:
            row = friendlyPiece.location[0]
            col = friendlyPiece.location[1]
        
            if [row, col] in enemyAttacks:
                attacked.append(friendlyPiece)
        
        return attacked
    
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
        
        # TODO: If attack is on the king, do it automatically? or conditionally... if piece is likely to capture 
            # also bishops
        if(move in pieceName.availAttacks):
            
            # score bonus for being an attack
            score += 3
            
            defender = Piece.chessboard[move[0]][move[1]]
            attackIndex = Piece.pieceData.index(pieceName.pieceType)
            defenderIndex = Piece.pieceData.index(defender.pieceType)
            captureInfo = str(Piece.captureMatrix[attackIndex][defenderIndex])
            if(len(captureInfo) >= 5):
                score += 5
            elif(len(captureInfo) >= 3):
                score += 3
            elif(len(captureInfo) == 2):
                score += 2
            elif(len(captureInfo) < 2):
                score += 1
                
            # priority for attacking commanders    
            if(defender.pieceType == 'k'):
                score += 20
            if(defender.pieceType == 'b'):
                score += 15
            
            # prio for attacking strong piece
            if(defender.pieceType == 'q'):
                score += 8
            if(defender.pieceType == 'h'):
                score += 8
               
               
        # increase score if piece is attacked
        # pawns get no increase in score as they often protect more important pieces 
        attackedPieces = self.set_attacked_pieces()
        
        if(piece in attackedPieces):
            if(piece.pieceType == 'k'):
                score += 20
            elif(piece.pieceType == 'b'):
                score += 15
            elif(piece.pieceType == 'h' or piece.pieceType == 'r'):
                score += 5
            
        return score
    
    # returns array of tuples (pieceID, move [row, col], score)
    def score_pieces(self):
        self.set_alive_pieces()
        self.set_legal_moves()
        
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
    
    
    # takes in corps to move. Probably easier to track active corps this way in main.py
    # returns highest score move for the entered corps (pieceID, move coords, score)
    def move(self, corps):
        # call move on the piece that has the highest heuristic value
            
        # TODO: Iterate through scores array, keep best move for each corps and move that piece. 
        #       If a corps commander is dead, (this shouldnt be an issue when we get corps transfers implemented), then nothing moves for that corps.
        #       bestMoveCorps1, bestMoveCorps2. bestMoveCorps3 = ~~~~~, ~~~~~, ~~~~~
        
        print("---In move---")
        
        moves = self.score_pieces()
        
        print("---After score pieces call in move---")
        
        bestMoveScore = -1
        tiedScores = []
        
        for move in moves:
            piece = Piece.find_piece(move[0])
            
            if piece.corps == corps:
                # corpsMoves.append(move)
                
                # check if score is higher than current best and set if true
                if move[2] > bestMoveScore:
                    tiedScores = []         #clear tied scores array
                    bestMoveScore = move[2]
                    bestMove = move
                    tiedScores.append(move)
                elif move[2] == bestMoveScore:
                    tiedScores.append(move)
                    
        # if tied scores has moves in it, pick a random move
        if len(tiedScores) > 1:
            bestMove = tiedScores[random.randint(0, len(tiedScores)-1)]
            
        # bestMoveScore = max(corpsMoves, key=lambda item: item[2])
        # bestMove = corpsMoves.index(bestMoveScore, key=lambda item: item[2])
        # I thought this would be good solution^^^ but problems with index function. Will calculate max manually
        
        # test
        print("bestMove: ", bestMove, "\nbestMoveScore: ", bestMoveScore)
        
        return bestMove



########## randomAI inherits ChessAI ##########
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

def test_move(pieceID, row, col):
    piece = Piece.find_piece(pieceID)
    print(piece, piece.location)
    
    piece.move(row, col)
    
    newBoard = Piece.chessboard

    tempRow = piece.location[0] 
    tempCol = piece.location[1]
        
    # clear current space
    Piece.chessboard[piece.location[0]][piece.location[1]] = None
    piece.location = [row, col]
    Piece.chessboard[row][col] = piece
    Piece.check_all_moves()
    
    print("------------After test_move-------------\n", Piece.chessboard)
    
    print(piece, piece.location)
    
    return Piece.chessboard

# use this to test without GUI?
def test_move2(pieceID, row, col):
    piece = Piece.find_piece(pieceID)
    
    if([row, col] in piece.availAttacks):
        defender = Piece.chessboard[row][col]
        piece.capture(defender, 1, 0)
    elif([row, col] in piece.availMoves):
        piece.move(row, col)
    else:
        print("test_move did nothing")
        
    Piece.check_all_moves()
    
    print("------------After test_move-------------\n", Piece.chessboard)
    
    return Piece.chessboard
'''
# move pieces
# test_move("wp4", 2, 3)
test_move("bp5", 5, 4)

aiTest.move(1)
aiTest.move(2)
aiTest.move(3)
'''