import numpy as np
from gamestate import GameState
from player import Player
from board import Board

def display_board(game_state: GameState=GameState(9, 10, 2)) -> None:
    # Taille du plateau
    size = len(game_state.board.walls_h)+1

    print("#"*5*size + "##") # Ligne du haut

    for i in range(size):
        # La taille des matrices wall_* impose de faire une disjonction de cas selon si on
        # se trouve sur la dernière ligne ou la dernière colonne
        if i==size-1:
            print("#", end="")
            for j in range(size):
                # Si on est sur la dernière ligne et dernière colonne (pas de mur possible):
                if j==size-1:
                    # Si pion sur la case:
                    if (i,j)==(game_state.player2.i,game_state.player2.j):
                        print("  x  ", end="")  
                    elif (i,j)==(game_state.player1.i,game_state.player1.j):
                        print("  o  ", end="")
                    # Si rien sur la case:
                    else:
                        print("  .  ", end="")
                # Si il y a un mur en (i-1, j), le mur continue car mur de taille 2:
                elif game_state.board.walls_v[i-1, j]==1:
                    # Si en plus un pion est présent:
                    if (i,j)==(game_state.player2.i,game_state.player2.j):
                        print("  x |", end="")
                    elif (i,j)==(game_state.player1.i,game_state.player1.j):
                        print("  o  ", end="")
                    # Si pas de pion (juste un mur)
                    else:
                        print("  . |", end="")
                
                else: # Si pas de mur, et pas dernière colonne (j!=size-1)
                    # Si pion présent en (i,j)
                    if (i,j)==(game_state.player2.i,game_state.player2.j):
                        print("  x  ", end="")
                    elif (i,j)==(game_state.player1.i,game_state.player1.j):
                        print("  o  ", end="")
                    # Si pas de pion
                    else:
                        print("  .  ", end="")
        else: # i!=size-1 --> Gestion des lignes, et des interlignes
            print("#", end="") # Début de la ligne
            # Ligne
            for j in range(size):
                # Si un pion se trouve en (i,j) et qu'il y a un mur vertical qui passe à cet endroit:
                if (i,j)==(game_state.player1.i,game_state.player1.j) and (game_state.board.walls_v[i, j]==1 or game_state.board.walls_v[i-1, j]==1):
                    print("  o |", end="")
                elif (i,j)==(game_state.player2.i,game_state.player2.j) and (game_state.board.walls_v[i, j]==1 or game_state.board.walls_v[i-1, j]==1):
                    print("  x |", end="")
                # Si pas de mur, mais pion présent en (i,j)
                elif (i,j)==(game_state.player1.i,game_state.player1.j):
                    print("  o  ", end="")
                elif (i,j)==(game_state.player2.i,game_state.player2.j):
                    print("  x  ", end="")
                else: # Si pas de pion
                    # Si dernière colonne, pas de mur
                    if j==size-1:
                        print("  .  ", end="")
                    else:
                        # Sinon, il peut y avoir un mur, dans ce cas:
                        if game_state.board.walls_v[i, j]==1 or game_state.board.walls_v[i-1, j]==1:
                            print("  . |", end="")
                        else: # Si pas de mur, case basique
                            print("  .  ", end="")
            print("#") # Fin de la ligne

            # Interligne
            print("#", end="") # Début de la ligne
            for j in range(size):
                # Si dernière colonne, il peut y avoir un mur horizontal qui se termine (car 2cases)
                if j==size-1:
                    if game_state.board.walls_h[i, j-1]==1:
                        print("-"*5, end="")
                    else: # Si pas de mur
                        print("     ", end="")
                else: # Si pas dernière colonne, on regarde s'il y a des murs
                    # Mur horizontal
                    if game_state.board.walls_h[i, j]==1 or game_state.board.walls_h[i, j-1]==1:
                        print("-"*5, end="")
                    # Mur vertical
                    elif game_state.board.walls_v[i, j]==1 or game_state.board.walls_v[i-1, j]==1:
                        print("    |", end="")
                    # Pas de mur
                    else:
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
#    #                                             #
#    #  .    .    .    .    .    .    .    .    .  #
#    #                                             #
#    #  .    .    .    .    .    .    .    .    .  #
#    #                                             #
#    #  .    .    .    .    .    .    .    .    .  #
#    #                                             #
#    #  .    .    .    .    .    .    .    .    .  #
#    #                                             #
#    #  .    .    .    .    x    .    .    .    .  #
#    ###############################################

if __name__== "__main__":
    size = 9
    player1 = Player(0, size//2, 10)
    player2 = Player(size-1, size//2, 10)
    board = Board(board_size=9, wall_size=2)
    board.set_v_wall(1, 1)
    board.set_h_wall(0, 0)
    game_state = GameState(player1, player2, board)

    display_board(game_state)