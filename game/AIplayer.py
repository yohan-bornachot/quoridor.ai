from AI.randomAI import RandomAI
from AI.sortAI import SortAI
#from AI.min_max_ai import MinimaxAI 
from AI.objectif_f import basic_objective

class AIPlayer:

    def __init__(self, name, play_as, time_to_play) -> None:
        if name == "random":
            self.ai = RandomAI(play_as, time_to_play)
        #elif name=="minimax":
        #    self.ai = MinimaxAI(time_to_play, basic_objective)
        elif name == "greedy":
            self.ai = SortAI(basic_objective, play_as, time_to_play)

    def select_next_step(self, next_steps):
        return self.ai.select_next_step(next_steps)