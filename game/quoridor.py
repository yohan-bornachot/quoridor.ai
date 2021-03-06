from functools import total_ordering
import sys
import numpy as np
import argparse

from time import sleep, time

from player import Player
from board import Board
from gamestate import GameState
from AIplayer import AIPlayer
from display import display_board

class Quoridor:

    def __init__(self, ai1, ai2, size = 9, nb_walls = 10, wall_size = 2, time_to_play = 1) -> None:
        self.nb_step = 0

        self.size = size
        self.time_to_play = time_to_play

        current_player = 1
        player1 = Player(0, self.size//2, nb_walls, self.size-1)
        player2 = Player(self.size-1, self.size//2, nb_walls, 0)
        board = Board(self.size, wall_size, np.zeros((size-1, size-1)), np.zeros((size-1, size-1)))

        self.ai1 = AIPlayer(ai1, play_as=1, time_to_play=time_to_play, gamma = 0.2)
        self.ai2 = AIPlayer(ai2, play_as=2, time_to_play=time_to_play, gamma = 0.3)


        self.game_state = GameState(player1, player2, board, self.size-1, self.size-1,  current_player)

    def play(self, verbose = True):
        self.game_start = time()

        while not self.game_state.is_terminal():

            self.nb_step += 1
            
            if verbose : 
                display_board(self.game_state)
                #sleep(0.5)

            next_states = self.game_state.next_gamestates()
            current_player = self.game_state.current_player


            if current_player == 1:
                next_step = self.ai1.select_next_step(self.game_state, next_states)

            if current_player == 2:
                next_step = self.ai2.select_next_step(self.game_state, next_states)

            self.game_state = next_step

        if verbose : display_board(self.game_state)

        self.game_stop = time()

    def get_winner(self):
        if self.game_state.player1.i == self.game_state.player1.goal :
            return 1
        if self.game_state.player2.i == self.game_state.player2.goal :
            return 2

    def get_nb_step(self):
        return self.nb_step


if __name__ == "__main__":

    ai_types = ["random", "minimax", "greedy", "sortAI"]
    parser = argparse.ArgumentParser()
    parser.add_argument("--ai1", default="random", choices=ai_types, help="player1 AI to be implemented")
    parser.add_argument("--ai2", default="random", choices=ai_types, help="player2 AI to be implemented")
    args = parser.parse_args()

    for _ in range(1):
        q = Quoridor(args.ai1, args.ai2)
        q.play(verbose=True)

        print("Winner is player : {}. Number of steps : {}. Temps jou?? {}".format(q.get_winner(),q.get_nb_step(), q.game_stop-q.game_start))
        print("Mean time by step : {}".format((q.game_stop-q.game_start)/q.nb_step))
