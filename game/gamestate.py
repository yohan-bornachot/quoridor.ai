import numpy as np

from player import Player
from board import Board

class GameState:

    def __init__(self, players, board, objectives, current_player_idx = 0) -> None:
        self.players = players
        self.nb_players = len(self.players)
        self.board = board
        self.objectives = objectives
        self.current_player_idx = current_player_idx
        self.current_player = players[self.current_player_idx]
        self.opponents = players.copy()
        self.opponents.pop(self.current_player_idx)

        self.possible_moves = {}

    def next_gamestates(self):
        next_steps = list()

        idx_step = 0

    
        if self.current_player.possible_up(self.board.walls_h, self.opponents):
            self.possible_moves["u"] = idx_step
            idx_step += 1
            next_players = [Player(self.current_player.i-1, self.current_player.j, self.current_player.nb_walls, self.current_player.goal_i, self.current_player.goal_j) if k == self.current_player_idx else self.players[k] for k in range(self.nb_players)]
            next_obj = [player.compute_objective(self.board.walls_h, self.board.walls_v) for player in next_players]
            next_steps.append(GameState(next_players , self.board, next_obj, (self.current_player_idx+1)%self.nb_players))

        
        if self.current_player.possible_down(self.board.walls_h, self.opponents):
            self.possible_moves["d"] = idx_step
            idx_step += 1
            next_players = [Player(self.current_player.i+1, self.current_player.j, self.current_player.nb_walls, self.current_player.goal_i, self.current_player.goal_j) if (k == self.current_player_idx) else self.players[k] for k in range(self.nb_players)]
            next_obj = [player.compute_objective(self.board.walls_h, self.board.walls_v) for player in next_players]
            next_steps.append(GameState(next_players , self.board, next_obj, (self.current_player_idx+1)%self.nb_players))


        if self.current_player.possible_left(self.board.walls_v, self.opponents):
            self.possible_moves["l"] = idx_step
            idx_step += 1
            next_players = [Player(self.current_player.i, self.current_player.j-1, self.current_player.nb_walls, self.current_player.goal_i, self.current_player.goal_j) if (k == self.current_player_idx) else self.players[k] for k in range(self.nb_players)]
            next_obj = [player.compute_objective(self.board.walls_h, self.board.walls_v) for player in next_players]
            next_steps.append(GameState(next_players , self.board, next_obj, (self.current_player_idx+1)%self.nb_players))


        if self.current_player.possible_right(self.board.walls_v, self.opponents):
            self.possible_moves["r"] = idx_step
            idx_step += 1
            next_players = [Player(self.current_player.i, self.current_player.j+1, self.current_player.nb_walls, self.current_player.goal_i, self.current_player.goal_j) if (k == self.current_player_idx) else self.players[k] for k in range(self.nb_players)]
            next_obj = [player.compute_objective(self.board.walls_h, self.board.walls_v) for player in next_players]
            next_steps.append(GameState(next_players , self.board, next_obj, (self.current_player_idx+1)%self.nb_players))

        if self.current_player.possible_jump_up(self.board.walls_h, self.opponents):
            self.possible_moves["uu"] = idx_step
            idx_step += 1
            next_players = [Player(self.current_player.i-2, self.current_player.j, self.current_player.nb_walls, self.current_player.goal_i, self.current_player.goal_j) if (k == self.current_player_idx) else self.players[k] for k in range(self.nb_players)]
            next_obj = [player.compute_objective(self.board.walls_h, self.board.walls_v) for player in next_players]
            next_steps.append(GameState(next_players , self.board, next_obj, (self.current_player_idx+1)%self.nb_players))

        if self.current_player.possible_jump_down(self.board.walls_h, self.opponents):
            self.possible_moves["dd"] = idx_step
            idx_step += 1
            next_players = [Player(self.current_player.i+2, self.current_player.j, self.current_player.nb_walls, self.current_player.goal_i, self.current_player.goal_j) if (k == self.current_player_idx) else self.players[k] for k in range(self.nb_players)]
            next_obj = [player.compute_objective(self.board.walls_h, self.board.walls_v) for player in next_players]
            next_steps.append(GameState(next_players , self.board, next_obj, (self.current_player_idx+1)%self.nb_players))

        if self.current_player.possible_jump_right(self.board.walls_v, self.opponents):
            self.possible_moves["rr"] = idx_step
            idx_step += 1
            next_players = [Player(self.current_player.i, self.current_player.j+2, self.current_player.nb_walls, self.current_player.goal_i, self.current_player.goal_j) if (k == self.current_player_idx) else self.players[k] for k in range(self.nb_players)]
            next_obj = [player.compute_objective(self.board.walls_h, self.board.walls_v) for player in next_players]
            next_steps.append(GameState(next_players , self.board, next_obj, (self.current_player_idx+1)%self.nb_players))

        if self.current_player.possible_jump_left(self.board.walls_v, self.opponents):
            self.possible_moves["ll"] = idx_step
            idx_step += 1
            next_players = [Player(self.current_player.i, self.current_player.j-2, self.current_player.nb_walls, self.current_player.goal_i, self.current_player.goal_j) if (k == self.current_player_idx) else self.players[k] for k in range(self.nb_players)]
            next_obj = [player.compute_objective(self.board.walls_h, self.board.walls_v) for player in next_players]
            next_steps.append(GameState(next_players , self.board, next_obj, (self.current_player_idx+1)%self.nb_players))

        if self.current_player.possible_jump_diag_ur(self.board.walls_h, self.board.walls_v, self.opponents):
            self.possible_moves["ur"] = idx_step
            idx_step += 1
            next_players = [Player(self.current_player.i-1, self.current_player.j+1, self.current_player.nb_walls, self.current_player.goal_i, self.current_player.goal_j) if (k == self.current_player_idx) else self.players[k] for k in range(self.nb_players)]
            next_obj = [player.compute_objective(self.board.walls_h, self.board.walls_v) for player in next_players]
            next_steps.append(GameState(next_players , self.board, next_obj, (self.current_player_idx+1)%self.nb_players))

        if self.current_player.possible_jump_diag_ul(self.board.walls_h, self.board.walls_v, self.opponents):
            self.possible_moves["ul"] = idx_step
            idx_step += 1
            next_players = [Player(self.current_player.i-1, self.current_player.j-1, self.current_player.nb_walls, self.current_player.goal_i, self.current_player.goal_j) if (k == self.current_player_idx) else self.players[k] for k in range(self.nb_players)]
            next_obj = [player.compute_objective(self.board.walls_h, self.board.walls_v) for player in next_players]
            next_steps.append(GameState(next_players , self.board, next_obj, (self.current_player_idx+1)%self.nb_players))

        if self.current_player.possible_jump_diag_dr(self.board.walls_h, self.board.walls_v, self.opponents):
            self.possible_moves["dr"] = idx_step
            idx_step += 1
            next_players = [Player(self.current_player.i+1, self.current_player.j+1, self.current_player.nb_walls, self.current_player.goal_i, self.current_player.goal_j) if (k == self.current_player_idx) else self.players[k] for k in range(self.nb_players)]
            next_obj = [player.compute_objective(self.board.walls_h, self.board.walls_v) for player in next_players]
            next_steps.append(GameState(next_players , self.board, next_obj, (self.current_player_idx+1)%self.nb_players))

        if self.current_player.possible_jump_diag_dl(self.board.walls_h, self.board.walls_v, self.opponents):
            self.possible_moves["dl"] = idx_step
            idx_step += 1
            next_players = [Player(self.current_player.i+1, self.current_player.j-1, self.current_player.nb_walls, self.current_player.goal_i, self.current_player.goal_j) if (k == self.current_player_idx) else self.players[k] for k in range(self.nb_players)]
            next_obj = [player.compute_objective(self.board.walls_h, self.board.walls_v) for player in next_players]
            next_steps.append(GameState(next_players , self.board, next_obj, (self.current_player_idx+1)%self.nb_players))

        n = len(self.board.walls_h)
        if self.current_player.get_nb_wall()>0 :
            for k in range(n):
                for l in range(n):
                    if self.board.possible_h_wall(k,l):
                        new_h_walls = np.copy(self.board.walls_h)
                        new_h_walls[k,l] = 1
                        next_board = Board(self.board.board_size, self.board.board_size, new_h_walls, np.copy(self.board.walls_v))
                        next_players = [Player(self.current_player.i, self.current_player.j, self.current_player.nb_walls-1, self.current_player.goal_i, self.current_player.goal_j) if (k == self.current_player_idx) else self.players[k] for k in range(self.nb_players)]
                        next_obj = [player.compute_objective(next_board.walls_h, next_board.walls_v) for player in next_players]
                        if (min(next_obj)>-1) :
                            self.possible_moves["h{}.{}".format(k,l)] = idx_step
                            idx_step += 1
                            next_steps.append(GameState(next_players, next_board, next_obj, (self.current_player_idx+1)%self.nb_players))

                    
                    if self.board.possible_v_wall(k,l):
                        new_v_walls = np.copy(self.board.walls_v)
                        new_v_walls[k,l] = 1
                        next_board = Board(self.board.board_size, self.board.board_size, np.copy(self.board.walls_h), new_v_walls)
                        next_players = [Player(self.current_player.i, self.current_player.j, self.current_player.nb_walls-1, self.current_player.goal_i, self.current_player.goal_j) if (k == self.current_player_idx) else self.players[k] for k in range(self.nb_players)]
                        next_obj = [player.compute_objective(next_board.walls_h, next_board.walls_v) for player in next_players]
                        if (min(next_obj)>-1) :
                            self.possible_moves["v{}.{}".format(k,l)] = idx_step
                            idx_step += 1
                            next_steps.append(GameState(next_players, next_board, next_obj, (self.current_player_idx+1)%self.nb_players))

        return next_steps
    
    def is_terminal(self):
        return (min(self.objectives)==0)

    def get_winner(self):
        k = 0 
        while self.objectives[k]>0 : 
            k+=1
        return k
