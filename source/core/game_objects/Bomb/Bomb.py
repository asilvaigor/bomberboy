import numpy as np

from source.core.game_objects.GameObject import GameObject
from source.core.ui.Animation import Animation
from source.core.utils import Constants


class Bomb(GameObject):
    """
    Represents a Bomb object.
    """

    def __init__(self, initial_tile):
        """
        Default constructor for the character.
        :param initial_tile: Initial tile coordinates for the character.
        """

        super().__init__(initial_tile, 'bomb')

        self.__setup_animation()
        self.__force_explosion = False
        self.__icon = self._sprite['small']

    def update(self, clock=None, tilemap=None):
        """
        Updates the character according to its intrinsic status.
        :param clock: Pygame.time.Clock object with the game's clock.
        :param tilemap: Numpy array with the map information.
        :return: True if the bomb has not exploded yet.
        """

        if self.__animation.done() or self.__force_explosion:
            return False

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

    def __setup_animation(self):
        """
        Sets up the bomb's animations, creating an object for it.
        """

        self.__animation = Animation([
            self._sprite['small'], self._sprite['normal'], self._sprite['big'],
            self._sprite['normal'], self._sprite['small'],
            self._sprite['normal'], self._sprite['big'], self._sprite['normal'],
            self._sprite['small']], Constants.BOMB_FRAME_DURATION * np.ones(9),
            stop=True)
