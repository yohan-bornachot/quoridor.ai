import numpy as np

def up(i, j, walls):
    return i>0 and walls[i-1, j] == 0 and (j == 0 or walls[i-1,j-1]==0)

def down(i, j, walls):
    size = len(walls) + 1
    return i<size-1 and walls[i+1, j] == 0 and (j == 0 or walls[i,j-1]==0)

def right(i, j, walls):
    size = len(walls) + 1
    return j<size-1 and walls[i, j+1] == 0 and (i == 0 or walls[i-1,j]==0)

def left(i, j, walls):
    return j>0 and walls[i, j-1] == 0 and (i == 0 or walls[i-1,j-1]==0)

def course_in_width(i, j, walls_h, walls_v, goal):
    size = len(walls_h) + 1
    course = np.zeros((size, size))
    course[i,j] = 1
    stack = list()
    stack.append((i,j))

    while len(stack)>0 and np.min(course[goal]) == 0: 
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
    
    return np.min(course[goal]) - 1

