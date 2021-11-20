from ai import AI
from random import randint

class RandomAI(AI):

    def __init__(self) -> None:
        super().__init__()

    def select_next_step(self, next_steps):
        return next_steps[randint(0,len(next_steps)-1)]