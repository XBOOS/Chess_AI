class UIHandler:
    """
    deal with text format for print out
    """
    def __init__(self,board):
        self._board = board
        return
    def printInit(self):
        print """
                            Bing's Chinese Chess Game
        ****************************************************************

                                Instructions:
        ****************************************************************
                            Symbol representation:
        K = King, A = Advisor, E = Elephant,
        C = Cannon, H = Horse, R = Rook, P = Pawns
        Your pieces: K A E C H R P
        Computer pieces: k a e c h r p
        ****************************************************************
                                Chess Board:
        ****************************************************************
        Grids : 10 rows (0 to 9) * 9 columns (0 to 8)
        Move :  Type in the start and target coordinates
                in the form of 'row_number,column_number'
        Example :
        >>Piece to move (0~9),(0~8): 3,4
        >>Position to go (0~9),(0~8): 7,8
        Then you move the piece in (3,4) to (7,8)

        ****************************************************************"
        Extra tips :
        You are Red side. Move first
        You can search for more information on chinese chess rules to play the game.
        Enjoy the time!
        """


    def printBoard(self):
        self._board.toString()
    def printMoves(self,moveList):
        print "Number of total moves : ",len(moveList)
        for (oldCoord,newCoord) in moveList:
            print oldCoord," => ",newCoord
        print

