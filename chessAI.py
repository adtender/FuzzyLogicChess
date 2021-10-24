import random
from pieces import Piece 

class ChessAI:

    chessboard = Piece.chessboard

    def __init__(self, team) -> None:
        self.team = team
        self.activePieces = []
        self.attackedPieces = []
        self.legalMoves = []            # list of tuples [(pieceID, location of move)]

    def getActivePieces(self):
        
        return