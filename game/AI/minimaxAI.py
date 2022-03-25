import numpy as np
import time
import sys
from random import shuffle
from typing import List

from .ai import AI
sys.path.append("..")
from gamestate import GameState

def basic_heuristic(futur_obj, current_obj, player):
    n = len(futur_obj)
    mask = np.ones((n))/(n-1)
    mask[player] = - 1
    return np.sum(mask*(np.array(futur_obj) - np.array(current_obj)))

class MinimaxAI(AI):

    def __init__(self, objective_function, play_as, time_to_play: float) -> None:
        super().__init__(play_as, time_to_play)
        self.objective_function = objective_function

    def minimax(self, state: GameState, remaining_time: float, depth : int = 0) -> float:
        t0 = time.time()
        eps = 10e-2

        maximize = self.play_as == state.current_player_idx

        if remaining_time<=eps or state.is_terminal():
            value = self.objective_function(state, state.current_player_idx)
            return value


        next_gamestates = state.next_gamestates()
        
        pruned_states = list()
        for futur_state in next_gamestates:
            ev_dist = basic_heuristic(futur_state.objectives, state.objectives, state.current_player_idx)
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

        pruned_states = list()
        dist = list()
        for state in next_steps:
            ev_dist = basic_heuristic(state.objectives, game_state.objectives, self.play_as)
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
