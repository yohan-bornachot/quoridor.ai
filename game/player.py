import numpy as np

from tools import course_in_width

class Subplayer:
    def __init__(self, i, j, nb_walls, goal) -> None:
        self.i = i
        self.j = j
        self.nb_walls = nb_walls
        self.goal = goal
 
    def possible_right(self, walls: np.ndarray) -> bool:
        board_size = len(walls) + 1
        return (self.j<board_size-1 and 
                (self.i == board_size-1 or walls[self.i, self.j] == 0) and 
                (self.i == 0 or walls[self.i-1,self.j]==0))

    def possible_left(self, walls: np.ndarray) -> bool:
        board_size = len(walls) + 1
        return (self.j>0 and 
                (self.i == board_size-1 or walls[self.i, self.j-1] == 0) and 
                (self.i == 0 or walls[self.i-1,self.j-1]==0))

    def possible_up(self, walls: np.ndarray) -> bool:
        board_size = len(walls) + 1
        return (self.i>0 and 
                (self.j == board_size-1 or walls[self.i-1, self.j] == 0) and 
                (self.j == 0 or walls[self.i-1,self.j-1]==0))

    def possible_down(self, walls: np.ndarray) -> bool:
        board_size = len(walls) + 1
        return (self.i<board_size-1 and
                (self.j == board_size-1 or walls[self.i, self.j] == 0) and
                (self.j == 0 or walls[self.i,self.j-1]==0))



class Player(Subplayer):

    def __init__(self, i, j, nb_walls, goal) -> None:
        super().__init__(i, j, nb_walls, goal)

    def possible_right(self, walls: np.ndarray, opponent: Subplayer) -> bool:
        """This function tests if it is possible to go right"""
        board_size = len(walls) + 1
        return (self.j<board_size-1 and 
                (self.i == board_size-1 or walls[self.i, self.j] == 0) and 
                (self.i == 0 or walls[self.i-1,self.j]==0) and
                (self.i != opponent.i or self.j != opponent.j - 1))

    def possible_left(self, walls: np.ndarray, opponent: Subplayer) -> bool:
        """This function tests if it is possible to go left"""
        board_size = len(walls) + 1
        return (self.j>0 and 
                (self.i == board_size-1 or walls[self.i, self.j-1] == 0) and 
                (self.i == 0 or walls[self.i-1,self.j-1]==0) and
                (self.i != opponent.i or self.j != opponent.j + 1))

    def possible_up(self, walls: np.ndarray,opponent: Subplayer) -> bool:
        """This function tests if it is possible to go upward"""
        board_size = len(walls) + 1
        return (self.i>0 and 
                (self.j == board_size-1 or walls[self.i-1, self.j] == 0) and 
                (self.j == 0 or walls[self.i-1,self.j-1]==0) and
                (self.i != opponent.i-1 or self.j != opponent.j))

    def possible_down(self, walls: np.ndarray, opponent: Subplayer) -> bool:
        """This function tests if it is possible to go downward"""
        board_size = len(walls) + 1
        return (self.i<board_size-1 and
                (self.j == board_size-1 or walls[self.i, self.j] == 0) and
                (self.j == 0 or walls[self.i,self.j-1]==0) and
                (self.i != opponent.i+1 or self.j != opponent.j))
    
    def is_opponent_right(self, walls:np.ndarray, opponent:Subplayer) -> bool:
        """This function returns True if the opponent is just at the right of the current pawn
        and if there is no wall between them."""
        return (self.i==opponent.i and self.j==opponent.j-1 and 
                walls[self.i, self.j]==0 and walls[self.i-1, self.j]==0)
    
    def is_opponent_left(self, walls:np.ndarray, opponent:Subplayer) -> bool:
        """This function returns True if the opponent is just at the left of the current pawn
        and if there is no wall between them."""
        return (self.i==opponent.i and self.j==opponent.j+1 and 
                walls[self.i, self.j-1]==0 and walls[self.i-1, self.j-1]==0)

    def is_opponent_up(self, walls:np.ndarray, opponent:Subplayer) -> bool:
        """This function returns True if the opponent is just above the current pawn
        and if there is no wall between them."""
        return (self.i==opponent.i+1 and self.j==opponent.j and 
                walls[self.i-1, self.j]==0 and walls[self.i-1, self.j-1]==0)
    
    def is_opponent_down(self, walls:np.ndarray, opponent:Subplayer) -> bool:
        """This function returns True if the opponent is just under the current pawn
        and if there is no wall between them."""
        return (self.i==opponent.i-1 and self.j==opponent.j and 
                walls[self.i, self.j]==0 and walls[self.i, self.j-1]==0)
    
    def possible_jump_right(self, walls: np.ndarray, opponent: Subplayer) -> bool:
        """This function tests if it is possible to jump over the opponent pawn towards right"""
        board_size = len(walls) + 1
        return  (self.j+1<board_size-1 and
                self.is_opponent_right(walls, opponent) and opponent.possible_left(walls, self))
    
    def possible_jump_left(self, walls: np.ndarray, opponent: Subplayer) -> bool:
        """This function tests if it is possible to jump over the opponent pawn towards left"""
        return  (self.j-1>0 and
                 self.is_opponent_left(walls, opponent) and opponent.possible_left(walls, self))

    def possible_jump_up(self, walls: np.ndarray, opponent: Subplayer) -> bool:
        """This function tests if it is possible to jump over the opponent pawn upward"""
        return  (self.i-1>0 and
                 self.is_opponent_up(walls, opponent) and opponent.possible_up(walls, self))
    
    def possible_jump_down(self, walls: np.ndarray, opponent: Subplayer) -> bool:
        """This function tests if it is possible to jump over the opponent pawn downward"""
        board_size = len(walls) + 1
        return  (self.i+1<board_size-1 and
                 self.is_opponent_down(walls, opponent) and opponent.possible_down(walls, self))
        
    def possible_jump_diag_ur(self, walls_h: np.ndarray, walls_v:np.ndarray, opponent: Subplayer) -> bool:
        """This function tests if it is possible to jump in diagonal (up-right)."""
        board_size = len(walls_h) + 1
        return ((self.i-1>0 and self.j+1<board_size-1) and
                ((self.is_opponent_up(walls_h, opponent) and opponent.possible_right(walls_v, self)) or
                 (self.is_opponent_right(walls_v, opponent) and opponent.possible_up(walls_h, self))))

    def possible_jump_diag_dr(self, walls_h: np.ndarray, walls_v:np.ndarray, opponent: Subplayer) -> bool:
        """This function tests if it is possible to jump in diagonal (down-right)."""
        board_size = len(walls_h) + 1
        return ((self.i+1>0 and self.j+1<board_size-1) and
                ((self.is_opponent_down(walls_h, opponent) and opponent.possible_right(walls_v, self)) or
                 (self.is_opponent_right(walls_v, opponent) and opponent.possible_down(walls_h, self))))
    
    def possible_jump_diag_ul(self, walls_h: np.ndarray, walls_v:np.ndarray, opponent: Subplayer) -> bool:
        """This function tests if it is possible to jump in diagonal (up-left)."""
        return ((self.i-1>0 and self.j-1>0) and
                ((self.is_opponent_up(walls_h, opponent) and opponent.possible_left(walls_v, self)) or
                 (self.is_opponent_left(walls_v, opponent) and opponent.possible_up(walls_h, self))))
    
    def possible_jump_diag_dl(self, walls_h: np.ndarray, walls_v:np.ndarray, opponent: Subplayer) -> bool:
        """This function tests if it is possible to jump in diagonal (down-left)."""
        board_size = len(walls_h) + 1
        return ((self.i+1<board_size-1 and self.j-1>0) and
                ((self.is_opponent_down(walls_h, opponent) and opponent.possible_left(walls_v, self)) or
                 (self.is_opponent_left(walls_v, opponent) and opponent.possible_down(walls_h, self))))

    def get_position(self):
        return self.i, self.j

    def get_nb_wall(self):
        return self.nb_walls

    def compute_objective(self, walls_h, walls_v):
        return course_in_width(self.i, self.j, walls_h, walls_v, self.goal)

    """
    def set_position(self, i, j):
        self.x = i
        self.y = j

    def move_up(self):
        self.i += 1
    
    def move_down(self):
        self.i -= 1

    def move_right(self):
        self.j += 1

    def move_left(self):
        self.j -= 1

    def use_stick(self):
        self.nb_walls -= 1
    """