#!/usr/bin/env python
# encoding: utf-8

class MoveSortHandler:
    """
    The moveRuleHandler produce all possible moves, about 40 each move
    when depth = 4, the alphaBeta search still takes relative long time.
    So I need to sort the move and give it a limit.

    Methodology:
        The searching order has a big influence on the
        performance of alpha-beta pruning
        So i need to adjust to a better order
        Sorting a list of constant length won't take much time, the sorting rule is the matter

        1. Capturing move is has more power than the usual position changing move
        2. Different piece has different power, so being captured is of different loss

        I will sort it according to wether it is capturing move and value(eaten piece)/value(attacker)

    """
    def __init__(self,board,limit=20):
        self._board = board
        self._limit = limit
        return

    def sortLegalMoves(self,moveList):
        #sort the move list according to the move quality value
        return sorted(moveList,key=self._getMoveQuality,reverse=True)[:self._limit]


        return

    def _getMoveQuality(self,move):
        """
        assign relative quality value to a move
        if simple position change : according to the moving piece value
        if capturing : according to the ratio *100

        relative value: King=10,R=4,C=H=3,E=A=2,P=1
        """
        if not self._board.isCaptureMove(move):
            #return self._getPieceValue(self._board.getPiece(move[0]))
            return 0
        else: # capturing move
            attacker = self._board.getPiece(move[0])
            victim= self._board.getPiece(move[1])
            return self._calcRatio(attacker,victim)

    def _getPieceValue(self,piece):
        tmp = piece.upper()
        if tmp == "K":
            return 10
        elif tmp == "R":
            return 4
        elif tmp =="C":
            return 3
        elif tmp =="H":
            return 3
        elif tmp == "E":
            return 2
        elif tmp == "A":
            return 2
        elif tmp == "P":
            return 1
        else:
            raise Exception("Illegal piece syntax")

    def _calcRatio(self,attacker,victim):
        return self._getPieceValue(victim)//self._getPieceValue(attacker)*100
