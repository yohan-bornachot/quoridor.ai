import numpy as np
from pandas import read_gbq

def up(i, j, walls):
    size = len(walls) + 1
    return i>0 and (j == size-1 or walls[i-1, j] == 0) and (j == 0 or walls[i-1,j-1]==0)

def down(i, j, walls):
    size = len(walls) + 1
    return i<size-1 and (j == size-1 or walls[i, j] == 0) and (j == 0 or walls[i,j-1]==0)

def right(i, j, walls):
    size = len(walls) + 1
    return j<size-1 and (i == size-1 or walls[i, j] == 0) and (i == 0 or walls[i-1,j]==0)

def left(i, j, walls):
    size = len(walls) + 1
    return j>0 and (i == size-1 or walls[i, j-1] == 0) and (i == 0 or walls[i-1,j-1]==0)

def course_in_width(i, j, walls_h, walls_v, goal_i, goal_j):
    size = len(walls_h) + 1
    course = np.zeros((size, size))
    course[i,j] = 1
    stack = list()
    stack.append((i,j))

    reach_goal = (goal_i == None and j == goal_j) or (goal_j == None and i == goal_i)
    steps_to_goal = 1

    while len(stack)>0 and not reach_goal: 
        current_stack = stack.copy()
        stack = list()

        for k,l in current_stack:
            if down(k, l, walls_h) and course[k+1, l] == 0:
                course[k+1, l] = course[k, l] + 1
                stack.append((k+1,l))

            if up(k, l, walls_h) and course[k-1, l] == 0:
                course[k-1, l] = course[k, l] + 1
                stack.append((k-1,l))

            if left(k, l, walls_v) and course[k, l-1] == 0:
                course[k, l-1] = course[k, l] + 1
                stack.append((k,l-1))

            if right(k, l, walls_v) and course[k, l+1] == 0:
                course[k, l+1] = course[k, l] + 1
                stack.append((k,l+1))

        if goal_i == None and np.max(course[:,goal_j])>0:
            reach_goal = True
            steps_to_goal = np.max(course[:,goal_j])

        if goal_j == None and np.max(course[goal_i])>0:
            reach_goal = True
            steps_to_goal = np.max(course[goal_i])
        
    if reach_goal : return steps_to_goal - 1 
    return -1

