# class of Game, organize the whole chess game logic and processing
# with 4 main workers

# userHandler : to handle the user input and directly interate with the users
# searchHandler : contain the minimax with alpha-beta pruning search process
# KBHandler
# UIHandler : some text format for print out

from board import Board
from userHandler import UserHandler
from searchHandler import SearchHandler
from uiHandler import UIHandler
class Game:
    """
    whole game object
    maintain some game status
    including a game board ( class Board )
    delegate work to different handlers
    """
    def __init__(self):
#initialize and start the game

        self.board = Board()
        self.userHandler = UserHandler()
        """  ********  You can control the search broadth for each layer here, the default is 20"""
        self.searchHandler = SearchHandler(self.board,20)
        self.uiHandler = UIHandler(self.board)

        self.run()

    def run(self):
        self.uiHandler.printInit()
        self.uiHandler.printBoard() #the initial board state
        while True:
            # (OldCoord,newCoord) in the form of ((0,1),(4,3)),illegal intentions are dealt with by userHandler
            (oldCoord,newCoord) = self.userHandler.askLegalMove(self.board)
            self.board.makeMove((oldCoord,newCoord)) #player move, board state updated
            self.uiHandler.printBoard()
            if self.checkOver():
                exit()
            (oldCoord,newCoord) = self.searchHandler.getBestMove(4)
            print "*************Computer's move ",(oldCoord,newCoord),"****************"
            self.board.makeMove((oldCoord,newCoord)) # computer move, board state updated
            self.uiHandler.printBoard()
            if self.checkOver():
               exit()



    def checkOver(self):
        winner = self.board.checkWinner()
        if winner:
            print "Game over!", winner, "Won !"
            return True
        else:
            return False





if __name__ =="__main__":
    print "Testing for chess game"
    game = Game()
    game.uiHandler.printInit()
