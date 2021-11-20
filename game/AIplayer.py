from ..AI.random import RandomAI

class AIPlayer:

    def __init__(self, name) -> None:
        if name == "random":
            self.ai = RandomAI()

    def select_next_step(self, next_steps):
        return self.ai.select_next_step(next_steps)