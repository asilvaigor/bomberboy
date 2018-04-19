from source.core.ai.Brain import Brain
from source.core.utils.ObjectEvents import CharacterEvents


class Agent:
    """
    Class which does the interface between the Cpu and the Q-Learning classes.
    """

    def __init__(self, id, load=False):
        """
        Default constructor.
        :param id: Cpu's id.
        :param load: Optional bool to load a neural network instead of
        creating a new one.
        """

        self.__brain = Brain(id, load)

    def decide(self, tilemap, reward, died):
        """
        Decides the action to be executed provided the Q-Learning output.
        :param tilemap: Numpy array with the map information.
        :param reward: Reward the cpu got on the last iteration.
        :param died: Bool to inform if the agent just died.
        :return: A CharacterEvent.
        """

        x = self.__brain.think(tilemap, reward, died)
        if x == 0:
            return CharacterEvents.NOTHING
        elif x == 1:
            return CharacterEvents.PLACE_BOMB
        elif x == 2:
            return CharacterEvents.MOVE_LEFT
        elif x == 3:
            return CharacterEvents.MOVE_UP
        elif x == 4:
            return CharacterEvents.MOVE_RIGHT
        else:
            return CharacterEvents.MOVE_DOWN
