# contain the piece moving rules of Chinese Chess
# imply the rules by possbile moves
class MoveRuleHandler:

    def __init__(self,board):
        self._board = board

# for moves capable of capturing other pieces
    def captureMoves():
        return

    def positionMoves():
        return
    def isPatternLegal(piece,(oldCoord,newCoord)):
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
            if
            #i feel i am really a little bit clever? :) :)



    def rook_moveList(coord):
        """
        args : coord (the current cooordinate)
        return : possible moves only depending on single piece moving rule
        """


