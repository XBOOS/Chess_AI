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

    def __init__(self,board):

        self._board = board
        return

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
                pieceValue = evaValue(piece)
                positionValue = evaPosition(piece,coord)
                flexibilityValue = evaFlexibility(piece,coord)
                #relationshipValue 
                value += piece_coef*pieceValue + position_coef*positionValue+flexibility_coef*flexibilityValue#+....
        return value        
                


        
