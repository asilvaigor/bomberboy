from source.core.utils.Constants import *
import random
import numpy as np


class Grid:
    """
        Create the map of the game
    """

    def __init__(self):
        self.__row = (MAP_HEIGTH // SQUARE_SIZE)
        self.__colum = MAP_WIDTH // SQUARE_SIZE
        self.__tilemap = np.zeros(shape=(self.__row, self.__colum), dtype=np.int)
        self.map_generate()

    def map_generate(self):
        """Generate the initial map"""
        # Put the blocks and the fixed blocks on the map
        for i in range(1, self.__row - 1):
            for j in range(1, self.__colum - 1):
                if i + j <= 3 or i + j >= 23 or (j == 13 and (i == 1 or i == 2)) or (j == 12 and i == 1) or (
                        i == 11 and (j == 1 or j == 2)) or (i == 10 and j == 1):
                    self.__tilemap[i][j] = UNIT_EMPTY
                elif (i % 2 == 0 and j % 2 == 0):
                    self.__tilemap[i][j] = UNIT_FIXED_BLOCK
                else:
                    self.__tilemap[i][j] = UNIT_BLOCK

        # Put the powerups on the map
        for i in range(NUMBER_POWERUPS):
            # Defines the position of the power up
            x = random.randint(1, self.__colum - 1)
            y = random.randint(1, self.__row - 1)
            while (self.__tilemap[y][x] != 3):
                x = random.randint(1, self.__colum - 1)
                y = random.randint(1, self.__row - 1)

            # Define which powerup will be put on the map
            self.__tilemap[y][x] = random.randint(UNIT_POWERUP_FIRE_HIDE, UNIT_POWERUP_BOMB_HIDE)

        for i in range(NUMBER_EMPTY):
            # Defines the position of the empty
            x = random.randint(1, self.__colum - 1)
            y = random.randint(1, self.__row - 1)
            while (self.__tilemap[y][x] != 3):
                x = random.randint(1, self.__colum - 1)
                y = random.randint(1, self.__row - 1)
            self.__tilemap[y][x] = UNIT_EMPTY

    def __getattr__(self, position):
        """Returns the map created"""
        return self.__tilemap[position[0]][position[1]]

    def get_tilemap(self):
        return self.__tilemap

    def get_dimension(self):
        dim = (self.__row, self.__colum)
        return dim
