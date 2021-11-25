import time

from .ai import AI

class Human(AI):
    def __init__(self, play_as, time_to_play=10) -> None:
        super().__init__(play_as, time_to_play=time_to_play)

    def select_next_step(self,state, next_steps):
        licit_move = False
        while not licit_move:
            human_choice = input("Choisir une action : \nm pour un déplacement, \nh pour placer un mur horizontal, \nv pour placer un mur vertical\n")
            if human_choice == "m":
                c = input("Quel déplacement souhaitez vous faire :\nz pour haut,\ns pour bas,\nq pour gauche,\nd pour droite\n")
                try :
                    if c == "z":
                        i = state.possible_moves.index("u")
                        return next_steps[i]
                    if c == "q":
                        i = state.possible_moves.index("l")
                        return next_steps[i]
                    if c == "s":
                        i = state.possible_moves.index("d")
                        return next_steps[i]
                    if c == "d":
                        i = state.possible_moves.index("r")
                        return next_steps[i]
                    else :
                        print("Déplacement impossible, veuillez recommencer")
                except :
                    print("Déplacement impossible, veuillez recommencer")
                        

            if human_choice == "h":
                c = input("Donnez la position du mur à placer sour la forme 'i j'")
                try :
                    c_split = c.split(sep = " ")
                    i, j = int(c_split[0]), int(c_split[1])
                    ind = state.possible_moves.index("h{}{}".format(i,j))
                    return next_steps[ind]
                except :
                    print("Placement impossible, veuillez recommencer")

            if human_choice == "v":
                c = input("Donnez la position du mur à placer sour la forme 'i j'")
                try :
                    c_split = c.split(sep = " ")
                    i, j = int(c_split[0]), int(c_split[1])
                    ind = state.possible_moves.index("v{}{}".format(i,j))
                    return next_steps[ind]
                except :
                    print("Placement impossible, veuillez recommencer")

            
            else :
                print("Déplacement inconnu, veuillez recommencer")