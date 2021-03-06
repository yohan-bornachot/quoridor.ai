def inv_objective(a, b):
    eps = 1e-6
    return 1/(a + eps) - 1/(b + eps)

def sum_objective(a, b):
    return a - b

def basic_objective(dist1, dist2, nb_wall1, nb_wall2, gamma = 0.1):
    return inv_objective(dist1, dist2) + gamma*sum_objective(nb_wall1, nb_wall2)