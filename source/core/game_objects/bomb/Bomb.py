import numpy as np
import os

from source.core.game_objects.GameObject import GameObject
from source.core.ui.Animation import Animation
from source.core.ui.Sprite import Sprite
from source.core.utils import Constants


class Bomb(GameObject):
    """
    Represents a Bomb object.
    """

    def __init__(self, initial_tile, range, character_id):
        """
        Default constructor for the character.
        :param initial_tile: Initial tile coordinates for the character.
        :param range: Fire range of the bomb.
        :param character_id: Id of the character which put the bomb.
        """

        super().__init__(initial_tile)

        sprite_name = 'bomb'
        sprites_dir = (os.path.dirname(os.path.realpath(__file__)) +
                       '/../../../../assets/sprites/')
        self.__sprite = Sprite(sprites_dir + sprite_name + '.png',
                               sprites_dir + sprite_name + '.txt',
                               (-2, 0)).get_dict()

        self.__setup_animation()
        self.__force_explosion = False
        self.__icon = self.__animation.update()
        self.__range = range
        self.__character_id = character_id

    def update(self, clock, tilemap):
        """
        Updates the bomb according to its intrinsic status.
        :param clock: Pygame.time.Clock object with the game's clock.
        :param tilemap: Numpy array with the map information.
        :return: True if the bomb has not exploded yet.
        """

        if self.__animation.done() or self.__force_explosion:
            tilemap[self.tile] = Constants.UNIT_EMPTY
            return False

        tilemap[self.tile] = Constants.UNIT_BOMB
        return True

    def draw(self, display):
        """
        Updates the the bomb's icon on the screen, according to its
        animation. Note: This function should be called after update(), and
        only if update() returns True.
        :param display: Pygame display object.
        """

        self.__icon = self.__animation.update()
        display.blit(self.__icon,
                     (self._pose.x - self.__icon.get_size()[0] / 2,
                      self._pose.y + Constants.SQUARE_SIZE / 2 -
                      self.__icon.get_size()[1] + Constants.DISPLAY_HEIGTH - 1))

    def explode(self):
        """
        Forces the explosion of a bomb. This is caused when another bomb's fire
        hits it.
        """

        self.__force_explosion = True

    @property
    def range(self):
        """
        Getter fot the bomb's range in tiles.
        :return: Bomb's range.
        """

        return self.__range

    @property
    def character_id(self):
        """
        Getter for the character's id which placed the bomb.
        :return: Character id which placed the bomb.
        """

        return self.__character_id

    def __setup_animation(self):
        """
        Sets up the bomb's animations, creating an object for it.
        """

        self.__animation = Animation([
            self.__sprite['small'], self.__sprite['normal'], self.__sprite['big'],
            self.__sprite['normal'], self.__sprite['small'],
            self.__sprite['normal'], self.__sprite['big'], self.__sprite['normal'],
            self.__sprite['small']], Constants.BOMB_FRAME_DURATION * np.ones(9),
            stop=True)
