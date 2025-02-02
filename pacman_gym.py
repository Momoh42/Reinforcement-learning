from gym import Env
from gym import spaces

import numpy as np
import copy


VIDE = 0
PACMAN = 1
BLOQUE = 2
FANTOME = 3
PACDOT = 4

HAUT = 0
BAS = 1
GAUCHE = 2
DROITE = 3


class PacmanEnvironment(Env):
    def __init__(self, rows, cols, num_ghosts=1, num_pac_dots=1, block_percentage=0.1, move_ghost=False, num_map=0):
        super().__init__()

        if num_map == 1 :
            self.rows = 4
            self.cols = 5
        elif num_map == 2 :
            self.rows = 6
            self.cols = 5
        elif num_map == 3 :
            self.rows = 10
            self.cols = 10
        else:
            self.rows = rows
            self.cols = cols

        self.grid = np.zeros((self.rows, self.cols), dtype=float)

        self.block_positions = []
        self.block_percentage = block_percentage 

        self.pacman_pos = None

        self.ghost_pos = None
        self.num_ghosts = num_ghosts
        self.ghost_positions = []
        self.move_ghost = move_ghost

        self.dot_pos = None
        self.num_pac_dots = num_pac_dots
        self.dot_positions = []

        self.reward = 0
        self.game_over = False


        if num_map == 1 :
            self.place_objects_map_1()
        elif num_map == 2 :
            self.place_objects_map_2()
        elif num_map == 3 :
            self.place_objects_map_3()
        else:
            self.place_objects()

        self.init = copy.deepcopy(self)

    def step(self, action):
        self.move_pacman(action)
        if self.move_ghost == True :
            self.move_ghosts()
        observation = self.grid
        reward = self.reward
        done = self.game_over
        info = {}

        return observation, reward, done, info

    def reset(self):
        etat_initial = copy.deepcopy(self.init)
        self.__dict__.update(etat_initial.__dict__)
        return etat_initial.grid

    def render(self, mode='human'):
        if mode == 'human':
            self.display()
        else:
            super().render(mode=mode)
        
    ########################################################
    #                      GETS                            #
    ########################################################
    
    def get_num_rows(self):
        return self.rows

    def get_num_cols(self):
        return self.cols

    def get_state(self):
        return self.pacman_pos
    
    def is_game_over(self):
        return self.game_over
    
    def get_reward(self):
        return self.reward

    def get_all_states(self):
        all_states = [(i, j) for i in range(self.rows) for j in range(self.cols)]
        return all_states
    
    def get_state_size(self):
        return len(self.get_state())
    
    def get_action_size(self):
        return len(self.get_possible_actions())
    
    def get_possible_actions(self):
        return [HAUT, BAS, GAUCHE, DROITE]
        
    ########################################################
    #               PLACEMENT DES OBJETS                   #
    ########################################################

    def place_objects(self):

    # Place des PAC-DOT de manière aléatoire
        for _ in range(self.num_pac_dots):
            dot_pos = tuple(np.random.randint(0, high=(self.rows, self.cols)))
            while dot_pos == self.pacman_pos or dot_pos in self.ghost_positions:
                dot_pos = tuple(np.random.randint(0, high=(self.rows, self.cols)))
            self.dot_positions.append(dot_pos)
            self.grid[dot_pos] = PACDOT

     # Place un fantôme aléatoire, en faisant en sorte qu'il ne soit pas sur PAC-DOT
        for _ in range(self.num_ghosts):
            while True:
                ghost_pos = tuple(np.random.randint(0, high=(self.rows, self.cols)))
                # Vérifier que la position du fantôme ne chevauche pas d'autres objets
                if (
                    self.grid[ghost_pos] == VIDE and
                    ghost_pos not in self.dot_positions and
                    ghost_pos != self.pacman_pos and
                    ghost_pos not in self.ghost_positions
                ):
                    break
            self.ghost_positions.append(ghost_pos)
            self.grid[ghost_pos] = FANTOME

        # Place des blocs aléatoirement en faisant en sorte qu'il ne soit ni sur PAC-DOT ni sur GHOST
        # 10% de la grille sera couvert de blocs
        num_blocks = int(self.block_percentage * self.rows * self.cols)
        for _ in range(num_blocks):
            while True:
                block_pos = tuple(np.random.randint(0, high=(self.rows, self.cols)))
                # Vérifier que la position du bloc ne chevauche pas d'autres objets
                if (
                    self.grid[block_pos] == VIDE and
                    block_pos not in self.dot_positions and
                    block_pos not in self.ghost_positions and
                    block_pos != self.pacman_pos
                ):
                    break
            self.block_positions.append(block_pos)
            self.grid[block_pos] = BLOQUE

        # Place un pacman en faisant en sorte qu'il ne soit ni sur un bloc, un fantôme ou sur le PAC-DOT
        while True:
            self.pacman_pos = tuple(np.random.randint(0, high=(self.rows, self.cols)))
            if (
                self.grid[self.pacman_pos] == VIDE and
                self.pacman_pos not in self.dot_positions and
                self.pacman_pos not in self.ghost_positions
            ):
                break
        self.grid[self.pacman_pos] = PACMAN
        
    ########################################################
    #    PLACEMENT DES OBJETS COMME SUR L'ENNONCE          #
    ########################################################
            
    def place_objects_map_1(self):

        # Place des PAC-DOT selon le schéma
        self.dot_positions = [
            (3, 2)
        ]

        for pacdot_pos in self.dot_positions:
            self.grid[pacdot_pos] = PACDOT

        # Place un fantôme selon le schéma
        self.ghost_positions = [
            (2, 0)
        ]

        for ghost_pos in self.ghost_positions:
            self.grid[ghost_pos] = FANTOME

        # Place un pacman selon le schéma
        self.pacman_pos = (0, 4)
        self.grid[self.pacman_pos] = PACMAN

        # Place des blocs selon le schéma
        self.block_positions = [
            (1, 2), (1, 3), (1, 4),
            (2, 2)
        ]

        for block_pos in self.block_positions:
            self.grid[block_pos] = BLOQUE

    ########################################################
    #                      MAP 2                           #
    ########################################################

    def place_objects_map_2(self):

        # Place des PAC-DOT selon le schéma
        self.dot_positions = [
            (5, 2)
        ]

        for pacdot_pos in self.dot_positions:
            self.grid[pacdot_pos] = PACDOT

        # Place un fantôme selon le schéma
        self.ghost_positions = [
            (2, 2)
        ]

        for ghost_pos in self.ghost_positions:
            self.grid[ghost_pos] = FANTOME

        # Place un pacman selon le schéma
        self.pacman_pos = (0, 2)
        self.grid[self.pacman_pos] = PACMAN

        # Place des blocs selon le schéma
        self.block_positions = [
            (1, 1), (1, 2), (1, 3),
            (3, 1), (3, 2), (3, 3)
        ]

        for block_pos in self.block_positions:
            self.grid[block_pos] = BLOQUE

    ########################################################
    #                      MAP 3                           #
    ########################################################

    def place_objects_map_3(self):

        # Place des PAC-DOT selon le schéma
        self.dot_positions = [
            (4, 4)
        ]

        for pacdot_pos in self.dot_positions:
            self.grid[pacdot_pos] = PACDOT

        # Place un fantôme selon le schéma
        self.ghost_positions = [
            (8, 1), (1, 8)
        ]

        for ghost_pos in self.ghost_positions:
            self.grid[ghost_pos] = FANTOME

        # Place un pacman selon le schéma
        self.pacman_pos = (1, 1)
        self.grid[self.pacman_pos] = PACMAN

        # Place des blocs selon le schéma
        self.block_positions = [
            (3,9), (3,8), (3,7), (3,6), 
            (9,3), (8,3), (7,3), (6,3),
            (4, 6), (5, 6), (6, 6), 
            (6, 5), (6, 4)
        ]

        for block_pos in self.block_positions:
            self.grid[block_pos] = BLOQUE
            
    
    #########################################################
    #                 MOUVEMENT DU PACMAN                   #
    #########################################################

    def move_pacman(self, action):
        new_pos = self.pacman_pos

        if action == HAUT and self.pacman_pos[0] > 0  :
            new_pos = (self.pacman_pos[0] - 1, self.pacman_pos[1])
        elif action == BAS and self.pacman_pos[0] < self.rows - 1  :
            new_pos = (self.pacman_pos[0] + 1, self.pacman_pos[1])
        elif action == GAUCHE and self.pacman_pos[1] > 0 :
            new_pos = (self.pacman_pos[0], self.pacman_pos[1] - 1) 
        elif action == DROITE and self.pacman_pos[1] < self.cols - 1  :
            new_pos = (self.pacman_pos[0], self.pacman_pos[1] + 1) 
            
        # maj de la grille et vérification des colisions
        self.grid[self.pacman_pos] = VIDE
        
        for block_pos in self.block_positions:
            self.grid[block_pos] = BLOQUE

        if self.grid[new_pos] == PACDOT:
            self.reward = +10
            self.game_over = True
        elif self.grid[new_pos] == FANTOME:
            self.reward = -10
            self.game_over = True
        elif self.grid[new_pos] == BLOQUE:
            self.reward = -1
            new_pos = self.pacman_pos
        else:
            self.reward = 0

        self.pacman_pos = new_pos
        self.grid[self.pacman_pos] = PACMAN

    #########################################################
    #                 MOUVEMENT DES FANTOMES                #
    #########################################################
    
    def move_ghosts(self):
        for ghost_index in range(self.num_ghosts):
            ghost_pos = self.ghost_positions[ghost_index]

            # Déplacement aléatoire des fantômes
            valid_moves = self.get_possible_actions()
            np.random.shuffle(valid_moves)  # Mélanger l'ordre des directions pour plus de variété

            new_pos = ghost_pos

            for action in valid_moves:
                if action == HAUT:
                    new_x, new_y = ghost_pos[0] - 1, ghost_pos[1]
                    if new_x >= 0 and self.grid[new_x, new_y] != BLOQUE and self.grid[new_x, new_y] != PACDOT:
                        new_pos = (new_x, new_y)
                        break

                elif action == BAS:
                    new_x, new_y = ghost_pos[0] + 1, ghost_pos[1]
                    if new_x < self.grid.shape[0] and self.grid[new_x, new_y] != BLOQUE and self.grid[new_x, new_y] != PACDOT:
                        new_pos = (new_x, new_y)
                        break

                elif action == GAUCHE:
                    new_x, new_y = ghost_pos[0], ghost_pos[1] - 1
                    if new_y >= 0 and self.grid[new_x, new_y] != BLOQUE and self.grid[new_x, new_y] != PACDOT:
                        new_pos = (new_x, new_y)
                        break

                elif action == DROITE:
                    new_x, new_y = ghost_pos[0], ghost_pos[1] + 1
                    if new_y < self.grid.shape[1] and self.grid[new_x, new_y] != BLOQUE and self.grid[new_x, new_y] != PACDOT:
                        new_pos = (new_x, new_y)
                        break

            # Mettre à jour la position du fantôme dans la liste
            self.ghost_positions[ghost_index] = new_pos
            self.grid[ghost_pos] = VIDE
            self.grid[new_pos] = FANTOME
 
            # On vérifie si un fantome a mangé un pacman
            if new_pos == self.pacman_pos :  
                self.reward = -10
                self.game_over = True

    #########################################################
    #                FONCTIONS D'AFFICHAGE                  #
    #########################################################

    def display(self):
        print('\n')
        for row in self.grid:
            row_str = ''
            for cell in row:
                if cell == VIDE :
                    row_str += '. '
                elif cell == BLOQUE:
                    row_str += 'B '
                elif cell == FANTOME:
                    row_str += 'G '
                elif cell == PACDOT:
                    row_str += 'D '
                elif cell == PACMAN:
                    row_str += 'P '
                else:
                    row_str += '? '
            print(row_str)
        print('Récompense :', self.reward)
        print('\n')
    
    def display_pos(self):
        print('Block positions :', self.block_positions)
        print('Ghost positions :', self.ghost_positions)
        print('Pacman position :', self.pacman_pos)
        print('Partie terminée :', self.game_over )
        print('Recompense :', self.reward)
        print('\n')