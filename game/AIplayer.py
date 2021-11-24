from AI.randomAI import RandomAI
from AI.sortAI import SortAI
from AI.minimaxAI import MinimaxAI 
from AI.objectif_f import basic_objective

class AIPlayer:

    def __init__(self, name, play_as, time_to_play, *args, **kwargs) -> None:

        if "gamma" in kwargs.keys():
            gamma = kwargs["gamma"]

        if name == "random":
            self.ai = RandomAI(play_as, time_to_play)   
        elif name=="minimax":
           self.ai = MinimaxAI(basic_objective, play_as, time_to_play)
        elif name == "greedy":
            self.ai = SortAI(basic_objective, play_as, time_to_play)
        elif name == "sortAI":
            self.ai = SortAI(basic_objective, gamma, play_as, time_to_play, *args, **kwargs)

    def select_next_step(self,game_state, next_steps):
        return self.ai.select_next_step(game_state, next_steps)