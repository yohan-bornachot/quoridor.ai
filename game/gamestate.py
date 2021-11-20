import numpy as np
from player import Player

class GameState:

    def __init__(self, size = 9, nb_stick = 10) -> None:
        
        self.size = size

        self.current_player = 0
        self.player0 = Player(0, self.size/2+1, nb_stick)
        self.player1 = Player(self.size, self.size/2+1, nb_stick)
