import numpy as np

from player import Player
from board import Board

class GameState:

    def __init__(self, player1, player2, board, objective1 , objective2, current_player = 1) -> None:
        self.player1 = player1
        self.player2 = player2
        self.board = board
        self.objective1 = objective1
        self.objective2 = objective2
        self.current_player = current_player

    def next_gamestates(self):
        next_steps = list()
        
        if self.current_player == 1:
            player = self.player1
            other = self.player2
        else : 
            player = self.player2
            other = self.player1

        next_player = ((2 - self.current_player) % 2) + 1

        if player.possible_up(self.board.walls_h, other):
            next_player1 = Player(player.i-1, player.j, player.nb_walls, player.goal)
            next_player2 = Player(other.i, other.j, other.nb_walls, other.goal)
            obj1 = next_player1.compute_objective(self.board.walls_h, self.board.walls_v)
            obj2 = next_player2.compute_objective(self.board.walls_h, self.board.walls_v)
            if self.current_player == 1 :
                next_steps.append(GameState(next_player1, next_player2 , self.board, obj1, obj2, next_player))
            else :
                next_steps.append(GameState(next_player2, next_player1 , self.board, obj2, obj1, next_player))

        if player.possible_down(self.board.walls_h, other):
            next_player1 = Player(player.i+1, player.j, player.nb_walls, player.goal)
            next_player2 = Player(other.i, other.j, other.nb_walls, other.goal)
            obj1 = next_player1.compute_objective(self.board.walls_h, self.board.walls_v)
            obj2 = next_player2.compute_objective(self.board.walls_h, self.board.walls_v)
            if self.current_player == 1 :
                next_steps.append(GameState(next_player1, next_player2 , self.board, obj1, obj2, next_player))
            else :
                next_steps.append(GameState(next_player2, next_player1 , self.board, obj2, obj1, next_player))

        if player.possible_left(self.board.walls_v, other):
            next_player1 = Player(player.i, player.j-1, player.nb_walls, player.goal)
            next_player2 = Player(other.i, other.j, other.nb_walls, other.goal)
            obj1 = next_player1.compute_objective(self.board.walls_h, self.board.walls_v)
            obj2 = next_player2.compute_objective(self.board.walls_h, self.board.walls_v)
            if self.current_player == 1 :
                next_steps.append(GameState(next_player1, next_player2 , self.board, obj1, obj2, next_player))
            else :
                next_steps.append(GameState(next_player2, next_player1 , self.board, obj2, obj1, next_player))

        if player.possible_right(self.board.walls_v, other):
            next_player1 = Player(player.i, player.j+1, player.nb_walls, player.goal)
            next_player2 = Player(other.i, other.j, other.nb_walls, other.goal)
            obj1 = next_player1.compute_objective(self.board.walls_h, self.board.walls_v)
            obj2 = next_player2.compute_objective(self.board.walls_h, self.board.walls_v)
            if self.current_player == 1 :
                next_steps.append(GameState(next_player1, next_player2 , self.board, obj1, obj2, next_player))
            else :
                next_steps.append(GameState(next_player2, next_player1 , self.board, obj2, obj1, next_player))

        if player.possible_jump_up(self.board.walls_h, other):
            next_player1 = Player(player.i-2, player.j, player.nb_walls, player.goal)
            next_player2 = Player(other.i, other.j, other.nb_walls, other.goal)
            obj1 = next_player1.compute_objective(self.board.walls_h, self.board.walls_v)
            obj2 = next_player2.compute_objective(self.board.walls_h, self.board.walls_v)
            if self.current_player == 1 :
                next_steps.append(GameState(next_player1, next_player2 , self.board, obj1, obj2, next_player))
            else :
                next_steps.append(GameState(next_player2, next_player1 , self.board, obj2, obj1, next_player))
            
        if player.possible_jump_down(self.board.walls_h, other):
            next_player1 = Player(player.i+2, player.j, player.nb_walls, player.goal)
            next_player2 = Player(other.i, other.j, other.nb_walls, other.goal)
            obj1 = next_player1.compute_objective(self.board.walls_h, self.board.walls_v)
            obj2 = next_player2.compute_objective(self.board.walls_h, self.board.walls_v)
            if self.current_player == 1 :
                next_steps.append(GameState(next_player1, next_player2 , self.board, obj1, obj2, next_player))
            else :
                next_steps.append(GameState(next_player2, next_player1 , self.board, obj2, obj1, next_player))

        if player.possible_jump_left(self.board.walls_v, other):
            next_player1 = Player(player.i, player.j-2, player.nb_walls, player.goal)
            next_player2 = Player(other.i, other.j, other.nb_walls, other.goal)
            obj1 = next_player1.compute_objective(self.board.walls_h, self.board.walls_v)
            obj2 = next_player2.compute_objective(self.board.walls_h, self.board.walls_v)
            if self.current_player == 1 :
                next_steps.append(GameState(next_player1, next_player2 , self.board, obj1, obj2, next_player))
            else :
                next_steps.append(GameState(next_player2, next_player1 , self.board, obj2, obj1, next_player))

        if player.possible_jump_right(self.board.walls_v, other):
            next_player1 = Player(player.i, player.j+2, player.nb_walls, player.goal)
            next_player2 = Player(other.i, other.j, other.nb_walls, other.goal)
            obj1 = next_player1.compute_objective(self.board.walls_h, self.board.walls_v)
            obj2 = next_player2.compute_objective(self.board.walls_h, self.board.walls_v)
            if self.current_player == 1 :
                next_steps.append(GameState(next_player1, next_player2 , self.board, obj1, obj2, next_player))
            else :
                next_steps.append(GameState(next_player2, next_player1 , self.board, obj2, obj1, next_player))

        if player.possible_jump_diag_ur(self.board.walls_h, self.board.walls_v, other):
            next_player1 = Player(player.i-1, player.j+1, player.nb_walls, player.goal)
            next_player2 = Player(other.i, other.j, other.nb_walls, other.goal)
            obj1 = next_player1.compute_objective(self.board.walls_h, self.board.walls_v)
            obj2 = next_player2.compute_objective(self.board.walls_h, self.board.walls_v)
            if self.current_player == 1 :
                next_steps.append(GameState(next_player1, next_player2 , self.board, obj1, obj2, next_player))
            else :
                next_steps.append(GameState(next_player2, next_player1 , self.board, obj2, obj1, next_player))

        if player.possible_jump_diag_ul(self.board.walls_h, self.board.walls_v, other):
            next_player1 = Player(player.i-1, player.j-1, player.nb_walls, player.goal)
            next_player2 = Player(other.i, other.j, other.nb_walls, other.goal)
            obj1 = next_player1.compute_objective(self.board.walls_h, self.board.walls_v)
            obj2 = next_player2.compute_objective(self.board.walls_h, self.board.walls_v)
            if self.current_player == 1 :
                next_steps.append(GameState(next_player1, next_player2 , self.board, obj1, obj2, next_player))
            else :
                next_steps.append(GameState(next_player2, next_player1 , self.board, obj2, obj1, next_player))

        if player.possible_jump_diag_dr(self.board.walls_h, self.board.walls_v, other):
            next_player1 = Player(player.i+1, player.j+1, player.nb_walls, player.goal)
            next_player2 = Player(other.i, other.j, other.nb_walls, other.goal)
            obj1 = next_player1.compute_objective(self.board.walls_h, self.board.walls_v)
            obj2 = next_player2.compute_objective(self.board.walls_h, self.board.walls_v)
            if self.current_player == 1 :
                next_steps.append(GameState(next_player1, next_player2 , self.board, obj1, obj2, next_player))
            else :
                next_steps.append(GameState(next_player2, next_player1 , self.board, obj2, obj1, next_player))

        if player.possible_jump_diag_dl(self.board.walls_h, self.board.walls_v, other):
            next_player1 = Player(player.i+1, player.j-1, player.nb_walls, player.goal)
            next_player2 = Player(other.i, other.j, other.nb_walls, other.goal)
            obj1 = next_player1.compute_objective(self.board.walls_h, self.board.walls_v)
            obj2 = next_player2.compute_objective(self.board.walls_h, self.board.walls_v)
            if self.current_player == 1 :
                next_steps.append(GameState(next_player1, next_player2 , self.board, obj1, obj2, next_player))
            else :
                next_steps.append(GameState(next_player2, next_player1 , self.board, obj2, obj1, next_player))


        n = len(self.board.walls_h)
        if player.get_nb_wall()>0 :
            for k in range(n):
                for l in range(n):
                    if self.board.possible_h_wall(k,l):
                        new_h_walls = np.copy(self.board.walls_h)
                        new_h_walls[k,l] = 1
                        next_board = Board(self.board.board_size, self.board.board_size, new_h_walls, np.copy(self.board.walls_v))
                        next_player1 = Player(player.i, player.j, player.nb_walls - 1, player.goal)
                        next_player2 = Player(other.i, other.j, other.nb_walls, other.goal)
                        obj1 = next_player1.compute_objective(next_board.walls_h, next_board.walls_v)
                        obj2 = next_player2.compute_objective(next_board.walls_h, next_board.walls_v)
                        if (obj1>-1 and obj2>-1) :
                            if self.current_player == 1 :
                                next_steps.append(GameState(next_player1, next_player2 , next_board, obj1, obj2, next_player))
                            else :
                                next_steps.append(GameState(next_player2, next_player1 , next_board, obj2, obj1, next_player))

                    if self.board.possible_v_wall(k,l):
                        new_v_walls = np.copy(self.board.walls_v)
                        new_v_walls[k,l] = 1
                        next_board = Board(self.board.board_size, self.board.board_size, np.copy(self.board.walls_h), new_v_walls)
                        next_player1 = Player(player.i, player.j, player.nb_walls - 1, player.goal)
                        next_player2 = Player(other.i, other.j, other.nb_walls, other.goal)
                        obj1 = next_player1.compute_objective(next_board.walls_h, next_board.walls_v)
                        obj2 = next_player2.compute_objective(next_board.walls_h, next_board.walls_v)
                        if (obj1>-1 and obj2>-1) : 
                            if self.current_player == 1 :
                                next_steps.append(GameState(next_player1, next_player2 , next_board, obj1, obj2, next_player))
                            else :
                                next_steps.append(GameState(next_player2, next_player1 , next_board, obj2, obj1, next_player))
        
        return next_steps
    
    def is_terminal(self):
        return (self.objective1==0 or self.objective2==0)
