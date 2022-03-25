import numpy as np
import time
import sys
from random import shuffle
from typing import List

from .ai import AI
sys.path.append("..")
from gamestate import GameState

def basic_heuristic(D1, D2, d1, d2):
    return d1 - D1 + D2 - d2

class MinimaxAI(AI):

    def __init__(self, objective_function, play_as, time_to_play: float) -> None:
        super().__init__(play_as, time_to_play)
        self.objective_function = objective_function

    def minimax(self, state: GameState, remaining_time: float, depth : int = 0) -> float:
        t0 = time.time()
        eps = 10e-2

        maximize = self.play_as == state.current_player

        p = state.current_player
        q = (p+1)%2

        if remaining_time<=eps or state.is_terminal():
            value = self.objective_function(state.objectives[q], 
                                            state.objectives[p],
                                            state.players[q].get_nb_wall(),
                                            state.players[p].get_nb_wall())
            return value
        next_gamestates = state.next_gamestates()
        
        pruned_states = list()
        for futur_state in next_gamestates:
            ev_dist = basic_heuristic(futur_state.objectives[p], futur_state.objectives[q], state.objectives[p], state.objectives[q])
            if ev_dist > (0 if len(pruned_states)>0 else -1):
                pruned_states.append(futur_state)
        n = len(pruned_states)
        shuffle(pruned_states)

        f = max if maximize else min
        value = self.minimax(next_gamestates[0], (remaining_time - time.time() + t0)/n, depth +1)
        for i in range(1,n):
            given_time = (remaining_time - time.time() + t0)/(n-i)
            value = f(value, self.minimax(pruned_states[i], given_time, depth + 1))
        return value

        
    def select_next_step(self, game_state: GameState, next_steps: List[GameState]) -> GameState:
        start = time.time()
        other = (self.play_as + 1)%game_state.nb_players

        pruned_states = list()
        dist = list()
        for state in next_steps:
            ev_dist = basic_heuristic(state.objectives[self.play_as], state.objectives[other],
                        game_state.objectives[self.play_as], game_state.objectives[other])
            dist.append(ev_dist)
            if ev_dist >(0 if len(pruned_states)>0 else -1) :
                pruned_states.append(state)
        n = len(pruned_states)
        
        if n == 1:
            return pruned_states[0]

        shuffle(pruned_states)

        remaining_time = (self.time_to_play - time.time() + start)/n
        best_val = self.minimax(next_steps[0], remaining_time)
        best_index = 0

        for i in range(1, n):
            remaining_time = (self.time_to_play - time.time() + start)/(n-i)
            value =  self.minimax(pruned_states[i], remaining_time)
            if value == max(best_val, value):
                best_val = value
                best_index = i
        
        return pruned_states[best_index]
