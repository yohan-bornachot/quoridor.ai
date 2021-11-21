from player import Player
from board import Board

class GameState:

    def __init__(self, player1, player2, board, current_player = 1) -> None:
        self.player1 = player1
        self.player2 = player2
        self.board = board
        self.current_player = current_player

    def next_gamestates(self):
        # TODO : finir cette fonction de l'enfer
        next_steps = list()
        
        if self.current_player == 1:
            player = self.player1
            other = self.player2
        else : 
            player = self.player2
            other = self.player1

        next_player = ((2 - self.current_player) % 2) + 1

        if player.possible_up(self.board.walls_h, other):
            if self.current_player == 1 :
                next_player1 = Player(player.i-1, player.j, player.nb_walls, player.goal)
                next_player2 = Player(other.i, other.j, other.nb_walls, other.goal)
            else :
                next_player1 = Player(player.i, player.j, player.nb_walls, player.goal)
                next_player2 = Player(other.i-1, other.j, other.nb_walls, other.goal)
            next_steps.append(GameState(next_player1, next_player2 , self.board, next_player))

        if player.possible_down(self.board.walls_h, other):
            if self.current_player == 1 :
                next_player1 = Player(player.i+1, player.j, player.nb_walls, player.goal)
                next_player2 = Player(other.i, other.j, other.nb_walls, other.goal)
            else :
                next_player1 = Player(player.i, player.j, player.nb_walls, player.goal)
                next_player2 = Player(other.i+1, other.j, other.nb_walls, other.goal)
            next_steps.append(GameState(next_player1, next_player2 , self.board, next_player))

        if player.possible_left(self.board.walls_v, other):
            if self.current_player == 1 :
                next_player1 = Player(player.i, player.j-1, player.nb_walls, player.goal)
                next_player2 = Player(other.i, other.j, other.nb_walls, other.goal)
            else :
                next_player1 = Player(player.i, player.j, player.nb_walls, player.goal)
                next_player2 = Player(other.i, other.j-1, other.nb_walls, other.goal)
            next_steps.append(GameState(next_player1, next_player2 , self.board, next_player))

        if player.possible_right(self.board.walls_v, other):
            if self.current_player == 1 :
                next_player1 = Player(player.i, player.j+1, player.nb_walls, player.goal)
                next_player2 = Player(other.i, other.j, other.nb_walls, other.goal)
            else :
                next_player1 = Player(player.i, player.j, player.nb_walls, player.goal)
                next_player2 = Player(other.i, other.j+1, other.nb_walls, other.goal)
            next_steps.append(GameState(next_player1, next_player2 , self.board, next_player))

        if player.possible_jump_up(self.board.walls_h, other):
            if self.current_player == 1 :
                next_player1 = Player(player.i-2, player.j, player.nb_walls, player.goal)
                next_player2 = Player(other.i, other.j, other.nb_walls, other.goal)
            else :
                next_player1 = Player(player.i, player.j, player.nb_walls, player.goal)
                next_player2 = Player(other.i-2, other.j, other.nb_walls, other.goal)
            next_steps.append(GameState(next_player1, next_player2 , self.board, next_player))

        if player.possible_jump_down(self.board.walls_h, other):
            if self.current_player == 1 :
                next_player1 = Player(player.i+2, player.j, player.nb_walls, player.goal)
                next_player2 = Player(other.i, other.j, other.nb_walls, other.goal)
            else :
                next_player1 = Player(player.i, player.j, player.nb_walls, player.goal)
                next_player2 = Player(other.i+2, other.j, other.nb_walls, other.goal)
            next_steps.append(GameState(next_player1, next_player2 , self.board, next_player))

        if player.possible_jump_left(self.board.walls_v, other):
            if self.current_player == 1 :
                next_player1 = Player(player.i, player.j-2, player.nb_walls, player.goal)
                next_player2 = Player(other.i, other.j, other.nb_walls, other.goal)
            else :
                next_player1 = Player(player.i, player.j, player.nb_walls, player.goal)
                next_player2 = Player(other.i, other.j-2, other.nb_walls, other.goal)
            next_steps.append(GameState(next_player1, next_player2 , self.board, next_player))

        if player.possible_jump_right(self.board.walls_v, other):
            if self.current_player == 1 :
                next_player1 = Player(player.i, player.j+2, player.nb_walls, player.goal)
                next_player2 = Player(other.i, other.j, other.nb_walls, other.goal)
            else :
                next_player1 = Player(player.i, player.j, player.nb_walls, player.goal)
                next_player2 = Player(other.i, other.j+2, other.nb_walls, other.goal)
            next_steps.append(GameState(next_player1, next_player2 , self.board, next_player))

        if player.possible_jump_diag_ur(self.board.walls_h, self.board.walls_v, other):
            if self.current_player == 1 :
                next_player1 = Player(player.i-1, player.j+1, player.nb_walls, player.goal)
                next_player2 = Player(other.i, other.j, other.nb_walls, other.goal)
            else :
                next_player1 = Player(player.i, player.j, player.nb_walls, player.goal)
                next_player2 = Player(other.i-1, other.j+1, other.nb_walls, other.goal)
            next_steps.append(GameState(next_player1, next_player2 , self.board, next_player))
        
        if player.possible_jump_diag_ul(self.board.walls_h, self.board.walls_v, other):
            if self.current_player == 1 :
                next_player1 = Player(player.i-1, player.j-1, player.nb_walls, player.goal)
                next_player2 = Player(other.i, other.j, other.nb_walls, other.goal)
            else :
                next_player1 = Player(player.i, player.j, player.nb_walls, player.goal)
                next_player2 = Player(other.i-1, other.j-1, other.nb_walls, other.goal)
            next_steps.append(GameState(next_player1, next_player2 , self.board, next_player))

        if player.possible_jump_diag_dr(self.board.walls_h, self.board.walls_v, other):
            if self.current_player == 1 :
                next_player1 = Player(player.i+1, player.j+1, player.nb_walls, player.goal)
                next_player2 = Player(other.i, other.j, other.nb_walls, other.goal)
            else :
                next_player1 = Player(player.i, player.j, player.nb_walls, player.goal)
                next_player2 = Player(other.i+1, other.j+1, other.nb_walls, other.goal)
            next_steps.append(GameState(next_player1, next_player2 , self.board, next_player))

        if player.possible_jump_diag_dl(self.board.walls_h, self.board.walls_v, other):
            if self.current_player == 1 :
                next_player1 = Player(player.i+1, player.j-1, player.nb_walls, player.goal)
                next_player2 = Player(other.i, other.j, other.nb_walls, other.goal)
            else :
                next_player1 = Player(player.i, player.j, player.nb_walls, player.goal)
                next_player2 = Player(other.i+1, other.j-1, other.nb_walls, other.goal)
            next_steps.append(GameState(next_player1, next_player2 , self.board, next_player))

        n = len(self.board.walls_h)
        for k in range(len(n)):
            for l in range(len(n)):
                if self.board.possible_h_wall(k,l):
                    pass