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

    def __init__(self, AIs, nb_players = 2, size = 9, nb_walls = 20, wall_size = 2, time_to_play = 2, gammas = None) -> None:

        self.nb_players = nb_players

        if gammas == None:
            gammas = [0.3 for _ in range(self.nb_players)]
        
        self.nb_step = 0

        self.size = size
        self.time_to_play = time_to_play

        self.nb_walls = nb_walls//nb_players

        current_player = 0
        if self.nb_players == 2 :
            players = [Player(0, self.size//2, self.nb_walls, self.size-1, None),
                        Player(self.size-1, self.size//2, self.nb_walls, 0, None)]
        elif self.nb_players == 4 : 
            players = [Player(0, self.size//2, self.nb_walls, self.size-1, None),
                        Player(self.size-1, self.size//2, self.nb_walls, 0, None),
                        Player(self.size//2, 0, self.nb_walls, None, self.size-1),
                        Player(self.size//2, self.size-1, self.nb_walls, None, 0)]

        board = Board(self.size, wall_size, np.zeros((size-1, size-1)), np.zeros((size-1, size-1)))

        self.AIs = [AIPlayer(AIs[i], play_as=i, time_to_play=time_to_play, gamma = gammas[i], board_size = size) for i in range(self.nb_players)]

        self.game_state = GameState(players, board, [self.size for _ in range(self.nb_players)],  current_player)

    def play(self, verbose = True):
        self.game_start = time()

        while not self.game_state.is_terminal():

            self.nb_step += 1
            
            if verbose : 
                display_board(self.game_state)
                sleep(0.5)

            next_states = self.game_state.next_gamestates()
            current_player_idx = self.game_state.current_player_idx

            next_step = self.AIs[current_player_idx].select_next_step(self.game_state, next_states)

            self.game_state = next_step

        if verbose : display_board(self.game_state)

        self.game_stop = time()

    def get_winner(self):
        return self.game_state.get_winner()

    def get_nb_step(self):
        return self.nb_step


if __name__ == "__main__":

    nb_players = [2, 4]
    ai_types = ["random", "minimax", "greedy", "sortAI", "dqn"]
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default= 2, choices= nb_players, help = "Number of players on the board")
    parser.add_argument("--ai1", default="dqn", choices=ai_types, help="player1 AI to be implemented")
    parser.add_argument("--ai2", default="minimax", choices=ai_types, help="player2 AI to be implemented")
    parser.add_argument("--ai3", default="sortAI", choices=ai_types, help="player3 AI to be implemented")
    parser.add_argument("--ai4", default="sortAI", choices=ai_types, help="player4 AI to be implemented")
    parser.add_argument("--v", type=bool, default=False, help= "Set this variable to False if you don't need to see the board")
    args = parser.parse_args()

    for _ in range(1):
        if args.n == 2:
            q = Quoridor([args.ai1, args.ai2])
        if args.n == 4 :
            q = Quoridor([args.ai1, args.ai2, args.ai3, args.ai4], nb_players= 4)
        q.play(verbose=args.v)

        print("Winner is player : {}. Number of steps : {}. Temps joué {}".format(q.get_winner(),q.get_nb_step(), q.game_stop-q.game_start))
        print("Mean time by step : {}".format((q.game_stop-q.game_start)/q.nb_step))
