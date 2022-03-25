from re import S
from .ai import AI
from gamestate import GameState
from quoridor import Quoridor
from copy import deepcopy
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import time

class Node:
    def __init__(self, state: GameState=None, parent: GameState=None, is_root: bool=False):
        self.state = state # store the couple (player, board) 
        self.children = {}
        self.parent = parent
        self.nb_games = 0
        self.nb_wins = 0
        self.is_root = is_root
        self.value = 1000

    def add_child(self, child: GameState, action: int):
        self.children[action] = child
        child.set_parent(self)
        
    def set_parent(self, parent: GameState):
        self.parent = parent
        
    def set_value(self,val):
        self.value = val
        
    def set_state(self, state: GameState):
        self.state = state
        
    def __repr__(self):
        return str(self.value)


class MctsAI(AI):

    def __init__(self, root_state: Node, max_iter: int, time_limit: float, step: int):
        self.root = root_state
        self.current_node = self.root
        self.max_iter = max_iter
        self.time_limit = time_limit
        self.step = step
        self.nb_games = 0
        self.player = 0

    
    def reset(self):
        self.current_node = self.root


    def train(self, nb_rounds=10, verbose=False):

        for n in range(nb_rounds):
            self.current_node = self.root
            if verbose:
                print("round n°{}".format(n))
            final = False

            while not final:
                available_actions = self.current_node.state.next_gamestates()
                known_actions = self.current_node.children.keys()
                unknown_actions = list(set(available_actions) - set(known_actions))

                # known tree area: 
                if unknown_actions == []:
                    if verbose:
                        print('node fully expanded: choose next with UCT')
                    # compute next move according to the MCTS algorithm with UCT
                    action = self.next_move()

                    # Move to next step
                    reward, final = self.next_step(self.current_node.state, action)
                    
                    if self.player == 1:
                        reward *= -1 # their win is my loss
                        self.player = 0
                    else:
                        self.player = 1
                    
                # unknown tree area: need to expand the tree
                else:
                    if verbose:
                        print('node not fully expanded: explore and expand')
                    # find an action that has not been explored
                    action = unknown_actions[0]
                    
                    child = self.expand(self.current_node, action) # play default policy until the end to get a reward
                    self.current_node = child
                    
                    # simulate the end of the game with random plays
                    reward = self.simulate()

                    if self.player == 1:
                        reward = reward * -1 # their win is my loss
                        self.player = 0
                    if verbose:
                        print('node expanded')
                    
                    final = True
                    
            # game is over, reward is collected, now we backpropagate it on the path
                    
            self.backpropagate(self.current_node, reward) # backprop the rewards up in the tree
            if verbose:
                print('reward backpropagated from child')
                self.game.display()

            self.nb_games +=1


    def next_move(self): #, neural_net: DQN):
        """
        returns the next move (integer action) given a board state (Node object)
        """

        values = dict()
        ## implement UCT decision with C_p = 1.
        for action, child in enumerate(self.current_node.next_gamestates()):
            uct = child.nb_wins / child.nb_games + 1. * np.sqrt(2*np.log(self.nb_games)/child.nb_games)
            values[action] = uct
                
            chosen_action = max(values, key=(lambda k: values[k]))

        return chosen_action


    def backpropagate(self, expanded_node, reward):
        """ propagates back the value received by the expanded node following rollout"""
        
        current_node = expanded_node
        while current_node != self.root:
            current_node.nb_games += 1
            current_node.value += reward
            reward = 0 if reward == 1 else 1
            current_node = current_node.parent
        return


    def expand(self, current_node, move):
        """
        move into chosen child state (node created)
        """
        child = Node(parent=current_node)
        child.nb_games = 1 # it is being played
        current_node.add_child(child, move)
        state = current_node.state.next_gamestates()[move]
        child.set_state(list(state))
        return child


    def simulate(self):
        final = False
        while not final:
            reward, final = self.next_step()
        return reward


    def next_step(self, action: int):
        self.current_node = self.current_node.children[action]
        final = self.current_node.state.is_terminal()
        state = self.current_node.state
        if state.players[0].i == state.players[0].goal :
            reward = 1
        elif state.players[1].i == state.players[1].goal :
            reward = -1
        else:
            reward = 0
        return reward, final


    def play(self):
        available_actions = self.game.get_actions(self.game.state)
        known_actions = self.current_node.children.keys()
        unknown_actions = list(set(available_actions) - set(known_actions))

        # known tree area: 
        if unknown_actions == []:
            
            #compute next move according to the MCTS algorithm with UCT
            action = self.next_move()

        # unknown tree area: need to expand the tree
        else:
            # find an action that has not been explored
            action = np.random.choice(unknown_actions)

        return action