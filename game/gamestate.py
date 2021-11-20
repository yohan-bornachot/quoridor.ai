from player import Player
from board import Board

class GameState:

    def __init__(self, player1, player2, board, current_player = 1) -> None:
        self.player1 = player1
        self.player2 = player2
        self.board = board
        self.current_player = current_player

    def next_gamesteps(self):
        
