from AI.DQNAiV2 import DQNV2
from AI.dqn.QNet import QNet
from AI.dqn.dqn_config import DQNConfig

from player import Player
from board import Board
from gamestate import GameState

from torch import load, no_grad, save, tensor, squeeze, unsqueeze, vstack, argmax, where, ones_like, zeros_like
import numpy as np
import random as rd
from datetime import datetime
from copy import deepcopy


class DQNTrainerV2 : 
    def __init__(self):

        config = DQNConfig().config
        
        self.net =  QNet(board_size=config["game"]["board_size"], nb_channels= config["model"]["nb_channels"],
        kernel_size=config["model"]["kernel_size"], mlp_sizes=config["model"]["mlp_size"], nb_futur_states=config["game"]["nb_futur_states"])

        self.rules_net = QNet(board_size=config["game"]["board_size"], nb_channels= config["model"]["nb_channels"],
        kernel_size=config["model"]["kernel_size"], mlp_sizes=config["model"]["mlp_size"], nb_futur_states=config["game"]["nb_futur_states"], used_for="rules")

        PATH = config["model"]["input_weight"]
        if  PATH != None:
            self.net.load_state_dict(load(PATH))

        self.ai = DQNV2(play_as=0, time_to_play=5, board_size=config["game"]["board_size"], nb_walls=config["game"]["nb_walls"], check_licit=False,  eps = config["learning"]["eps"],
        eps_decay=config["learning"]["eps_decay"],min_eps=config["learning"]["eps_min"], gamma=config["learning"]["gamma"],
        reward_network=self.net, rules_network=self.rules_net, lr = config["learning"]["lr"] )

        self.state_list = self.ai.get_state_list()
        self.state_dic = {}
        for i,state in enumerate(self.state_list):
            self.state_dic[state] = i

        self.nb_players = 2
        self.nb_walls = config["game"]["nb_walls"]

        self.gamma = config["learning"]["gamma"]

        self.nb_step = 0

        self.size = config["game"]["board_size"]
        self.nb_walls = config["game"]["board_size"]//self.nb_players

        self.nb_samples_to_train = config["learning"]["nb_samples_to_train"]
        self.nb_training = config["learning"]["nb_training"]
        self.batch_size = config["learning"]["batch_size"]

        self.path_to_save = config["model"]["output_weight"]

        self.nb_games = 0

        self.state_stack = list()
        self.next_state_stack = list()
        self.reward_stack = list()
        self.action_stack = list()
        self.rules_state_stack = list()
        self.rules_target_stack = list()

    
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
                inputs = self.ai.from_state_to_network_inputs(self.game_state)
                mask = squeeze(self.ai.compute_rules(inputs)) > tensor(self.ai.rules_threshold).to(self.ai.device)
                if rd.random()<self.ai.eps :
                    tmp_idx = rd.randint(0, sum(mask).item()-1)
                    idx_action = 0 
                    while tmp_idx > 0:
                        tmp_idx += - mask[idx_action].item()
                        idx_action += 1
                else:
                    rewards = squeeze(self.ai.compute_rewards(inputs))
                    idx_action = argmax(where(mask == 1, rewards, ones_like(rewards)*min(rewards)))
            

            legal = self.ai.legal_move(self.game_state, idx_action)
            if legal != None :
                self.state_stack.append(self.game_state)
                self.next_state_stack.append(self.game_state)
                self.action_stack.append(idx_action)
                current_rewards.append((2*current_player_idx-1)*current_gamma)
                next_step = next_states[legal]
                self.next_state_stack.append(next_step)
            else :
                idx_action = rd.randint(0, len(next_states)-1)
                next_step = next_states[idx_action]

            
            self.rules_state_stack.append(self.game_state)
            tmp_target = zeros_like(mask)
            for key in self.game_state.possible_moves:
                tmp_target[self.state_dic[key]] = 1
            self.rules_target_stack.append(tmp_target)
            

            if current_player_idx == 1 :
                current_gamma *= self.gamma
            self.game_state = next_step

        winner = self.game_state.get_winner()
        current_rewards = (2*winner-1)*np.array(current_rewards)
        current_rewards = current_gamma / current_rewards
        self.reward_stack = self.reward_stack + current_rewards.tolist()


    def create_states_tensors(self, batch_idx, use_list = "current"):
        c_list = list()
        pos_list = list()
        goals_list = list()
        nb_walls_list =list()
        for idx in batch_idx :
            if use_list == "current":
                state = self.state_stack[idx]
            elif use_list == "next":
                state = self.next_state_stack[idx]
            elif use_list == "rules":
                state = self.rules_state_stack[idx]

            c_1 = unsqueeze(tensor(state.board.walls_h),0)
            c_2 = unsqueeze(tensor(state.board.walls_v),0)
            c = unsqueeze(vstack((c_1,c_2)).float(),0)
            c_list.append(c)

            current_player = state.current_player_idx
            nb_walls = [state.players[current_player].get_nb_wall()]
            pos = [state.players[current_player].i, state.players[current_player].j]
            goals = [state.players[current_player].goal_i]

            for i,player in enumerate(state.players):
                if i!=current_player:
                    nb_walls.append(player.get_nb_wall())
                    pos.append(player.i)
                    pos.append(player.j)
                    goals.append(player.goal_i)
            nb_walls_list.append(unsqueeze(tensor(nb_walls)/self.nb_walls,0))
            pos_list.append(unsqueeze(tensor(pos)/self.size,0))
            goals_list.append(unsqueeze(tensor(goals)/self.size,0))
            
        c = vstack(c_list)
        pos = vstack(pos_list)
        goals = vstack(goals_list)
        nb_walls = vstack(nb_walls_list)
        return c, pos, goals, nb_walls


    def create_batches(self):

        nb_samples = len(self.action_stack)
        ind = [i for i in range(nb_samples)]
        batch_list = list()
        while len(ind)>self.batch_size:
            batch = list()
            for _ in range(self.batch_size):
                i = rd.randint(0, len(ind)-1)
                x = ind.pop(i)
                batch.append(x)
            batch_list.append(batch)
        
        training_batches = list()
        rewards_tensor = tensor(self.reward_stack)
        actions_tensor = tensor(self.action_stack)

        for batch in batch_list :
            rewards = rewards_tensor[batch]
            actions = actions_tensor[batch]
            states = self.create_states_tensors(batch)
            next_states = self.create_states_tensors(batch, "next")
            
            training_batches.append((states, rewards, next_states, actions))

        return training_batches


    def create_rules_batches(self):
        nb_samples = len(self.rules_target_stack)
        ind = [i for i in range(nb_samples)]
        batch_list = list()
        while len(ind)>self.batch_size:
            batch = list()
            for _ in range(self.batch_size):
                i = rd.randint(0, len(ind)-1)
                x = ind.pop(i)
                batch.append(x)
            batch_list.append(batch)
        training_batches = list()

        for batch in batch_list:
            states = self.create_states_tensors(batch, "rules")
            targets = vstack([self.rules_target_stack[idx] for idx in batch])
            training_batches.append((states, targets))
        return training_batches



    def reset_stacks(self):
        self.state_stack = list()
        self.next_state_stack = list()
        self.reward_stack = list()
        self.action_stack = list()
        self.rules_state_stack = list()
        self.rules_target_stack = list()

    def train_dqn(self):
        for training in range(self.nb_training):
            print("## Training {}/{} ##".format(training,self.nb_training))

            self.reset_stacks()

            print("Creation du dataset : jeu")
            while len(self.rules_state_stack) < self.nb_samples_to_train:
                print("\rProcessus effectué à {}%".format(round(100*len(self.rules_state_stack) / self.nb_samples_to_train,4)), end = "")
                self.init_game()
                self.play_game()
                self.nb_games += 1
                
            print("")
            
            print("Proportion d'actions illégales : {}%".format(round(100*(1-len(self.action_stack)/len(self.rules_state_stack)))))
            print("Entrainement du réseau REWARDS")
            batches = self.create_batches()
            loss = 0
            for batch in batches:
                states, rewards, next_states, actions = batch
                loss += self.ai.train_rewards_on_batch(states, rewards, next_states, actions)
            if len(batches) > 0 :
                print("Loss : {}".format(loss/len(batches)))
            else :
                print("Pas assez de données au cours de cette passe.")

            print("Entrainement du réseau RULES")
            batches = self.create_rules_batches()
            loss = 0
            for batch in batches:
                states, targets = batch
                loss += self.ai.train_rules_on_batch(states, targets)
            print("Loss : {}".format(loss/len(batches)))
            

            self.ai.decrease_eps()
            self.ai.update_target()
            
            print("Nombre de parties déjà jouées : {}".format(self.nb_games))
            
            if (training+1)%10 == 0 :
                date = str(datetime.today()).split('.')[0].replace(' ','_')
                cpu_net = deepcopy(self.ai.net).to("cpu")
                save(cpu_net.state_dict(), self.path_to_save+"rewards_"+date+"_epoch{}.h5".format(training))
                cpu_net = deepcopy(self.ai.rules_net).to("cpu")
                save(cpu_net.state_dict(), self.path_to_save+"rules_"+date+"_epoch{}.h5".format(training))
            
            print("")
                
        print("Fin de l'entrainement, nombre de parties jouées : {}".format(self.nb_games))

        date = str(datetime.today()).split('.')[0].replace(' ','_')
        cpu_net = deepcopy(self.ai.net).to("cpu")
        save(cpu_net.state_dict(), self.path_to_save+date+".h5")
        cpu_net = deepcopy(self.ai.rules_net).to("cpu")
        save(cpu_net.state_dict(), self.path_to_save+"rules"+date+".h5")
        
