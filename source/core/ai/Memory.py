from random import randint
import numpy as np

from source.core.utils import Constants


class Memory:
    """
    Class which contains a circular vector with the stored data. It has a getter
    which returns n random elements, which is used in training. Each element
    holds: tilemap, action, reward, died
    """

    def __init__(self, capacity):
        """
        Default constructor. It allocates a vector of the desired capacity and
        puts random elements in it.
        :param capacity: Total capacity of the memory.
        :param initial_memory: Number of initial random elements.
        """

        self.__data = [None] * (capacity + 1)
        self.__start = 0
        self.__end = 0
        self.__size = len(self.__data)

    def get_batch(self, size):
        """
        Returns random samples from the memory, in which each element also
        includes the previous tilemap.
        :param size: Number of samples to be returned.
        :return: List of 5 elements, which are numpy array for each values of:
        previous_tilemap, tilemap, action, reward, died.
        """

        if self.__start == 0 and self.__end - self.__start + 1 < size:
            return None

        map_shape = (size, Constants.NUM_ROWS, Constants.NUM_COLUMNS)
        actions_shape = (size, Constants.NUM_ACTIONS)
        batch = [np.zeros(map_shape, dtype=np.uint8),
                 np.zeros(map_shape, dtype=np.uint8),
                 np.zeros(actions_shape, dtype=np.int8),
                 np.zeros(size, dtype=np.uint8), np.zeros(size, dtype=bool)]
        if self.__start == 0:
            for i in range(size):
                x = randint(1, self.__end - 1)
                batch[0][i] = self.__data[x - 1][0]
                batch[1][i] = self.__data[x][0]
                batch[2][i] = self.__data[x][1]
                batch[3][i] = self.__data[x][2]
                batch[4][i] = self.__data[x][3]

        return batch

    def append(self, tilemap, action, reward, died):
        """
        Appends an element to the circular vector.
        :param tilemap: Numpy array with the map information.
        :param action: Vector of bools which indicate the action taken in this
        state.
        :param reward: Reward the cpu got on the last iteration.
        :param died: Bool to inform if the agent just died.
        """

        self.__data[self.__end] = (np.uint8(tilemap), np.uint8(action),
                                   np.int8(reward), bool(died))

        if self.__full:
            self.__start = (self.__start + 1) % self.__size
        self.__end = (self.__end + 1) % self.__size

    def __full(self):
        """
        Checks if the memory is full.
        """

        return self.__start == (self.__end + 1) % self.__size
