from .ai import AI
from random import randint

class RandomAI(AI):

    def __init__(self,play_as, time_to_play) -> None:
        super().__init__(play_as,time_to_play)

    def select_next_step(self, next_steps, *args, **kwargs):
        return next_steps[randint(0,len(next_steps)-1)]