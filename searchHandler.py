class SearchHandler:
    """
    MiniMax search algorithm with alpha-beta pruning.
    """
    def __init__(self,board):
        self._board = board
        return

    def alphaBeta(self,isMax,depth,alpha,beta):
        """
        return (best_move,alpha/beta)
        """
        # Max = Computer = black
        # Because computer is doing the search, so it tries to maximize its winning possiblity
        print " now the depth is ",depth
        if depth == 0 or self._board.checkOver():
            # reach the search depth limit or terminal node
            return (self._board._lastMove,self._board.calcValue())

        legalMoves = self._board.allLegalMoves(isMax)# isMax = Computer =Black side
        best_move = None
        if isMax:
            for move in legalMoves:
                self._board.makeMove(move)
                (childMove,childValue) = self.alphaBeta(False,depth-1,alpha,beta)
                self._board.unmakeMove(move)

                if alpha < childValue:
                   # (best_move,alpha) = (childMove,childValue)
                    alpha = childValue
                    best_move = move
                if alpha >=beta:
                    print "alpha cutoff pruning here"
                    break
            return (best_move,alpha)
        else:
            for move in legalMoves:
                self._board.makeMove(move)
                (childMove,childValue) = self.alphaBeta(True,depth-1,alpha,beta)
                self._board.unmakeMove(move)
                if beta > childValue:
                   # (best_move,beta) = (childMove,childValue)
                   beta = childValue
                   best_move = move
                if alpha >=beta:
                    print "beta cutoff pruning here"
                    break
            return (best_move,beta)


# mock class for testing alphaBeta searching
class Game_for_test:
    def __init__(self,initial="A"):
        self._gameRule = """
    ===================================================
    Another simple game for alphaBeata testing.
    MIN:           A(4)                   H(6)
                  /   \\                /     \\
    MAX:        B(15)    C(4)         I(6)     J(9)
                /   \\  /  \\        /  \\     /  \\
    MIN:      D(15) E(8) F(3)G(4)   K(-5)L(6) M(1)N(9)
    ===================================================
    """
        self._currentNode = initial
        self._lastMove = None
        self._moves= { "Root":["A","H"],"A":["B","C"],"H":["I","J"],
                "B":["D","E"],"C":["F","G"],"I":["K","L"],
                "J":["M","N"]}
        self._values = {"D":15,"E":8,"F":3,"G":4,"K":-5,"L":6,"M":1,"N":9}

        return

    def showGameRule(self):
        print self._gameRule
        return

    def allLegalMoves(self,BlackSide):
        """
        return legalMoves ==> a list of childNodes
        """

        childNodes = self._moves[self._currentNode]
        legalMoves = []
        for cNode in childNodes:
            legalMoves.append((self._currentNode,cNode))
        # print "Here get legal moves......",legalMoves
        return legalMoves

    def checkOver(self):
        return self._currentNode in self._values

    def calcValue(self):
        if self._currentNode not in self._values:
       #     print "now the currentNode is ",self._currentNode
            raise Exception("Not terminal node,cannot calc value")
        return self._values[self._currentNode]

    def makeMove(self,move):
        """
        input move ==> nextNode, just put currentNode to nextNode
        """
        self._lastMove = move
        self._currentNode = move[1]
        print "Move one step : ", move

    def unmakeMove(self,move):
        #go back to parent node as recorded
        print "Step back : ", move[1],"=>",move[0]
        self._currentNode = move[0]

    def getBestMove(self):
        (best_move,value) = self.alphaBeta(True,4,-float("inf"),float("inf"))
        return best_move



if __name__ == "__main__":
    print "=======Testing alphaBest using Simple game========="
    game_test = Game_for_test("Root") # can change to either starting node including Root
    game_test.showGameRule()
    searchHandler = SearchHandler(game_test)
    #initial alpha = NEG_INFINITY, beta = POS_INFINITY
    (best_move,value) = searchHandler.alphaBeta(True,3,-float("inf"),float("inf")) # using bool to control start from MAX or MIN
    print "The (best_move,value) = (",best_move ,",",value
    print "=======Simple Game Test Ending===================="
    print "Pretty good result, I didnt use the child best_move, maybe could serve as cache!"


