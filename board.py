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
                "A":[(0,3),(0,5)],
                "k":[(0,4)],
                "c":[(2,1),(2,7)],
                "p":[(3,0),(3,2),(3,4),(3,6),(3,8)]}


    def calcValue(self):
        # using evaluation function to calculate the value of the current state
        return self._blackValue()-self._redValue()

    def isOnBoard(self,coord):
        return 0<= coord[0]<9 and 0<=coord[1]<10

    def isMoveLegal(self,(oldCoor,newCoord)):
        #check board border and target position occupation by own piece
        if not isOnBoard(coord):
            return False

        piece = self._state[oldCoord]
        target = self._state[newCoord]
        #Can just check the upper and lowercase of letter ,depends on which is faster

        if piece in self._redSet and target in self._redSet:
            return False
        elif piece in self._blackSet and target in self._blackSet:
            return False
        else:
            #check with chess moving rule
            return self._moveRuleHandler.isMoveLegal((oldCoord,newCoord))


    def makeMove(self,RedSide,(oldCoord,newCoord)):
        #should pass in player?
        #don't include the legal check here,because wethere checking depends on player/comp side
        #upate the grid and piece lists
        piece = self._state[oldCoord]
        target = self._state[newCoord]
        #special case : King suicide, but this would be prevented by evaluation func
        if RedSide:
        # if piece in self._redSet:
            self._redSet[piece] = [newCoord if x==oldCoord else x for x in self._redSet[piece]]
        else:
            self._blackSet[piece] = [newCoord if x==oldCoord else x for x in self._blackSet[piece]]

        self._state[oldCoord] = "*"
        self._state[newCoord] = piece
        #decide wether capturing move
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

    def _blackValue(self):
        # calculate the value of the black pieces a.k.a computer side
        return self._evaluator.calcValue(False)#BLACK_COMPUTER

    def _redValue(self):
        return self._evaluator.calcValue(True)#RED_PLAYER

    def pieceFlexibility(self,piece,coord):
        #maybe shouldnt cache it,recompute one but cache too many
        #moveRuleHandler.roughMoves(piece,coord)
        return 0

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

    def printBoard(self):
        print "             Current Board"
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

        print "       0   1   2   3   4   5   6   7   8   "



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
   print "(3,2) : " board.isOnBoard((3,2))
   print "(11,9) : " board.isOnBoard((11,9))
   print "(6,-2) : " board.isOnBoard((6,-2))
   print "==isMoveLegal=="
   print "illegal :  "board.isMoveLegal((0,0),(0,1))
   print "illegal :  "board.isMoveLegal((2,1),(0,1))
   print "illegal :  "board.isMoveLegal((0,0),(0,1))
