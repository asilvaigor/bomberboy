import numpy as np

from source.core.game_objects.character.Character import Character
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

        self.__velocity = np.array([0, 0])

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

        # TODO: Make AI!!
        if not (self._new_event == CharacterEvents.WIN or
                self._new_event == CharacterEvents.DIE):
            self._new_event = CharacterEvents.STOP_DOWN
