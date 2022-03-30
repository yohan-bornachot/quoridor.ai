from AI.randomAI import RandomAI
from AI.sortAI import SortAI
from AI.minimaxAI import MinimaxAI
from AI.DQNAi import DQN
from AI.objectif_f import basic_objective

from AI.dqn.dqn_config import DQNConfig
from AI.dqn.QNet import QNet
from torch import load

class AIPlayer:

    def __init__(self, name, play_as, time_to_play, board_size, *args, **kwargs) -> None:

        gamma = kwargs.get("gamma")

        if name == "random":
            self.ai = RandomAI(play_as, time_to_play)   
        elif name=="minimax":
           self.ai = MinimaxAI(basic_objective, play_as, time_to_play)
        elif name == "greedy":
            self.ai = SortAI(basic_objective, gamma, play_as, time_to_play)
        elif name == "sortAI":
            self.ai = SortAI(basic_objective, gamma, play_as, time_to_play)
        elif name == "dqn" : 
            config = DQNConfig().config

            net =  QNet(board_size=config["game"]["board_size"], nb_channels= config["model"]["nb_channels"],
            kernel_size=config["model"]["kernel_size"], mlp_sizes=config["model"]["mlp_size"], nb_futur_states=config["game"]["nb_futur_states"])
            net.load_state_dict(load("/Users/W4kee/Documents/Projets/quoridor.ai/game/AI/dqn/trained_files/2022-03-27_15_53_40_epoch39.h5"))

            self.ai = DQN(play_as = play_as, time_to_play = time_to_play, board_size = board_size,
            nb_walls = config["game"]["nb_walls"], check_licit = True, eps = 0., eps_decay = 1,
            min_eps = 0., gamma = config["learning"]["gamma"], network = net, lr = 1e-3)

    def select_next_step(self,game_state, next_steps):
        return self.ai.select_next_step(game_state, next_steps)

    def switch_player(self, play_as):
        self.ai.switch_player(play_as)