import numpy as np
import time
import sys
from typing import List

from .ai import AI
sys.path.append("..")
from game.gamestate import GameState

class MinimaxAI(AI):

    def __init__(self, objective_function, play_as, time_to_play: float) -> None:
        super().__init__(play_as, time_to_play)
        self.objective_function = objective_function

    def minimax(self, state: GameState, remaining_time: float, maximize: bool) -> float:
        t0 = time.time()
        eps = 10e-2
        if remaining_time<=eps or state.is_terminal():
            value = self.objective_function(state.objective1, 
                                            state.objective2,
                                            state.player1.get_nb_wall(),
                                            state.player2.get_nb_wall())
            return value if maximize else -value
        next_gamestates = state.next_gamestates()
        if maximize:
            value = -np.Infinity
            for next_state in next_gamestates:
                remaining_time -= (time.time()-t0)
                remaining_time /= len(next_gamestates)
                value = max(value, self.minimax(next_state, remaining_time, False))
            return value
        else: # minimizing player
            value = np.Infinity
            for next_state in next_gamestates:
                remaining_time = (time.time()-t0)
                remaining_time /= len(next_gamestates)
                value = min(value, self.minimax(next_state, remaining_time, True))
            return value


    def select_next_step(self, next_steps: List[GameState]) -> GameState:
        best_val = 0
        best_index = 0
        for i in range(len(next_steps)):
            maximize = (self.play_as==1)
            value = self.minimax(next_steps[i], self.time_to_play, maximize)
            if value > best_val and maximize:
                best_val = value
                best_index = i

            elif value < best_val and not maximize:
                best_val = value
                best_index = i

        return next_steps[best_index]