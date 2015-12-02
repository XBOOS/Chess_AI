# contain the piece moving rules of Chinese Chess
# Imply the rules by possbile moves
# from board import Board #just for testing
class MoveRuleHandler:

    def __init__(self,board):
        self._board = board

# for moves capable of capturing other pieces
    def captureMoves(self):
        return

    def positionMoves(self):
        return

    def isMoveLegal(self,piece,(oldCoord,newCoord)):
        return (oldCoord,newCoord) in self.getLegalMoveList(piece,oldCoord)

        """
        if piece.upper()=="R": #for Rook
            return (oldCoord,newCoord) in self.rook_moveList((oldCoord))
#            if oldCoord[0]==newCoord[0]: # on the same row
#                #check obstacle
#                for col in range(min(oldCoord[1],newCoord[1])+1,max(oldCoord[1],newCoord[1])):
#                    if self._board._state[oldCoord[0]][col]!="*":
#                        return False
#            elif oldCoord[1]==newCoord[1]: # on the same column
#                for row in range(min(oldCoord[0],newCoord[0])+1,max(oldCoord[1],newCoord[1])):
#                    if self._board._state[oldCoord[row]][1]!="*":
#                        return False
#            else: # now on the same line
#                return False
#            return True
        elif piece.upper()=="H": #for Horse
            # only : so  (x1-x2)*(y1-y2)==2
#            if (oldCoord[0]-newCoord[0])*(oldCoord[1]-newCoord[1])==2:
            return (oldCoord,newCoord) in self.horse_movelist((oldCoord))
        elif piece.upper()=="E":
            return (oldCoord,newCoord) in self.elephant_moveList((oldCoord))
        elif piece.upper()=="A":
            return (oldCoord,newCoord) in self.advisor_moveList((oldCoord))
        elif piece.upper()=="K":
            return (oldCoord,newCoord) in self.king_moveList((oldCoord))
        elif piece.upper()=="C":
            return (oldCoord,newCoord) in self.cannon_moveList((oldCoord))
        elif piece.upper()=="P":
            return (oldCoord,newCoord) in self.pawn_moveList((oldCoord))
        else:
            raise Exception("illegal piece input in checkMoveLegal"+piece)

        """

    def getLegalMoveList(self,piece,coord):
        piece_up = piece.upper()
        if piece_up == "R":
            return self.rook_moveList(coord)
        elif piece_up == "H":
            return self.horse_movelist(coord)
        elif piece_up =="E":
            return self.elephant_moveList(coord)
        elif piece_up =="A":
            return self.advisor_moveList(coord)
        elif piece_up =="K":
            return self.king_moveList(coord)
        elif piece_up =="C":
            return self.cannon_moveList(coord)
        elif piece_up =="P":
            return self.pawn_moveList(coord)
        else:
            raise Exception("illegal piece input in checkMoveLegal"+piece)


    def numOfLegalMoves(self,piece,coord):
        return len(self.getLegalMoveList(piece,coord))


    """
    The legal move list generation doesnt take move quality into consideration
    For alpha beta pruning, I need to sort it according to self-define quality evaluation
    one way is to evaluate the board value after move if doing pre-computation
    """

    def rook_moveList(self,(x,y)):
        """
        args : (x,y)  (the current cooordinate)
        return : legal moves for Rook, straight line horizontally or vertically
        """
        legalMoves = []
        unitSteps = [(-1,0),(0,-1),(1,0),(0,1)]
        (i,j) = (x,y)

        for unitStep in unitSteps:
            (i,j) = self.add_tuple((i,j) , unitStep)
            while self._board.isOnBoard((i,j)) and self._board._state[i][j]=="*":
                legalMoves.append(((x,y),(i,j)))
                (i,j) = self.add_tuple((i,j) , unitStep)
            if self._board.isOnBoard((i,j)):# come across obstacle piece
                #check side, different side=>capturing move
                if not self._board.isOnSameSide((x,y),(i,j)):
                    legalMoves.append(((x,y),(i,j)))
            (i,j) = (x,y)

        return legalMoves



    def horse_movelist(self,(x,y)):
        """
        args : (x,y)  (the current cooordinate)
        return : Horse move: go one unit step orthogona and one unit step diagonal
        """
        legalMoves = []
        unitSteps = {(-1,0):[(-2,-1),(-2,1)]
                ,(0,-1):[(1,-2),(-1,-2)]
                ,(1,0):[(2,1),(2,-1)]
                ,(0,1):[(1,2),(-1,2)]}
        (i,j) = (x,y)
        for ob_step in unitSteps: #the key is position of obstacle
            obstacle = self.add_tuple((x,y),ob_step)
            # get out of board or get horse's "leg" obstacled
            if not self._board.isOnBoard(obstacle) or self._board.getPiece(obstacle) !="*":
                continue
            for tmp in unitSteps[ob_step]:
                (i,j) = self.add_tuple((i,j),tmp)
                if self._board.isOnBoard((i,j)) and (self._board._state[i][j]=="*" or not self._board.isOnSameSide((x,y),(i,j))):
                    #legalMoves.append((i,j))
                    legalMoves.append(((x,y),(i,j)))
                (i,j) = (x,y)

        return legalMoves

    def elephant_moveList(self,(x,y)):
        """
        args : (x,y)  (the current cooordinate)
        return : Elephant move list: go cross 2 diagonals and not get one obstacle in the "elephant eye"
        """
        legalMoves = []
        unitSteps = [(-1,1),(-1,-1),(1,-1),(1,1)]
        (i,j) = (x,y)
        for unitStep in unitSteps:
            (i,j) = self.add_tuple((i,j),unitStep)
            #print "now the (i,j ) is ",(i,j)
            # check the elephant eye is obstacled or not

            if not self._board.isOnBoard((i,j)) or self._board.getPiece((i,j)) !="*":
                (i,j) = (x,y)
                continue
            (i,j) = self.add_tuple((i,j), unitStep)
            if self._board.isOnBoard((i,j)) and (self._board._state[i][j]=="*" or not self._board.isOnSameSide((x,y),(i,j))):
                if self._board.onRedSide((x,y)) and i<5:#cross the river
                    (i,j) = (x,y)
                    continue
                elif not self._board.onRedSide((x,y)) and i>4:#cross the river
                    (i,j) = (x,y)
                    continue

                #legalMoves.append((i,j))
                legalMoves.append(((x,y),(i,j)))
            (i,j) = (x,y)

        return legalMoves

    def advisor_moveList(self,(x,y)):
        """
        args : (x,y)  (the current cooordinate)
        return : Advisor move list: go cross one diagonal and can only stay in the palace
        """

        #Maybe direct emumeration maybe is faster
        positions = {(0,3):[(1,4)]
                ,(0,5):[(1,4)]
                ,(1,4):[(2,3),(2,5)]
                ,(2,3):[(1,4)]
                ,(2,5):[(1,4)]
                ,(9,3):[(8,4)]
                ,(9,5):[(8,4)]
                ,(8,4):[(7,3),(7,5)]
                ,(7,3):[(8,4)]
                ,(7,5):[(8,4)]}
        legalMoves = []
        for (i,j) in positions[(x,y)]:
            legalMoves.append(((x,y),(i,j)))
        return legalMoves

#        legalMoves = []
#        unitSteps = [(-1,1),(-1,-1),(1,-1),(1,1)]
#        (i,j) = (x,y)
#        for unitStep in unitSteps:
#            (i,j) += unitStep

#            if self._board.isOnBoard((i,j)) and (self._board._state[i][j]=="*" or self._board.isOnSameSide((x,y),(j,j))):
#                legalMoves.append((i,j))
#            (i,j) = (x,y)

    def cannon_moveList(self,(x,y)):
        """
        args : (x,y)  (the current cooordinate)
        return : Cannon move list: move orthogonally but capturing other pieces needs to hop over a third piece
        """
        legalMoves = []
        unitSteps = [(-1,0),(0,-1),(1,0),(0,1)]
        (i,j) = (x,y)

        for unitStep in unitSteps:
            (i,j) = self.add_tuple((i,j) , unitStep)
            while self._board.isOnBoard((i,j)) and self._board._state[i][j]=="*":
                #print "the first while loop (i,j) = ",(i,j)
                legalMoves.append(((x,y),(i,j)))
                (i,j) = self.add_tuple((i,j) , unitStep)
            if self._board.isOnBoard((i,j)):# come across obstacle piece
                #check capturing possibility
                (i,j) = self.add_tuple((i,j) , unitStep)
                while self._board.isOnBoard((i,j)) and self._board._state[i][j]=="*":
                    (i,j) = self.add_tuple((i,j) , unitStep)
                    continue
                if self._board.isOnBoard((i,j)) and not self._board.isOnSameSide((x,y),(i,j)):# come across obstacle piece
                    legalMoves.append(((x,y),(i,j)))
            (i,j) = (x,y)

        return legalMoves

    def pawn_moveList(self,(x,y)):
        """
        args : (x,y)  (the current cooordinate)
        return : Pawn move list: move forward before crossing the river and move forward or left or right by one step after crossing the river
        """
        legalMoves = []
        (i,j) = (x,y)
        if self._board.onRedSide((x,y)):
            unitSteps = [(-1,0),(0,-1),(0,1)]
            if x>4: # before crossing the river
                (i,j) = (i-1,j)
                if self._board.getPiece((i,j)) == "*" or not self._board.isOnSameSide((x,y),(i,j)): # before crossing the river
                    legalMoves.append(((x,y),(i,j)))
            else: # after crossing the river
                for unitStep in unitSteps:
                    (i,j) = self.add_tuple((i,j) , unitStep)
                    if self._board.getPiece((i,j)) == "*" or not self._board.isOnSameSide((x,y),(i,j)): # before crossing the river
                        legalMoves.append(((x,y),(i,j)))
                    (i,j) = (x,y)
        else: # on the black side
            unitSteps = [(1,0),(0,1),(0,-1)]
            if x<5: # before crossing the river
                (i,j) = (i+1,j)
                if self._board.getPiece((i,j)) == "*" or not self._board.isOnSameSide((x,y),(i,j)): # before crossing the river
                    legalMoves.append(((x,y),(i,j)))
            else: # after crossing the river
                for unitStep in unitSteps:
                    (i,j) = self.add_tuple((i,j) , unitStep)
                    if self._board.getPiece((i,j)) == "*" or not self._board.isOnSameSide((x,y),(i,j)): # before crossing the river
                        legalMoves.append(((x,y),(i,j)))
                    (i,j) = (x,y)
        return legalMoves

    def king_moveList(self,(x,y)):
        """
        args : (x,y)  (the current cooordinate)
        return : King move list: move one step orthogonally in palace
        """
        legalMoves = []
        unitSteps = [(-1,0),(0,-1),(1,0),(0,1)]
        (i,j) = (x,y)
        for unitStep in unitSteps:
           # print "testing====how many time king unitstep"
            (i,j) = self.add_tuple((i,j) , unitStep)
            if self._board.isInPalace((i,j)) and ( self._board.getPiece((i,j))=="*" or not self._board.isOnSameSide((x,y),(i,j))):
                legalMoves.append(((x,y),(i,j)))
            (i,j) = (x,y)

        return legalMoves

    def add_tuple(self,t1,t2):
        return tuple(x + y for x, y in zip(t1,t2))


if __name__ == "__main__":
    print "=============Testing for Chess move rules==========="
    print "For testing use, import the board module for Board class first"
    board_for_test = Board()
    board_for_test.printBoard()
    moveRuleHandler = MoveRuleHandler(board_for_test)

    print "=====King :  king_moveList====="
    print "Black King : ",moveRuleHandler.king_moveList((0,4))
    print "Red King : ",moveRuleHandler.king_moveList((9,4))
    print "Black Advisor (0,3) : ",moveRuleHandler.advisor_moveList((0,3))
    print "Red Advisor (9,5) : ",moveRuleHandler.advisor_moveList((9,5))
    print "Black Elephant (0,6) : ",moveRuleHandler.elephant_moveList((0,6))
    print "Red Elephant (9,2) : ",moveRuleHandler.elephant_moveList((9,2))
    print "have not checked about elephant eye yet"
    print "Black Horse(0,1) : ",moveRuleHandler.horse_movelist((0,1))
    print "Red Horse(9,7) : ",moveRuleHandler.horse_movelist((9,7))
    print "Black Rook(0,0) : ",moveRuleHandler.rook_moveList((0,0))
    print "Red Rook(9,8) : ",moveRuleHandler.rook_moveList((9,8))
    print "Black Cannon(2,7) : ",moveRuleHandler.cannon_moveList((2,7))
    print "Red Cannon(7,1) : ",moveRuleHandler.cannon_moveList((7,1))
    print "Black Pawn(3,0) : ",moveRuleHandler.pawn_moveList((3,0))
    print "Black Pawn(3,6) : ",moveRuleHandler.pawn_moveList((3,6))
    print "Red Pawn(6,2) : ",moveRuleHandler.pawn_moveList((6,2))
    print "Red Pawn(6,4) : ",moveRuleHandler.pawn_moveList((6,4))

    print "Make a new board for testing obstacle(especially for horse and elephant) and capturing moves"
    board_for_test.makeMove(((9,7),(7,6)))
    print "======after makeMove((9,7),(7,6))=========="
    board_for_test.printBoard()
    print "Red Cannon(7,7) : ",moveRuleHandler.cannon_moveList((7,7))
    print "Red Horse(7,6) : ",moveRuleHandler.horse_movelist((7,6))

    print "Good Job!"
    print "======after unmakeMove((9,7),(7,6))=========="
    board_for_test.unmakeMove(((9,7),(7,6)))
    board_for_test.printBoard()
    print "============RED ROOK ATTACKING BLACK CANNON========================="
    print "======after makeMove((9,8),(8,8))============"
    board_for_test.makeMove(((9,8),(8,8)))
    board_for_test.printBoard()
    print "======after makeMove((8,8),(8,5))============"
    board_for_test.makeMove(((8,8),(8,5)))
    board_for_test.printBoard()
    print "======after makeMove((8,5),(2,5))============"
    board_for_test.makeMove(((8,5),(2,5)))
    board_for_test.printBoard()
    print "Red Rook(2,5) : ",moveRuleHandler.rook_moveList((2,5))


    print "===========Testing for isMoveLegal() is done in board.py========"
