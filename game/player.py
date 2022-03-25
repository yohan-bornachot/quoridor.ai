import numpy as np
from typing import List, Tuple

from tools import course_in_width

class BasicPlayer:
    def __init__(self, i, j, nb_walls, goal_i, goal_j) -> None:
        self.i = i
        self.j = j
        self.nb_walls = nb_walls
        self.goal_i = goal_i
        self.goal_j = goal_j
 

class SubPlayer(BasicPlayer):

    def __init__(self, i, j, nb_walls, goal_i, goal_j) -> None:
        super().__init__(i, j, nb_walls, goal_i, goal_j)

    def possible_right(self, walls: np.ndarray, opponents: List[BasicPlayer]) -> bool:
        """This function tests if it is possible to go right"""
        board_size = len(walls) + 1
        k = 0
        while k<len(opponents) and (self.i != opponents[k].i or self.j + 1 != opponents[k].j):
            k+=1
        return (self.j<board_size-1 and 
                (self.i == board_size-1 or walls[self.i, self.j] == 0) and 
                (self.i == 0 or walls[self.i-1,self.j]==0) and
                k==len(opponents))

    def possible_left(self, walls: np.ndarray, opponents: List[BasicPlayer]) -> bool:
        """This function tests if it is possible to go left"""
        board_size = len(walls) + 1
        k = 0
        while k<len(opponents) and (self.i != opponents[k].i or self.j - 1 != opponents[k].j):
            k+=1
        return (self.j>0 and 
                (self.i == board_size-1 or walls[self.i, self.j-1] == 0) and 
                (self.i == 0 or walls[self.i-1,self.j-1]==0) and
                (k==len(opponents)))

    def possible_up(self, walls: np.ndarray, opponents: List[BasicPlayer]) -> bool:
        """This function tests if it is possible to go upward"""
        board_size = len(walls) + 1
        k = 0
        while k<len(opponents) and (self.i - 1 != opponents[k].i or self.j != opponents[k].j):
            k+=1
        return (self.i>0 and 
                (self.j == board_size-1 or walls[self.i-1, self.j] == 0) and 
                (self.j == 0 or walls[self.i-1,self.j-1]==0) and
                k==len(opponents))

    def possible_down(self, walls: np.ndarray, opponents: List[BasicPlayer]) -> bool:
        """This function tests if it is possible to go downward"""
        board_size = len(walls) + 1
        k = 0
        while k<len(opponents) and (self.i + 1 != opponents[k].i or self.j != opponents[k].j):
            k+=1
        return (self.i<board_size-1 and
                (self.j == board_size-1 or walls[self.i, self.j] == 0) and
                (self.j == 0 or walls[self.i,self.j-1]==0) and
                k==len(opponents))
    
    def is_opponent_right(self, walls:np.ndarray, opponents:List[BasicPlayer]) -> Tuple[bool, int]:
        """This function returns True if the opponent is just at the right of the current pawn
        and if there is no wall between them."""
        board_size = len(walls) + 1
        k = 0
        while k<len(opponents) and (self.i!=opponents[k].i or self.j!=opponents[k].j-1):
            k+=1
        return (k<len(opponents) and 
                (self.i == board_size-1 or walls[self.i, self.j]==0) and walls[self.i-1, self.j]==0), k
    
    def is_opponent_left(self, walls:np.ndarray, opponents:List[BasicPlayer]) -> Tuple[bool, int]:
        """This function returns True if the opponent is just at the left of the current pawn
        and if there is no wall between them."""
        board_size = len(walls) + 1
        k = 0
        while k<len(opponents) and (self.i!=opponents[k].i or self.j!=opponents[k].j+1):
            k+=1
        return (k<len(opponents) and 
                (self.i == board_size-1 or walls[self.i, self.j-1]==0) and walls[self.i-1, self.j-1]==0), k

    def is_opponent_up(self, walls:np.ndarray, opponents:List[BasicPlayer]) -> Tuple[bool, int]:
        """This function returns True if the opponent is just above the current pawn
        and if there is no wall between them."""
        board_size = len(walls) + 1
        k = 0
        while k<len(opponents) and (self.i!=opponents[k].i+1 or self.j!=opponents[k].j):
            k+=1
        return (k<len(opponents) and 
                (self.j == board_size-1 or  walls[self.i-1, self.j]==0) and walls[self.i-1, self.j-1]==0), k
    
    def is_opponent_down(self, walls:np.ndarray, opponents:List[BasicPlayer]) -> Tuple[bool, int]:
        """This function returns True if the opponent is just under the current pawn
        and if there is no wall between them."""
        board_size = len(walls) + 1
        k = 0
        while k<len(opponents) and (self.i!=opponents[k].i-1 or self.j!=opponents[k].j):
            k+=1
        return (k<len(opponents) and 
                (self.j == board_size-1 or walls[self.i, self.j]==0) and walls[self.i, self.j-1]==0), k


class Player(SubPlayer):

    def __init__(self, i, j, nb_walls, goal_i, goal_j) -> None:
        super().__init__(i, j, nb_walls, goal_i, goal_j)
    
    def possible_jump_right(self, walls: np.ndarray, opponents: List[SubPlayer]) -> bool:
        """This function tests if it is possible to jump over the opponent pawn towards right"""
        board_size = len(walls) + 1
        copy_opponents = opponents.copy()
        if self.j+1<board_size :
            test, k = self.is_opponent_right(walls, opponents)
            if test :
                copy_opponents.pop(k)
                copy_opponents.append(self) 
                if opponents[k].possible_right(walls, copy_opponents) : return True
        return False
    
    def possible_jump_left(self, walls: np.ndarray, opponents: List[SubPlayer]) -> bool:
        """This function tests if it is possible to jump over the opponent pawn towards left"""
        copy_opponents = opponents.copy()
        if self.j-1>0 :
            test, k = self.is_opponent_left(walls, opponents)
            if test :
                copy_opponents.pop(k)
                copy_opponents.append(self)
                if opponents[k].possible_left(walls, copy_opponents) : 
                    return True
        return False

    def possible_jump_up(self, walls: np.ndarray, opponents: List[SubPlayer]) -> bool:
        """This function tests if it is possible to jump over the opponent pawn upward"""
        copy_opponents = opponents.copy()
        if self.i-1>0 : 
            test, k = self.is_opponent_up(walls, opponents)
            if test :
                copy_opponents.pop(k)
                copy_opponents.append(self)
                if opponents[k].possible_up(walls, copy_opponents):
                    return True
        return False
    
    def possible_jump_down(self, walls: np.ndarray, opponents: List[SubPlayer]) -> bool:
        """This function tests if it is possible to jump over the opponent pawn downward"""
        board_size = len(walls) + 1
        copy_opponents = opponents.copy()
        if self.i+1<board_size : 
            test, k = self.is_opponent_down(walls, opponents)
            if test :
                copy_opponents.pop(k)
                copy_opponents.append(self)
                if opponents[k].possible_down(walls, copy_opponents):
                    return True
        return False
        
    def possible_jump_diag_ur(self, walls_h: np.ndarray, walls_v:np.ndarray, opponents: List[SubPlayer]) -> bool:
        """This function tests if it is possible to jump in diagonal (up-right)."""
        board_size = len(walls_h) + 1
        if self.i-1>0 and self.j+1<board_size-1 :
            test, k = self.is_opponent_up(walls_h, opponents)
            copy_opponents = opponents.copy()
            if test :
                copy_opponents.pop(k)
                copy_opponents.append(self)
                if opponents[k].possible_right(walls_v,copy_opponents):
                    return True
            test, k = self.is_opponent_right(walls_v,opponents)
            copy_opponents = opponents.copy()
            if test :
                copy_opponents.pop(k)
                copy_opponents.append(self)
                if opponents[k].possible_up(walls_h, copy_opponents): 
                    return True
        return False


    def possible_jump_diag_dr(self, walls_h: np.ndarray, walls_v:np.ndarray, opponents: List[SubPlayer]) -> bool:
        """This function tests if it is possible to jump in diagonal (down-right)."""
        board_size = len(walls_h) + 1

        if self.i+1>0 and self.j+1<board_size-1 :
            test, k = self.is_opponent_down(walls_h, opponents)
            if test :
                copy_opponents = opponents.copy()
                copy_opponents.pop(k)
                copy_opponents.append(self)
                if opponents[k].possible_right(walls_v,copy_opponents):
                    return True
            test, k = self.is_opponent_right(walls_v, opponents)
            if test :
                copy_opponents = opponents.copy()
                copy_opponents.pop(k)
                copy_opponents.append(self)
                if  opponents[k].possible_down(walls_h,copy_opponents):
                    return True
        return False

    
    def possible_jump_diag_ul(self, walls_h: np.ndarray, walls_v:np.ndarray, opponents: List[SubPlayer]) -> bool:
        """This function tests if it is possible to jump in diagonal (up-left)."""
        if (self.i-1>0 and self.j-1>0) :
            test, k = self.is_opponent_up(walls_h, opponents)
            if test :
                copy_opponents = opponents.copy()
                copy_opponents.pop(k)
                copy_opponents.append(self)
                if opponents[k].possible_left(walls_v, copy_opponents) :
                    return True
            test, k = self.is_opponent_left(walls_v, opponents)
            if test :
                copy_opponents = opponents.copy()
                copy_opponents.pop(k)
                copy_opponents.append(self)
                if opponents[k].possible_up(walls_h,  copy_opponents) :
                    return True 
        return False
    
    def possible_jump_diag_dl(self, walls_h: np.ndarray, walls_v:np.ndarray, opponents: List[SubPlayer]) -> bool:
        """This function tests if it is possible to jump in diagonal (down-left)."""
        board_size = len(walls_h) + 1
        if (self.i+1<board_size-1 and self.j-1>0) :
            test, k = self.is_opponent_down(walls_h, opponents)
            if test :
                copy_opponents = opponents.copy()
                copy_opponents.pop(k)
                copy_opponents.append(self)
                if opponents[k].possible_left(walls_v, copy_opponents):
                    return True
            test, k = self.is_opponent_left(walls_v, opponents)
            if test :
                copy_opponents = opponents.copy()
                copy_opponents.pop(k)
                copy_opponents.append(self)
                if opponents[k].possible_down(walls_h, copy_opponents):
                    return True
        return False

    def get_position(self):
        return self.i, self.j

    def get_nb_wall(self):
        return self.nb_walls

    def compute_objective(self, walls_h, walls_v):
        return course_in_width(self.i, self.j, walls_h, walls_v, self.goal_i, self.goal_j)
