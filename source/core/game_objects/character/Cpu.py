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
        self.__counter = 0
        self.__decision = CharacterEvents.NOTHING

        self.__initial_tile = initial_tile
        self.__sprite_name = sprite_name

    def decide(self, tilemap, characters):
        """
        Decides the IA next move.
        :param tilemap: Numpy array with the map information.
        :param characters: List of characters in the match.
        """

        enemies_pos = list()
        for c in characters:
            if c.id != self.id:
                enemies_pos.append(c.tile)

        if self.__counter < Constants.FRAME_UPDATE_RATE:
            self.__counter += 1
        else:
            self.__agent.observe(tilemap, enemies_pos)
            self.__decision = self.__agent.act()
            self.__counter = 0
        if not (self._new_event == CharacterEvents.WIN or
                self._new_event == CharacterEvents.DIE):
            self._new_event = self.__decision

    def reset(self):
        """
        Resets the cpu to its initial position and state. This method is used
        during training.
        """

        super().__init__(self.__initial_tile, self.__sprite_name, self.id)
        self.__counter = 0
