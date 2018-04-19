import numpy as np

from source.core.ai.Agent import Agent
from source.core.game_objects.character.Character import Character
from source.core.utils import Constants
from source.core.utils.ObjectEvents import CharacterEvents


class Cpu(Character):
    """
    Represents a bomberboy character controlled by a cpu. It is derived from
    Character class.
    """

    def __init__(self, initial_tile, sprite_name, id, load=False):
        """
        Default constructor for the character.
        :param initial_tile: Initial tile coordinates for the character.
        :param sprite_name: String to select the character sprite.
        :param id: Character's id.
        :param load: Optional bool to load a neural network instead of
        creating a new one.
        """

        super().__init__(initial_tile, sprite_name, id)
        self.__agent = Agent(id, load)
        self.__delay_counter = 0
        self.__reward_counter = 0
        self.__decision = CharacterEvents.NOTHING

        self.__initial_tile = initial_tile
        self.__sprite_name = sprite_name

    def decide(self, tilemap, characters, clock, force=False):
        """
        Decides the IA next move. This method limits the IA thinking decision to
        every k frames.
        :param tilemap: Numpy array with the map information.
        :param characters: List of characters in the match.
        :param clock: Pygame clock.
        :param force: Forces the cpu to decide something, independent on its
        delay counter.
        """

        # Finding enemies positions
        input = np.array(tilemap)
        for c in characters:
            if c.id == self.id:
                input[c.tile] = Constants.UNIT_SELF
            else:
                input[c.tile] = Constants.UNIT_ENEMY

        # Adjusting IA decision delay time
        self.__delay_counter += clock.get_time()

        # Updating IA
        if self.__delay_counter > Constants.UPDATE_DELAY or force:
            self.__decision = self.__agent.decide(input, self.__reward_counter,
                                                  not self.is_alive)
            self.__delay_counter %= Constants.UPDATE_DELAY
            self.__reward_counter = 0
        if not (self._new_event == CharacterEvents.WIN or
                self._new_event == CharacterEvents.DIE):
            self._new_event = self.__decision

    def reset(self):
        """
        Resets the cpu to its initial position and state. This method is used
        during training.
        """

        super().__init__(self.__initial_tile, self.__sprite_name, self.id)
        self.__delay_counter = 0

    def get_reward(self):
        """
        Getter for the current reward.
        :return: Cpus current reward.
        """

        return self.__reward_counter

    def reward(self, reward):
        """
        Gives a reward to the cpu for a given action.
        :param reward:
        :return:
        """

        if self.is_alive:
            self.__reward_counter += reward
