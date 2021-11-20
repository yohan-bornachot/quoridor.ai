import numpy as np

class Board:

    def __init__(self, board_size, ) -> None:
        self.walls_h = np.zeros((board_size-1, board_size-1))
        self.walls_v = np.zeros((board_size-1, board_size-1))

    def possible_h_wall(self, i, j):
        return (self.walls_h[i,j] == 0 and (j==0 or self.walls_h[i,j-1]==0) and self.walls_v[i+1,j] == 0)

    def possible_v_wall(self, i, j):
        pass #TODO

    def set_h_wall(self, i, j):
        self.walls_h[i,j] = 1

    def set_v_wall(self, i, j):
        self.walls_v[i,j] = 1
