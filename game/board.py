import numpy as np

class Board:

    def __init__(self, board_size, wall_size) -> None:
        self.board_size = board_size
        self.walls_h = np.zeros((board_size-1, board_size-1))
        self.walls_v = np.zeros((board_size-1, board_size-1))
        self.wall_size = wall_size

    def possible_h_wall(self, i, j):
        # TODO : utiliser wall_size pour ne pas checker que des murs de taille 2
        return (self.walls_h[i,j] == 0 and (j==0 or self.walls_h[i,j-1]==0) and self.walls_v[i+1,j] == 0)

    def possible_v_wall(self, i, j):
        # TODO : utiliser wall_size pour ne pas checker que des murs de taille 2
        return (self.walls_v[i,j] == 0 and (i==0 or self.walls_v[i-1,j]==0) and self.walls_h[i, j-1] == 0)

    def set_h_wall(self, i, j):
        self.walls_h[i,j] = 1

    def set_v_wall(self, i, j):
        self.walls_v[i,j] = 1
