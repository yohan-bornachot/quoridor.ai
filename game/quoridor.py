from player import Player
from board import Board

class Quoridor:

    def __init__(self, size = 9, nb_walls = 10, wall_size = 2) -> None:
        
        self.size = size

        self.current_player = 0
        self.player0 = Player(0, self.size/2+1, nb_walls)
        self.player1 = Player(self.size, self.size/2+1, nb_walls)
        self.board = Board(self.size, wall_size)