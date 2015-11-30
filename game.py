# class of Game, organize the whole chess game logic and processing
# with 4 main workers

# userHandler : to handle the user input and directly interate with the users
# searchHandler : contain the minimax with alpha-beta pruning search process
# KBHandler 
# UIHandler : some text format for print out

from board import Board
#import userHandler
#import searchHandler
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
#        self.userHandler = UserHandler()
#        self.searchHandler = SearchHandler()
        self.uiHandler = UIHandler(self.board)
        
        #self.run()
    
    def run(self):
        uiHandler.printInit()
        uiHandler.printBoard() #the initial board state
        while True:
            # (OldCoord,newCoord) in the form of ((0,1),(4,3)),illegal intentions are dealt with by userHandler
            (oldCoord,newCoord) = userHandler.askLegalMove(self.board) 
            self.board.pieceMove((oldCoord,newCoord)) #player move, board state updated
            uiHandler.printBoard()
            if self.checkOver():
                break
            (oldCoord,newCoord) = searchHandler.getBestMove(self.board)
            self.board.pieceMove((oldCoord,newCoord)) # computer move, board state updated
            uiHandler.printBoard()
            if self.checkOver():
                break



    def checkOver(self):
        winner = self.board.checkWinner()
        if not winner:
            print "Game over!", winner, "Won !"
            return True
        else:
            return False


        


if __name__ =="__main__":
    print "Testing for chess game"
    game = Game()
    game.uiHandler.printInit() 
