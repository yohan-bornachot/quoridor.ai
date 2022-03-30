from AI.DQNAi import DQN
from AI.dqn.QNet import QNet
from AI.dqn.dqn_config import DQNConfig

from player import Player
from board import Board
from gamestate import GameState

from torch import load, no_grad, save, tensor, unsqueeze, vstack
import numpy as np
import random as rd
from datetime import datetime
from copy import deepcopy


class DQNTrainer : 
    def __init__(self):

        config = DQNConfig().config
        
        self.net =  QNet(board_size=config["game"]["board_size"], nb_channels= config["model"]["nb_channels"],
        kernel_size=config["model"]["kernel_size"], mlp_sizes=config["model"]["mlp_size"], nb_futur_states=config["game"]["nb_futur_states"])

        PATH = config["model"]["input_weight"]
        if  PATH != None:
            self.net.load_state_dict(load(PATH))

        self.ai = DQN(play_as=0, time_to_play=5, board_size=config["game"]["board_size"], nb_walls=config["game"]["nb_walls"], check_licit=False,  eps = config["learning"]["eps"],
        eps_decay=config["learning"]["eps_decay"],min_eps=config["learning"]["eps_min"], gamma=config["learning"]["gamma"],
        network=self.net, lr = config["learning"]["lr"] )

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
        self.illegal_count = 0

    
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
                self.illegal_count += 1
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
            
            c_list = list()
            pos_list = list()
            goals_list = list()
            nb_walls_list =list()
            for idx in batch :
                state = self.state_stack[idx]
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
            states = c, pos, goals, nb_walls
            
            c_list = list()
            pos_list = list()
            goals_list = list()
            nb_walls_list =list()
            for idx in batch :
                state = self.next_state_stack[idx]
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
            next_states = c, pos, goals, nb_walls

            training_batches.append((states, rewards, next_states, actions))

        return training_batches



    def reset_stacks(self):
        self.state_stack = list()
        self.next_state_stack = list()
        self.reward_stack = list()
        self.action_stack = list()
        self.illegal_count = 0

    def train_dqn(self):
        for training in range(self.nb_training):
            print("Training {}/{}".format(training,self.nb_training))

            self.reset_stacks()

            print("Creation du dataset : jeu")
            while len(self.action_stack) < self.nb_samples_to_train:
                self.init_game()
                self.play_game()
                self.nb_games += 1
                
            
            
            batches = self.create_batches()
            
            print("Entrainement sur le dataset")
            loss = 0
            for batch in batches:
                states, rewards, next_states, actions = batch
                loss += self.ai.train_on_batch(states, rewards, next_states, actions)
            print("Loss : {}, proportion d'actions illégales : {}".format(loss/len(batches),self.illegal_count/len(self.action_stack)))

            self.ai.decrease_eps()
            self.ai.update_target()
            
            print("Nombre de parties déjà jouées : {}".format(self.nb_games))
            
            if (training+1)%10 == 0 :
                date = str(datetime.today()).split('.')[0].replace(' ','_')
                cpu_net = deepcopy(self.ai.net).to("cpu")
                save(cpu_net.state_dict(), self.path_to_save+date+"_epoch{}.h5".format(training))
                
        print("Fin de l'entrainement, nombre de parties jouées : {}".format(self.nb_games))

        date = str(datetime.today()).split('.')[0].replace(' ','_')
        cpu_net = deepcopy(self.ai.net).to("cpu")
        save(cpu_net.state_dict(), self.path_to_save+date+".h5")
        
