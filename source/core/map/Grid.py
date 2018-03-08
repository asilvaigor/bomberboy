from source.core.utils.Constants import *
import numpy as np

class Grid:
    """
        Create the map of the game
    """

    def __init__(self):
        self.__row = WINDOW_HEIGHT//SQUARE_SIZE
        self.__colum = WINDOW_WIDTH//SQUARE_SIZE
        self.__tilemap = np.zeros(shape = (self.__row, self.__colum), dtype = np.int)


    @property
    def tilemap(self):
        return self.__tilemap
