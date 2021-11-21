import sys
import numpy as np

from player import Player
from board import Board
from gamestate import GameState
from AIplayer import AIPlayer
from display import display_board

class Quoridor:

    def __init__(self, ai1, ai2, size = 9, nb_walls = 10, wall_size = 2) -> None:
        
        self.nb_step = 0

        self.size = size

        current_player = 1
        player1 = Player(0, self.size/2+1, nb_walls, self.size)
        player2 = Player(self.size, self.size/2+1, nb_walls, 0)
        board = Board(self.size, wall_size, np.zeros((size-1, size-1)), np.zeros((size-1, size-1)))

        self.ai1 = AIPlayer(ai1)
        self.ai2 = AIPlayer(ai2)


        self.game_state = GameState(player1, player2, board, current_player)

    def game_over(self):
        if self.game_state.player1.i == self.game_state.player1.goal :
            return 1
        
        if self.game_state.player2.i == self.game_state.player2.goal :
            return 2
        
        return 0

    def play(self, verbose = True):

        while self.game_over() == 0:

            self.nb_step += 1
            
            if verbose : display_board(self.game_state)

            next_states = self.game_state.next_gamestates()
            current_player = self.game_state.current_player

            if current_player == 1:
                next_step = self.ai1.select_next_step(next_states)

            if current_player == 2:
                next_step = self.ai2.select_next_step(next_states)

            self.game_state = next_step

        if verbose : display_board(self.game_state)

    def get_winner(self):
        return self.game_over()

    def get_nb_step(self):
        return self.nb_step


if __name__ == "__main__":
    ai1 = sys.argv[1]
    ai2 = sys.argv[2]

    q = Quoridor(ai1, ai2)
    q.play()

    print("Winner is player : {}. Number of steps : {}".format(q.get_winner(),q.get_nb_step()))
        
