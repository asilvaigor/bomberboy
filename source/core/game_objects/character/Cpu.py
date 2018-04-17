from source.core.ai.Agent import Agent
from source.core.game_objects.character.Character import Character
from source.core.utils import Constants
from source.core.utils.ObjectEvents import CharacterEvents


class Cpu(Character):
    """
    Represents a bomberboy character controlled by a cpu. It is derived from
    Character class.
    """

    def __init__(self, initial_tile, sprite_name, id):
        """
        Default constructor for the character.
        :param initial_tile: Initial tile coordinates for the character.
        :param sprite_name: String to select the character sprite.
        :param id: Character's id.
        """

        super().__init__(initial_tile, sprite_name, id)
        self.__agent = Agent()
        self.__frame_counter = 0
        self.__reward_counter = 0
        self.__decision = CharacterEvents.NOTHING

        self.__initial_tile = initial_tile
        self.__sprite_name = sprite_name

    def decide(self, tilemap, characters):
        """
        Decides the IA next move. This method limits the IA thinking decision to
        every k frames.
        :param tilemap: Numpy array with the map information.
        :param characters: List of characters in the match.
        """

        enemies_pos = list()
        for c in characters:
            if c.id != self.id:
                enemies_pos.append(c.tile)

        if self.__frame_counter < Constants.FRAME_UPDATE_RATE:
            self.__frame_counter += 1
        else:
            self.__decision = self.__agent.decide(tilemap, enemies_pos,
                                                  self.__reward_counter)
            self.__frame_counter = 0
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
        self.__frame_counter = 0

    def reward(self, reward):
        """
        Gives a reward to the cpu for a given action.
        :param reward:
        :return:
        """

        self.__reward_counter += reward
