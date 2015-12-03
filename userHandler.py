#!/usr/bin/env python
# encoding: utf-8

class UserHandler:
    def __inti__(self):
        return
    def askLegalMove(self,board):
        """
        board for the current board
        return legal move (oldCoord,newCoord)
        """
        legal = False
        msg = "Game start!"
        while not legal:
            print msg
            user_input = raw_input("Piece to move ? (0~9),(0~8) : ")
            oldCoord = tuple(map(int,(user_input.split(","))))

            user_input = raw_input("Position to go ? (0~9),(0~8) : ")
            newCoord = tuple(map(int,(user_input.split(","))))
            (legal,msg) = self.isMoveLegal(board,oldCoord,newCoord)

        return (oldCoord,newCoord)

    def isMoveLegal(self,board,oldCoord,newCoord):
        """
        Check wether the user input is legal.
        1. The original piece coordinate must red piece
        2. Other checking can be done by Board.isMoveLegal()
        """
        if not board.isOnBoard(oldCoord):
            return (False,"position not on board!")
        elif not board.onRedSide(oldCoord):
            return (False,"You can only move red piece! (Upper char)")
        else:
            return (board.isMoveLegal((oldCoord,newCoord)),"Illegal move!")




