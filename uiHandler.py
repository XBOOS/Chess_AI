class UIHandler:
    """
    deal with text format for print out
    """
    def __init__(self,board):
        self._board = board
        return
    def printInit(self):
        print "Welcome to Bing's Chinese chess game"
        print "================================================================"
        print "Instructions:"
        print "================================================================"
        print "Symbol representation:\n","K = King, A = Advisor, E = Elephant,\nC = Cannon, H = Horse, R = Rook, P = Pawns"
        print "Your pieces: K A E C H R P. Computer pieces: k a e c h r p."
        print "================================================================"
        print "Chess Board:"
        print "================================================================"
        print "grids of 10 ranks (from 0 to 9)* 9 files(from 0 to 8)"
        print "For your move,specify the start and target coordinates in the form of (x1,y1) (x2,y2)"

        print "================================================================"
        print "You are Red side. Move first"
        print "You can search for more information on chinese chess rules to play the game. \nEnjoy the time!"


    def printBoard(self):
        self._board.toString()
    def printMoves(self,moveList):
        print "Number of total moves : ",len(moveList)
        for (oldCoord,newCoord) in moveList:
            print oldCoord," => ",newCoord
        print

