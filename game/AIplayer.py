from AI.random import RandomAI
#from AI.min_max_ai import MinimaxAI 
from AI.objectif_f import basic_objective

class AIPlayer:

    def __init__(self, name, time_to_play) -> None:
        if name == "random":
            self.ai = RandomAI(time_to_play)
        #elif name=="minimax":
        #    self.ai = MinimaxAI(time_to_play, basic_objective)

    def select_next_step(self, next_steps):
        return self.ai.select_next_step(next_steps)