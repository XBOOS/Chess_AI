# contain the piece moving rules of Chinese Chess
# Imply the rules by possbile moves
class MoveRuleHandler:

    def __init__(self,board):
        self._board = board

# for moves capable of capturing other pieces
    def captureMoves(self):
        return

    def positionMoves(self):
        return
    def isPatternLegal(self,piece,(oldCoord,newCoord)):
        """
        check the moving pattern, regardless of target position availability
        """
        if piece.upper()=="R": #for Rook
            if oldCoord[0]==newCoord[0]: # on the same row
                #check obstacle
                for col in range(min(oldCoord[1],newCoord[1])+1,max(oldCoord[1],newCoord[1])):
                    if self._board._state[oldCoord[0]][col]!="*":
                        return False
            elif oldCoord[1]==newCoord[1]: # on the same column
                for row in range(min(oldCoord[0],newCoord[0])+1,max(oldCoord[1],newCoord[1])):
                    if self._board._state[oldCoord[row]][1]!="*":
                        return False
            else: # now on the same line
                return False
            return True
        elif piece.upper()=="H": #for Horse
            # only : so  (x1-x2)*(y1-y2)==2
            if (oldCoord[0]-newCoord[0])*(oldCoord[1]-newCoord[1])==2:
                if




    """
    The legal move list generation takes move quality into consideration
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
            (i,j) += unitStep
            while self._board.isOnBoard((i,j)) and self._board._state[i][j]=="*":
                legalMoves.append(((x,y),(i,j)))
                (i,j) += unitStep
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
        unitSteps = {(-1,0):[(-2,1),(-2,1)],(0,-1):[(1,-2),(-1,-2)],(1,0):[(2,1),(2,-1)],(0,1):[(1,2),(-1,2)]}
        (i,j) = (x,y)
        for ob_step in unitSteps: #the key is position of obstacle
            obstacle = (x,y)+ob_step
            # get out of board or get horse's "leg" obstacled
            if not self._board.isOnBoard(obstacle) or self._board._state[obstacle[0]][obstacle[1]]] !="*":
                continue
            for tmp in unitSteps[obstacle]:
                (i,j) +=tmp
                if self._board.isOnBoard((i,j)) and (self._board._state[i][j]=="*" or self._board.isOnSameSide((x,y),(j,j))):
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
            (i,j) += unitStep

            # check the elephant eye is obstacled or not
            if not self._board.isOnBoard(obstacle) or self._board._state[obstacle[0]][obstacle[1]]] !="*":
                continue
            (i,j)+=unitStep
            if self._board.isOnBoard((i,j)) and (self._board._state[i][j]=="*" or self._board.isOnSameSide((x,y),(j,j))):
                if self._board.onRedSide((x,y)) and x<5:#cross the river
                    continue
                elif not self._board.onRed((x,y)) and x>4:#cross the river
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
            (i,j) += unitStep
            while self._board.isOnBoard((i,j)) and self._board._state[i][j]=="*":
                legalMoves.append(((x,y),(i,j)))
                (i,j) += unitStep
            if self._board.isOnBoard((i,j)):# come across obstacle piece
                #check capturing possibility
                (i,j) += unitStep
                while self._board.isOnBoard((i,j)) and self._board._state[i][j]=="*":
                    pass
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
                (i,j) += (-1,0)
                if self._board.getPiece((i,j)) == "*" or not self._board.isOnSameSide((x,y),(i,j)): # before crossing the river
                    legalMoves.append((x,y),(i,j))
            else: # after crossing the river
                for unitStep in unitSteps:
                    (i,j) += unitStep
                    if self._board.getPiece((i,j)) == "*" or not self._board.isOnSameSide((x,y),(i,j)): # before crossing the river
                        legalMoves.append((x,y),(i,j))
                    (i,j) = (x,y)
        else: # on the black side
            unitSteps = [(1,0),(0,1),(0,-1)]
            if x<5: # before crossing the river
                (i,j) += (1,0)
                if self._board.getPiece((i,j)) == "*" or not self._board.isOnSameSide((x,y),(i,j)): # before crossing the river
                    legalMoves.append((x,y),(i,j))
            else: # after crossing the river
                for unitStep in unitSteps:
                    (i,j) += unitStep
                    if self._board.getPiece((i,j)) == "*" or not self._board.isOnSameSide((x,y),(i,j)): # before crossing the river
                        legalMoves.append((x,y),(i,j))
                    (i,j) = (x,y)
        return legalMoves

    def king_moveList(self,(x,y)):
        """
        args : (x,y)  (the current cooordinate)
        return : King move list: move one step orthogonally in palace
        """
        legalMoves = []
        unitSteps = [(-1,0),(0,-1),(1,0),(1,0)]
        (i,j) = (x,y)
        for unitStep in unitSteps:
            (i,j) += unitStep
            if self._board.isInPalace((i,j)) and not self.board.isOnSameSide((x,y),(i,j)):
                legalMoves.append((x,y),(i,j))
            (i,j) = (x,y)

        return legalMoves
























