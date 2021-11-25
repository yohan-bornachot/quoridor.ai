import numpy as np

from player import Player
from board import Board

class GameState:

    def __init__(self, players, board, objectives, current_player = 0) -> None:
        self.players = players
        self.nb_players = len(self.players)
        self.board = board
        self.objectives = objectives
        self.current_player = current_player

        self.possible_moves = list()

    def next_gamestates(self):
        next_steps = list()

        p = self.current_player
        q = (self.current_player + 1)%self.nb_players
        print(q)
        

        if self.players[p].possible_up(self.board.walls_h, self.players[q]):
            self.possible_moves.append("u")
            next_players = [Player(self.players[p].i-1, self.players[p].j, self.players[p].nb_walls, self.players[p].goal),
                            Player(self.players[q].i, self.players[q].j, self.players[q].nb_walls, self.players[q].goal)]
            if p != 0 :
                next_players = next_players.reverse()
            next_obj = [player.compute_objective(self.board.walls_h, self.board.walls_v) for player in next_players]
            next_steps.append(GameState(next_players , self.board, next_obj, q))

        
        if self.players[p].possible_down(self.board.walls_h, self.players[q]):
            self.possible_moves.append("d")
            next_players = [Player(self.players[p].i+1, self.players[p].j, self.players[p].nb_walls, self.players[p].goal),
                            Player(self.players[q].i, self.players[q].j, self.players[q].nb_walls, self.players[q].goal)]
            if p != 0 :
                next_players = next_players.reverse()
            next_obj = [player.compute_objective(self.board.walls_h, self.board.walls_v) for player in next_players]
            next_steps.append(GameState(next_players , self.board, next_obj, q))


        if self.players[p].possible_left(self.board.walls_v, self.players[q]):
            self.possible_moves.append("l")
            next_players = [Player(self.players[p].i, self.players[p].j-1, self.players[p].nb_walls, self.players[p].goal),
                            Player(self.players[q].i, self.players[q].j, self.players[q].nb_walls, self.players[q].goal)]
            if p != 0 :
                next_players = next_players.reverse()
            next_obj = [player.compute_objective(self.board.walls_h, self.board.walls_v) for player in next_players]
            next_steps.append(GameState(next_players , self.board, next_obj, q))


        if self.players[p].possible_right(self.board.walls_v, self.players[q]):
            self.possible_moves.append("r")
            next_players = [Player(self.players[p].i, self.players[p].j+1, self.players[p].nb_walls, self.players[p].goal),
                            Player(self.players[q].i, self.players[q].j, self.players[q].nb_walls, self.players[q].goal)]
            if p != 0 :
                next_players = next_players.reverse()
            next_obj = [player.compute_objective(self.board.walls_h, self.board.walls_v) for player in next_players]
            next_steps.append(GameState(next_players , self.board, next_obj, q))

        if self.players[p].possible_jump_up(self.board.walls_h, self.players[q]):
            self.possible_moves.append("uu")
            next_players = [Player(self.players[p].i-2, self.players[p].j, self.players[p].nb_walls, self.players[p].goal),
                            Player(self.players[q].i, self.players[q].j, self.players[q].nb_walls, self.players[q].goal)]
            if p != 0 :
                next_players = next_players.reverse()
            next_obj = [player.compute_objective(self.board.walls_h, self.board.walls_v) for player in next_players]
            next_steps.append(GameState(next_players , self.board, next_obj, q))

        if self.players[p].possible_jump_down(self.board.walls_h, self.players[q]):
            self.possible_moves.append("dd")
            next_players = [Player(self.players[p].i+2, self.players[p].j, self.players[p].nb_walls, self.players[p].goal),
                            Player(self.players[q].i, self.players[q].j, self.players[q].nb_walls, self.players[q].goal)]
            if p != 0 :
                next_players = next_players.reverse()
            next_obj = [player.compute_objective(self.board.walls_h, self.board.walls_v) for player in next_players]
            next_steps.append(GameState(next_players , self.board, next_obj, q))

        if self.players[p].possible_jump_right(self.board.walls_v, self.players[q]):
            self.possible_moves.append("rr")
            next_players = [Player(self.players[p].i, self.players[p].j+2, self.players[p].nb_walls, self.players[p].goal),
                            Player(self.players[q].i, self.players[q].j, self.players[q].nb_walls, self.players[q].goal)]
            if p != 0 :
                next_players = next_players.reverse()
            next_obj = [player.compute_objective(self.board.walls_h, self.board.walls_v) for player in next_players]
            next_steps.append(GameState(next_players , self.board, next_obj, q))

        if self.players[p].possible_jump_left(self.board.walls_v, self.players[q]):
            self.possible_moves.append("ll")
            next_players = [Player(self.players[p].i, self.players[p].j-2, self.players[p].nb_walls, self.players[p].goal),
                            Player(self.players[q].i, self.players[q].j, self.players[q].nb_walls, self.players[q].goal)]
            if p != 0 :
                next_players = next_players.reverse()
            next_obj = [player.compute_objective(self.board.walls_h, self.board.walls_v) for player in next_players]
            next_steps.append(GameState(next_players , self.board, next_obj, q))

        if self.players[p].possible_jump_diag_ur(self.board.walls_h, self.board.walls_v, self.players[q]):
            self.possible_moves.append("ur")
            next_players = [Player(self.players[p].i-1, self.players[p].j+1, self.players[p].nb_walls, self.players[p].goal),
                            Player(self.players[q].i, self.players[q].j, self.players[q].nb_walls, self.players[q].goal)]
            if p != 0 :
                next_players = next_players.reverse()
            next_obj = [player.compute_objective(self.board.walls_h, self.board.walls_v) for player in next_players]
            next_steps.append(GameState(next_players , self.board, next_obj, q))

        if self.players[p].possible_jump_diag_ul(self.board.walls_h, self.board.walls_v, self.players[q]):
            self.possible_moves.append("ul")
            next_players = [Player(self.players[p].i-1, self.players[p].j-1, self.players[p].nb_walls, self.players[p].goal),
                            Player(self.players[q].i, self.players[q].j, self.players[q].nb_walls, self.players[q].goal)]
            if p != 0 :
                next_players = next_players.reverse()
            next_obj = [player.compute_objective(self.board.walls_h, self.board.walls_v) for player in next_players]
            next_steps.append(GameState(next_players , self.board, next_obj, q))

        if self.players[p].possible_jump_diag_dr(self.board.walls_h, self.board.walls_v, self.players[q]):
            self.possible_moves.append("dr")
            next_players = [Player(self.players[p].i+1, self.players[p].j+1, self.players[p].nb_walls, self.players[p].goal),
                            Player(self.players[q].i, self.players[q].j, self.players[q].nb_walls, self.players[q].goal)]
            if p != 0 :
                next_players = next_players.reverse()
            next_obj = [player.compute_objective(self.board.walls_h, self.board.walls_v) for player in next_players]
            next_steps.append(GameState(next_players , self.board, next_obj, q))

        if self.players[p].possible_jump_diag_dl(self.board.walls_h, self.board.walls_v, self.players[q]):
            self.possible_moves.append("dl")
            next_players = [Player(self.players[p].i+1, self.players[p].j-1, self.players[p].nb_walls, self.players[p].goal),
                            Player(self.players[q].i, self.players[q].j, self.players[q].nb_walls, self.players[q].goal)]
            if p != 0 :
                next_players = next_players.reverse()
            next_obj = [player.compute_objective(self.board.walls_h, self.board.walls_v) for player in next_players]
            next_steps.append(GameState(next_players , self.board, next_obj, q))

        n = len(self.board.walls_h)
        if self.players[p].get_nb_wall()>0 :
            for k in range(n):
                for l in range(n):
                    if self.board.possible_h_wall(k,l):
                        new_h_walls = np.copy(self.board.walls_h)
                        new_h_walls[k,l] = 1
                        next_board = Board(self.board.board_size, self.board.board_size, new_h_walls, np.copy(self.board.walls_v))
                        next_players = [Player(self.players[p].i, self.players[p].j, self.players[p].nb_walls - 1, self.players[p].goal),
                                         Player(self.players[q].i, self.players[q].j, self.players[q].nb_walls, self.players[q].goal)]
                        if p != 0 :
                            next_players = next_players.reverse()
                        next_obj = [player.compute_objective(self.board.walls_h, self.board.walls_v) for player in next_players]
                        if (next_obj[0]>-1 and next_obj[1]>-1) :
                            self.possible_moves.append("h{}{}".format(k,l))
                            next_steps.append(GameState(next_players, next_board, next_obj, q))

                    
                    if self.board.possible_v_wall(k,l):
                        new_v_walls = np.copy(self.board.walls_v)
                        new_v_walls[k,l] = 1
                        next_board = Board(self.board.board_size, self.board.board_size, np.copy(self.board.walls_h), new_v_walls)
                        next_players = [Player(self.players[p].i, self.players[p].j, self.players[p].nb_walls - 1, self.players[p].goal),
                                         Player(self.players[q].i, self.players[q].j, self.players[q].nb_walls, self.players[q].goal)]
                        if p != 0 :
                            next_players = next_players.reverse()
                        next_obj = [player.compute_objective(self.board.walls_h, self.board.walls_v) for player in next_players]
                        if (next_obj[0]>-1 and next_obj[1]>-1) :
                            self.possible_moves.append("v{}{}".format(k,l))
                            next_steps.append(GameState(next_players, next_board, next_obj, q))

        

        return next_steps
    
    def is_terminal(self):
        return (self.objectives[0]==0 or self.objectives[1]==0)
