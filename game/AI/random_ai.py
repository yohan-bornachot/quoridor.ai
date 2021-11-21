from random import randint
from .ai import AI

class RandomAI(AI):

    def __init__(self, time_to_play) -> None:
        super().__init__(time_to_play)

    def select_next_step(self, next_steps):
        return next_steps[randint(0,len(next_steps)-1)]