import time

from .ai import AI

class Human(AI):
    def __init__(self, play_as, time_to_play=10) -> None:
        super().__init__(play_as, time_to_play=time_to_play)

    def select_next_step(self, next_steps):
        licit_move = False
        while not licit_move:
            human_choice = input("Choisir une action : \nm pour un déplacement, \nh pour placer un mur horizontal, \nv pour placer un mur vertical\n")
            if human_choice == "m":
                c = input("Quel déplacement souhaitez vous faire :\nz pour haut,\ns pour bas,\nq pour gauche,\nd pour droite\n")
                if c == "z":

                if c == "q":

                if c == "s":

                if c == "d":
                    
                else :
                    print("Déplacement impossible, veuillez recommencer")
                    

            if human_choice == "h":
                c = input("Donnez la position du mur à placer sour la forme 'i j'")
                try :
                    c_split = c.split(sep = " ")
                    i, j = int(c_split[0]), int(c_split[1])

                except :
                    print("Placement impossible, veuillez recommencer")

            if human_choice == "v":
                c = input("Donnez la position du mur à placer sour la forme 'i j'")
                try :
                    c_split = c.split(sep = " ")
                    i, j = int(c_split[0]), int(c_split[1])
                    
                except :
                    print("Placement impossible, veuillez recommencer")

            
            else :
                print("Déplacement inconnu, veuillez recommencer")