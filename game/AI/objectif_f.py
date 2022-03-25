from logging import raiseExceptions


def basic_objective(state, play_as, gamma = 0.3):
    eps = 1e-4
    obj = (1/(eps+state.objectives[play_as])+gamma*state.players[play_as].get_nb_wall())
    tmp = 0
    for i in range(state.nb_players):
        tmp += (i!=play_as)*(1/(eps+state.objectives[i]-1)+gamma*state.players[i].get_nb_wall())
    obj -= tmp/(state.nb_players-1)

    return obj