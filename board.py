import numpy as np
from evaluator import Evaluator
from moveRuleHandler import MoveRuleHandler
class Board:
    """
    chess board
    maintain the pieces of both sides of player and computer

    _state : maintain the piece type of each board coordinate
    _evaluator : contain the evaluation utilities
    _redSet : maintain player's piece set ---player is the red side
    _blackSet : maintain computer's piece set -- computer is the black side

    """
    def __init__(self):
        self._state = np.zeros((10,9),dtype = object)#['*' for i in range(90)]
        self._lastCapturedPiece = list()
        self._lastMove = None  #for search cache
        self._initialize()
        self._evaluator = Evaluator(self)
        self._moveRuleHandler = MoveRuleHandler(self)
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
                "a":[(0,3),(0,5)],
                "k":[(0,4)],
                "c":[(2,1),(2,7)],
                "p":[(3,0),(3,2),(3,4),(3,6),(3,8)]}


    def calcValue(self):
        # using evaluation function to calculate the value of the current state
        return self._blackValue()-self._redValue()

    def isOnBoard(self,coord):
        return 0<= coord[0]<10 and 0<=coord[1]<9

    def isInPalace(self,(x,y)):
        if not self.isOnBoard((x,y)): return False
        return (7<=x<=9 and 3<=y<=5) or (0<=x<=2 and 3<=y<=5)

    def isOnSameSide(self,coord1,coord2):
        return self._state[coord1].islower() == self._state[coord2].islower()

    def onRedSide(self,coord):
        #return True if on red side
        return self._state[coord].isupper()
        # return self._state[coord] in self._state._redSet


    def allLegalMoves(self,BlackSide):
        allLegalMoves = []
        if BlackSide:
            for piece in self._blackSet:
                for coord in self._blackSet[piece]:
                    allLegalMoves.extend(self._moveRuleHandler.getLegalMoveList(piece,coord))
        else:
            for piece in self._redSet:
                for coord in self._redSet[piece]:
                    allLegalMoves.extend(self._moveRuleHandler.getLegalMoveList(piece,coord))

        print "=========For debugging: total number of possible legal moves : ",len(allLegalMoves)
        print "now the red set are ",self._redSet
        print allLegalMoves
        return allLegalMoves




    def isMoveLegal(self,(oldCoord,newCoord)):
        """
        args: from oldCoord to newCoord
        return : True for legal, False for illegal
        1. check the coordinates on chess board - isOnBoard()
        2. check if the target position is occupied by own pieces
        3. check if the move pattern is legal, e.g. Elephant only move 2 crossovers

        PS. other legality checking only applies when the player is user,then check it in userHandler,
            because computer's moves are generated by legalMoves, can leave out the checking process
        """

        if not (self.isOnBoard(oldCoord) or self.isOnBoard(newCoord)):
            return False


        piece = self._state[oldCoord]
        target = self._state[newCoord]
        #Can just check the upper and lowercase of letter ,depends on which is faster

        print "piece and target are :",piece, target
        if piece in self._redSet and target in self._redSet:
            return False
        elif piece in self._blackSet and target in self._blackSet:
            return False
        else:
            #check with chess moving rule
            return self._moveRuleHandler.isMoveLegal(piece,(oldCoord,newCoord))

    def unmakeMove(self,(oldCoord,newCoord),RedSide=None):

        if RedSide==None:
            RedSide = self.onRedSide(newCoord)
        piece = self.getPiece(newCoord)
        target = self._lastCapturedPiece.pop() # the name is corresponding to makeMove
        print "here is the lastCapturedPiece..",target
        #restore the chess board state and piece set
        self.setPiece(oldCoord,piece)
        self.setPiece(newCoord,target)

        if RedSide:
        # if piece in self._redSet:
            self._redSet[piece] = [oldCoord if x==newCoord else x for x in self._redSet[piece]]
        else:
            self._blackSet[piece] = [oldCoord if x==newCoord else x for x in self._blackSet[piece]]


        if target =="*":
            print "Attention here , the captured piece is just *"
            return
        if RedSide:# the captured piece is black
            if target in self._blackSet:
                self._blackSet[target].append(newCoord)
            else:
                self._blackSet[target] = [newCoord]
        else:
            if target in self._redSet:
                self._redSet[target].append(newCoord)
            else:
                self._redSet[target] = [newCoord]


        #self.makeMove((newCoord,oldCoord),RedSide)

    def makeMove(self,(oldCoord,newCoord),RedSide=None):
        #should pass in player?  Ride = Player = True, Black = Computer = False

        #!!!!!!Don't include the legal check here,because wethere checking depends on player/comp side
        #upate the grid and piece lists

        #piece = self._state[oldCoord[0]][oldCoord[1]]
        #target = self.getPiece[newCoord[0]][newCoord[1]]
        piece = self.getPiece(oldCoord)
        target = self.getPiece(newCoord)

        self._lastMove = (oldCoord,newCoord)
        print "Move in search : ",oldCoord,"=>",newCoord

        if RedSide ==None:
            RedSide = self.onRedSide((oldCoord))
            print "if it is on redSide? ",RedSide
        #special case : King suicide, but this would be prevented by evaluation func
        if RedSide:
        # if piece in self._redSet:
            self._redSet[piece] = [newCoord if x==oldCoord else x for x in self._redSet[piece]]
        else:
            self._blackSet[piece] = [newCoord if x==oldCoord else x for x in self._blackSet[piece]]

        #self._state[oldCoord[0]][oldCoord[1]] = "*"
        #self._state[newCoord[0]][newCoord[1]] = piece
        self.setPiece(oldCoord,"*")
        self.setPiece(newCoord,piece)

        #cache this captured piece
        self._lastCapturedPiece.append(target)
        #if is capturing move,update the piece list
        if target != "*":
            if not RedSide:#only can eat piece of other side
            #if target in self._redSet:
                self._redSet[target].remove(newCoord)
                if self._redSet[target]==[]:
                    # if no pieces left remove from board list
                    del self._redSet[target]
            else:
                self._blackSet[target].remove(newCoord)
                if self._blackSet[target]==[]:
                    # if no pieces left remove from board list
                    del self._blackSet[target]

    def getPiece(self,coord):
        return self._state[coord[0]][coord[1]]

    def setPiece(self,coord,newPiece):
        self._state[coord[0]][coord[1]] = newPiece
        return


    def _blackValue(self):
        # calculate the value of the black pieces a.k.a computer side
        return self._evaluator.calcValue(False)#BLACK_COMPUTER

    def _redValue(self):
        return self._evaluator.calcValue(True)#RED_PLAYER

    def pieceFlexibility(self,piece,coord):
        #maybe shouldnt cache it,recompute one but cache too many
        #moveRuleHandler.roughMoves(piece,coord)
        return self._moveRuleHandler.numOfLegalMoves(piece,coord)
        #return 0

    def _initialize(self):

        for i in range(10):
            for j in range(9):
                self._state[i][j]="*"

        self._state[0][0] =self._state[0][8]= "r"
        self._state[9][0] =self._state[9][8]= "R"
        self._state[0][1] =self._state[0][7]= "h"
        self._state[9][1] =self._state[9][7]= "H"
        self._state[0][2] =self._state[0][6]= "e"
        self._state[9][2] =self._state[9][6]= "E"
        self._state[0][3] =self._state[0][5]= "a"
        self._state[9][3] =self._state[9][5]= "A"
        self._state[0][4] = "k"
        self._state[9][4] = "K"
        self._state[2][1] =self._state[2][7]= "c"
        self._state[7][1] =self._state[7][7]= "C"
        self._state[3][0] =self._state[3][2]= self._state[3][4]=self._state[3][6]=self._state[3][8] = "p"
        self._state[6][0] =self._state[6][2]= self._state[6][4]=self._state[6][6]=self._state[6][8] = "P"

    def combineXY(self,x,y):
        return x*9+y

    def splitXY(self,xy):
        return (xy//9,xy%9)

    def checkOver(self):
        return self.checkWinner()!=None

    def checkWinner(self):
        # check if king was captured
        if "K" not in self._redSet:
            return "You"
        elif  "k" not in self._blackSet:
            return "Computer"
        else:
            return None

    def printBoard(self):
        print "\n\n             Current Board"
        print "       0   1   2   3   4   5   6   7   8   "
        print "----------------------------------------------"
        for i in range(5):
            print i," [",
            for j in range(9):
                print " ",self._state[i][j],
            print " ] ",i
        print "----------------------------------------------"
        print "~ ~ ~ ~ ~ ~ ~ ~ ~ River ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ "
        print "----------------------------------------------"
        for i in range(5,10):
            print i," [",
            for j in range(9):
                print " ",self._state[i][j],
            print " ] ",i

        print "----------------------------------------------"

        print "       0   1   2   3   4   5   6   7   8  \n\n "



if __name__=="__main__":
    print "Testing for Board"
    board = Board()
    #print board.combineXY(3,4)
    #print board.splitXY(45)

    board.printBoard()
    print "===red set===",board._redSet
    print "===black set===",board._blackSet

    print "========calcValue test==========="
    print "Initial board: red-black = 0 ? ",board.calcValue()

    print "==========utilities test=========="
    print "==isOnBoard()=="
    print "(3,2) : ", board.isOnBoard((3,2))
    print "(11,9) : ", board.isOnBoard((11,9))
    print "(6,-2) : ", board.isOnBoard((6,-2))
#"""
    print "==isMoveLegal=="
    print "illegal(=False) :  ",board.isMoveLegal(((0,0),(0,1)))
    print "illegal(=False) :  ",board.isMoveLegal(((2,1),(0,1)))
    print "illegal(=False) :  ",board.isMoveLegal(((0,0),(0,1)))
#    print "legal(=True) :  ",board.isMoveLegal(((0,0),(1,0)))
#    print "legal(=True) :  ",board.isMoveLegal(((8,0),(2,1)))
#"""
    print "==isOnSameSide=="
    print board._state[(0,0)],board._state[(2,7)],"  on the same side " ,board.isOnSameSide((0,0),(2,7))
    print board._state[(0,5)],board._state[(9,5)],"on different side ", board.isOnSameSide((0,5),(9,5))


    print "==makeMove====="
    board.printBoard()

    print "==============after makeMove((0,0),(1,0))============="
    board.makeMove(((0,0),(1,0)))
    board.printBoard()


    print "==============after makeMove((9,7),(7,6))============="
    board.makeMove(((9,7),(7,6)),True)
    board.printBoard()

    print "==============after unmakeMove((9,7),(7,6))============="
    board.unmakeMove(((9,7),(7,6)),True)
    board.printBoard()

    board.unmakeMove(((0,0),(1,0)))
    print
    print "==============Testing for isMoveLegal()==============="
    print "Legal cannon move check : ",board.isMoveLegal(((9,7),(7,6)))
    print "Legal cannon move check : ",board.isMoveLegal(((0,0),(1,0)))
    print "Illegal cannon move check : ",board.isMoveLegal(((9,8),(9,7)))

