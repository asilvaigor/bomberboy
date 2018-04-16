import numpy as np

from source.core.game_objects.character.Character import Character
from source.core.utils.ObjectEvents import CharacterEvents


class Player(Character):
    """
    Represents a bomberboy character controlled by a player. It is derived from
    Character class and allows movement through keyboard events.
    """

    def __init__(self, initial_tile, sprite_name, key_commands, id):
        """
        Default constructor for the character.
        :param initial_tile: Initial tile coordinates for the character.
        :param sprite_name: String to select the character sprite.
        :param key_commands: Dict informing keys used by the user to give.
        :param id: Player's id.
        commands to the bomberboy.
        """

        super().__init__(initial_tile, sprite_name, id)

        self.__velocity = np.array([0, 0])
        self.__key_commands = key_commands

    def key_up(self, key):
        """
        Updates the character velocity and events given that a key was released.
        :param key: pygame.locals key id.
        """

        if not (self._new_event == CharacterEvents.WIN or
                self._new_event == CharacterEvents.DIE):
            if key == self.__key_commands['left']:
                self.__velocity += (1, 0)
                self._new_event = CharacterEvents.STOP_LEFT
            elif key == self.__key_commands['right']:
                self.__velocity += (-1, 0)
                self._new_event = CharacterEvents.STOP_RIGHT
            elif key == self.__key_commands['up']:
                self.__velocity += (0, 1)
                self._new_event = CharacterEvents.STOP_UP
            elif key == self.__key_commands['down']:
                self.__velocity += (0, -1)
                self._new_event = CharacterEvents.STOP_DOWN

            if not self._got_special_event:
                if self.__velocity[1] == 1:
                    self._new_event = CharacterEvents.MOVE_DOWN
                elif self.__velocity[1] == -1:
                    self._new_event = CharacterEvents.MOVE_UP
                elif self.__velocity[0] == 1:
                    self._new_event = CharacterEvents.MOVE_RIGHT
                elif self.__velocity[0] == -1:
                    self._new_event = CharacterEvents.MOVE_LEFT

    def key_down(self, key):
        """
        Updates the character velocity and events given that a key was pressed.
        :param key: pygame.locals key id.
        """

        if not (self._new_event == CharacterEvents.WIN or
                self._new_event == CharacterEvents.DIE):
            if key == self.__key_commands['left']:
                self.__velocity += (-1, 0)
            elif key == self.__key_commands['right']:
                self.__velocity += (1, 0)
            elif key == self.__key_commands['up']:
                self.__velocity += (0, -1)
            elif key == self.__key_commands['down']:
                self.__velocity += (0, 1)
            elif key == self.__key_commands['bomb']:
                self._just_placed_bomb = True

            if not self._got_special_event:
                if self.__velocity[1] == 1:
                    self._new_event = CharacterEvents.MOVE_DOWN
                elif self.__velocity[1] == -1:
                    self._new_event = CharacterEvents.MOVE_UP
                elif self.__velocity[0] == 1:
                    self._new_event = CharacterEvents.MOVE_RIGHT
                elif self.__velocity[0] == -1:
                    self._new_event = CharacterEvents.MOVE_LEFT
