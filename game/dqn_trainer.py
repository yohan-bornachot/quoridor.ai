from AI.dqn.DQNAi import DQN
from AI.dqn.QNet import QNet
from AI.dqn.dqn_config import DQNConfig

from player import Player
from board import Board
from gamestate import GameState

from torch import load, no_grad, save
import numpy as np
import random as rd
from datetime import datetime

class DQNTrainer : 
    def __init__(self):

        config = DQNConfig().config
        
        self.net =  QNet(board_size=config["game"]["board_size"], nb_channels= config["model"]["nb_channels"],
        kernel_size=config["model"]["kernel_size"], mlp_sizes=config["model"]["mlp_sizes"], nb_futur_states=config["game"]["nb_futur_states"])

        PATH = config["model"]["input_weight"]
        if  PATH != None:
            self.net.load_state_dict(load(PATH))

        self.ai = DQN(play_as=0, time_to_play=5, board_size=config["game"]["board_size"], check_licit=False, eps = config["learning"]["eps"],
        eps_decay=config["learning"]["eps_decay"],min_eps=config["learning"]["eps_min"], gamma=config["learning"]["gamma"],
        network=self.net, lr = config["learning"]["lr"] )

        self.nb_players = 2

        self.gamma = config["learning"]["gamma"]

        self.nb_step = 0

        self.size = config["game"]["board_size"]
        self.nb_walls = config["game"]["board_size"]//self.nb_players

        self.nb_samples_to_train = config["learning"]["nb_samples_to_train"]
        self.nb_training = config["learning"]["nb_training"]
        self.batch_size = config["learning"]["batch_size"]

        self.path_to_save = config["learning"]["output_weight"]

        self.nb_games = 0

        self.state_stack = list()
        self.next_state_stack = list()
        self.reward_stack = list()
        self.action_stack = list()

    
    def init_game(self):
        players = [Player(0, self.size//2, self.nb_walls, self.size-1, None),
                    Player(self.size-1, self.size//2, self.nb_walls, 0, None)]
        wall_size = 2
        board = Board(self.size, wall_size, np.zeros((self.size-1, self.size-1)), np.zeros((self.size-1, self.size-1)))
        self.game_state = GameState(players, board, [self.size for _ in range(self.nb_players)],  0)


    def play_game(self):

        current_rewards = list()
        current_gamma = 1

        while not self.game_state.is_terminal():

            self.nb_step += 1
            

            next_states = self.game_state.next_gamestates()
            current_player_idx = self.game_state.current_player_idx


            self.ai.switch_player(current_player_idx)
            with no_grad():
                idx_action = self.ai.policy(self.game_state)
            legal = self.ai.legal_move(self.game_state, idx_action)
            if legal == None :
                self.state_stack.append(self.game_state)
                self.next_state_stack.append(self.game_state)
                self.action_stack.append(idx_action)
                current_rewards.append(0)
                idx_action = rd.randint(0, len(next_states)-1)
                next_step = next_states[idx_action]
            else :
                next_step = next_states[legal]
            
            self.state_stack.append(self.game_state)
            self.next_state_stack.append(next_step)
            self.action_stack.append(idx_action)
            current_rewards.append((2*current_player_idx-1)*current_gamma)

            if current_player_idx == 1 :
                current_gamma *= self.gamma

            self.game_state = next_step

        winner = self.game_state.get_winner()
        current_rewards = (2*winner-1)*np.array(current_rewards)
        current_rewards += (-current_gamma/2)*(current_rewards==0)
        current_rewards = (current_gamma / np.array(current_rewards))
        self.reward_stack = self.reward_stack + current_rewards.tolist()


    def create_batch(self):
        # TODO : créer les batchs pour l'entrainement
        pass

    def reset_stacks(self):
        self.state_stack = list()
        self.next_state_stack = list()
        self.reward_stack = list()
        self.action_stack = list()

    def train_dqn(self):
        for training in range(self.nb_training):
            print("Training {}/{}".format(training,self.nb_training))

            self.reset_stacks()

            while len(self.action_stack) < self.nb_samples_to_train:
                self.init_game()
                self.play_game()
                self.nb_games += 1
            
            batches = self.create_batch()
            for batch in batches:
                states, rewards, next_states, actions = batch
                self.ai.train_on_batch(states, rewards, next_states, actions)

            self.ai.decrease_eps()
            self.ai.update_target()
        print("Fin de l'entrainement, nombre de parties jouées : {}".format(self.nb_games))

        date = str(datetime.today()).split('.')[0].replace(' ','_')
        save(self.ai.net.state_dict(), self.path_to_save+date+".h5")
        
