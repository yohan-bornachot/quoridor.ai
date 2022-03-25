import numpy as np
from gamestate import GameState
from player import Player
from board import Board

def display_board(game_state: GameState) -> None:
    # Taille du plateau
    size = len(game_state.board.walls_h)+1

    n_players = game_state.nb_players

    first_str = "#"*5*size + "##  Nombre de murs restants : "
    for i in range(n_players):
        first_str = first_str + " joueur{} {}".format(i,game_state.players[i].get_nb_wall())

    print(first_str) # Ligne du haut

    for i in range(size):
        # La taille des matrices wall_* impose de faire une disjonction de cas selon si on
        # se trouve sur la dernière ligne ou la dernière colonne
        if i==size-1:
            print("#", end="")
            for j in range(size):
                # Si on est sur la dernière ligne et dernière colonne (pas de mur possible):
                if j==size-1:
                    # Si pion sur la case:
                    k=0
                    while k<n_players and (i,j)!=(game_state.players[k].i,game_state.players[k].j):
                        k += 1
                    if k==n_players:
                        print("  .  ", end="")
                    else :
                        print("  {}  ".format(k), end="")

                # Si il y a un mur en (i-1, j), le mur continue car mur de taille 2:
                elif game_state.board.walls_v[i-1, j]==1:
                    # Si en plus un pion est présent:
                    k=0
                    while k<n_players and (i,j)!=(game_state.players[k].i,game_state.players[k].j):
                        k += 1
                    if k==n_players:
                        print("  . |", end="")
                    else :
                        print("  {} |".format(k), end="")
                
                else: # Si pas de mur, et pas dernière colonne (j!=size-1)
                    # Si pion présent en (i,j)
                    k=0
                    while k<n_players and (i,j)!=(game_state.players[k].i,game_state.players[k].j):
                        k += 1
                    if k==n_players:
                        print("  .  ", end="")
                    else :
                        print("  {}  ".format(k), end="")
        else: # i!=size-1 --> Gestion des lignes, et des interlignes
            print("#", end="") # Début de la ligne
            # Ligne
            for j in range(size):
                if j==size-1:
                    k=0
                    while k<n_players and (i,j)!=(game_state.players[k].i,game_state.players[k].j):
                        k += 1
                    if k==n_players:
                        print("  .  ", end="")
                    else :
                        print("  {}  ".format(k), end="")
                else:
                    if i==0:
                        # Si un pion se trouve en (i,j) et qu'il y a un mur vertical qui passe à cet endroit:
                        if game_state.board.walls_v[i, j]==1 :
                            k=0
                            while k<n_players and (i,j)!=(game_state.players[k].i,game_state.players[k].j):
                                k += 1
                            if k==n_players:
                                print("  . |", end="")
                            else :
                                print("  {} |".format(k), end="")
                        else :
                            k=0
                            while k<n_players and (i,j)!=(game_state.players[k].i,game_state.players[k].j):
                                k += 1
                            if k==n_players:
                                print("  .  ", end="")
                            else :
                                print("  {}  ".format(k), end="")
                    else:
                        if (game_state.board.walls_v[i, j]==1 or game_state.board.walls_v[i-1, j]==1):
                            k=0
                            while k<n_players and (i,j)!=(game_state.players[k].i,game_state.players[k].j):
                                k += 1
                            if k==n_players:
                                print("  . |", end="")
                            else :
                                print("  {} |".format(k), end="")
                        else :
                            k=0
                            while k<n_players and (i,j)!=(game_state.players[k].i,game_state.players[k].j):
                                k += 1
                            if k==n_players:
                                print("  .  ", end="")
                            else :
                                print("  {}  ".format(k), end="")

            print("#") # Fin de la ligne

            # Interligne
            print("#", end="") # Début de la ligne
            for j in range(size):
                # Si dernière colonne, il peut y avoir un mur horizontal qui se termine (car 2cases)
                if j==size-1:
                    if game_state.board.walls_h[i, j-1]==1:
                        print("-"*5, end="")
                    else: # Si pas de mur
                        print(" "*5, end="")
                
                elif j==0:
                    if game_state.board.walls_h[i, j]==1:
                        print("-"*5, end="")
                    # Mur vertical
                    elif i==0 and game_state.board.walls_v[i, j]==1:
                        print("    |", end="")
                    elif game_state.board.walls_v[i, j]==1 or game_state.board.walls_v[i-1, j]==1:
                        print("    |", end="")
                    else: # si pas de mur
                        print(" "*5, end="")

                else: # Si pas dernière colonne, on regarde s'il y a des murs
                    # Mur horizontal
                    if game_state.board.walls_h[i, j]==1 or game_state.board.walls_h[i, j-1]==1:
                        print("-"*5, end="")
                    # Mur vertical
                    elif i==0 and game_state.board.walls_v[i, j]==1:
                        print("    |", end="")
                    elif game_state.board.walls_v[i, j]==1 or game_state.board.walls_v[i-1, j]==1:
                        print("    |", end="")
                    else: # Pas de mur
                        print("     ", end="")
        print("#")


    print("#"*5*size + "##")


############ EXEMPLE DE GRILLE ###########

# players : o, x
# murs : | ou - ou " " (si absent)
# case : .

#    ###############################################
#    #  .    .    .    .    o    .    .    .    .  #
#    #----------                                   #
#    #  .    .  | .    .    .    .    .    .    .  #
#    #          |                                  #
#    #  .    .  | .    .    .    .    .    .    .  #
#    #          |                                  #
#    #  .    .    .    .    .    .    .    .    .  #
#    #                         ----------          #
#    #  .    .    .    .    .    o    .    .    .  #
#    #                                             #
#    #  .    .    .    .    .    x    .    .    .  #
#    #                                             #
#    #  .    .    .    .    .    .    .    .    .  #
#    #                                             #
#    #  .    .    .    .    .    .    .    .    .  #
#    #                                             #
#    #  .    .    .    .    x    .    .    .    .  #
#    ###############################################

if __name__== "__main__":
    size = 9
    players[0] = Player(0, size//2, 10)
    players[1] = Player(size-1, size//2, 10)
    board = Board(board_size=9, wall_size=2)
    board.set_v_wall(1, 1)
    board.set_h_wall(0, 0)
    game_state = GameState(players[0], players[1], board, size, size)

    display_board(game_state)