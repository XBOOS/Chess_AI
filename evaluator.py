import positionTable
class Evaluator:
    """
    Evaluator function for the game search
    Heuristic factors:
    1. pieces' value evaluation
    2. pieces' position evalution
    3. pieces' flexibility evaluation
    4. relationship evaluation
        For simplicity, I only consider some special set of relationship between pieces

    Acknoledgement:
    I read papers about the ELP chinese chess methodolody and use some of their evaluation methods.

    """

    def __init__(self,board,coef1=7,coef2=15,coef3=1):

        self._board = board
        self._strengthList = {"K":6000,"A":120,"E":120,"R":600,"H":270,"C":285,"P":30}
        # using default coefficients for linear factors if not special values specified
        self._piece_coef = coef1
        self._position_coef = coef2
        self._flexibility_coef = coef3

    def calcValue(self,RedSide):
        # accept a set of pieces from one player side a.k.a red or black
        if RedSide:
            pieceSet = self._board._redSet
        else:
            pieceSet = self._board._blackSet

        value = 0
        for piece in pieceSet:
            coordlist = pieceSet[piece]
            for coord in coordlist:
                pieceValue = self.evaValue(piece)
                positionValue = self.evaPosition(piece,coord)
                flexibilityValue = self.evaFlexibility(piece,coord)
                #relationshipValue
                value += self._piece_coef*pieceValue + self._position_coef*positionValue+self._flexibility_coef*flexibilityValue#+....
        return value


    def evaValue(self,piece):
        #already in the consistent upper case
        piece = piece.upper()
        return self._strengthList[piece]

    def evaPosition(self,piece,coord):
        return positionTable.getPositionValue(piece,coord)

    def evaFlexibility(self,piece,coord):
        # to evaluate the number of free moves form current states,determined by current board state
        # delegate to board to do the work
        return self._board.pieceFlexibility(piece,coord)
        #return 0

#for testing use
    def setBoard(self,board):
        self._board = board


# For testing use -mock
class Board_for_test: #not needed, but dont affect the module
    def __init__(self):
        self._redSet = {"R":[(9,0),(9,8)],
                "H":[(9,1),(9,7)],
                "E":[(9,2),(9,6)],
                "A":[(9,3),(9,5)],
                "K":[(9,4)],
                "C":[(7,1),(7,7)],
                "P":[(6,0),(6,2),(6,4),(6,6),(6,8)]}
        self._blackSet = {"r":[(0,0),(0,8)],
                "h":[(0,1),(0,7)],
                "e":[(0,2),(0,6)],
                "A":[(0,3),(0,5)],
                "k":[(0,4)],
                "c":[(2,1),(2,7)],
                "p":[(3,0),(3,2),(3,4),(3,6),(3,8)]}

    def changeRedSet(self,piece,newList):
        self._redSet[piece] = newList
        return
    def changeBlackSet(self,piece,newList):
        self._blackSet[piece] = newList
        return
    def pieceFlexibility(self,piece,coord):
        return 0 # only for testing use





if __name__=="__main__":

    print "Testing for evaluator class"
    print "==========================="
    print "cannot import board to use due to mutual importing"
    print "just mock a new Board class"
    board = Board_for_test()
    evaluator = Evaluator(board)
    print "=====evaValue======="
    print "R = ",evaluator.evaValue("R"),"  r = ",evaluator.evaValue("r")
    print "H = ",evaluator.evaValue("H"),"  h = ",evaluator.evaValue("h")
    print "C = ",evaluator.evaValue("C"),"  c = ",evaluator.evaValue("c")
    print "P = ",evaluator.evaValue("P"),"  p = ",evaluator.evaValue("p")
    print "E = ",evaluator.evaValue("E"),"  e = ",evaluator.evaValue("e")
    print "A = ",evaluator.evaValue("A"),"  a = ",evaluator.evaValue("a")
    print "K = ",evaluator.evaValue("K"),"  k = ",evaluator.evaValue("k")

    print "======evaPosition====="
    print "16 = ",evaluator.evaPosition("R",(3,2))
    print "14 = ",evaluator.evaPosition("H",(2,7))

    print "======calcValue======"

    board.changeRedSet("R",[(8,0),(9,8)])
    print "Red side board value = ",evaluator.calcValue(True)
    print "Black side board value = ",evaluator.calcValue(False)
