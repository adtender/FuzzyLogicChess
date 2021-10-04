
class Piece:

    pieceID = ""
    team = 0        # 0 for white, 1 for black
    corps = 0       # 0 left bishop, 1 king, 2 right king
    active = 0      # 0 dead, 1 alive
    avail_moves = [[0,0], [-1,-1]]


    # possible
    # id is in binary
    # first 2 bits signifies team (01 = white, 10 = black)
    # second 3 bits signifies corps (100=left, 010=king, 001=right)
    # third 3 bits signifies piece (001=king, 010=pawn, 011=knight, 100=bishop, 101=rook, 110=queen)


    #
    def __init__(self, id, team, corps, ):
        self.pieceID = id
        self.team = team

    def check_moves(self, chessboard):
        return 

    def capture(self, defender):
        # return true or false or new board?
        
        return 