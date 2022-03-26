from numpy.core.fromnumeric import argmax
from .ai import AI

class SortAI(AI):
    def __init__(self, objective_function, gamma, play_as, time_to_play=10) -> None:
        super().__init__(play_as=play_as, time_to_play=time_to_play)
        self.objective_function = objective_function
        self.gamma = gamma


    def select_next_step(self, game_state, next_steps):
        eval = [self.objective_function(state, self.play_as) for state in next_steps]
        return next_steps[argmax(eval)]
    