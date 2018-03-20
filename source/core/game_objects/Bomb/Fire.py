import numpy as np
import os

from source.core.game_objects.GameObject import GameObject
from source.core.ui.Animation import Animation
from source.core.ui.Sprite import Sprite
from source.core.utils import Constants


class Fire(GameObject):
    """
    Represents a Fire object.
    """

    def __init__(self, initial_tile, fire_range):
        """
        Default constructor for the character.
        :param initial_tile: Initial tile coordinates for the fire.
        :param fire_range: Fire's range in tile units.
        """

        super().__init__(initial_tile)

        sprite_name = 'fire'
        sprites_dir = (os.path.dirname(os.path.realpath(__file__)) +
                       '/../../../../assets/sprites/')
        self.__sprite = Sprite(sprites_dir + sprite_name + '.png',
                               sprites_dir + sprite_name + '.txt', 0).get_dict()

        self.__range = fire_range
        self.__setup_animations()
        self.__tree = list('middle')

    def update(self, clock, tilemap):
        """
        Updates the fire according to its intrinsic status.
        :param clock: Pygame.time.Clock object with the game's clock.
        :param tilemap: Numpy array with the map information.
        :return: True if the fire still exists.
        """

        if self.__middle_animation.done():
            tilemap[self.tile] = Constants.UNIT_EMPTY
            return False

        tilemap[self.tile] = Constants.UNIT_FIRE
        # TODO: Update tree

        return True

    def draw(self, display):
        """
        Updates the the bomb's icon on the screen, according to its
        animation. Note: This function should be called after update(), and
        only if update() returns True.
        :param display: Pygame display object.
        """

        icon = self.__middle_animation.update()
        display.blit(icon,
                     (self._pose.x - icon.get_size()[0] / 2,
                      self._pose.y + Constants.SQUARE_SIZE / 2 -
                      icon.get_size()[1] + Constants.DISPLAY_HEIGTH))

    def __setup_animations(self):
        """
        Sets up the all the fire's animations, even if the fire does not have
        one of its parts due to the tilemap.
        """

        self.__middle_animation = Animation(np.concatenate(
            [[self.__sprite['middle_thinner'], self.__sprite['middle_thin']],
             np.tile([self.__sprite['middle_normal'],
                      self.__sprite['middle_thick'],
                      self.__sprite['middle_thicker']], 5),
             [self.__sprite['middle_thick'], self.__sprite['middle_normal'],
              self.__sprite['middle_thin'], self.__sprite['middle_thinner']]]),
            Constants.FIRE_FRAME_DURATION * np.ones(21), stop=True)

        self.__up1_animation = Animation(np.concatenate(
            [[self.__sprite['up1_thinner'], self.__sprite['up1_thin']],
             np.tile([self.__sprite['up1_normal'],
                      self.__sprite['up1_thick'],
                      self.__sprite['up1_thicker']], 5),
             [self.__sprite['up1_thick'], self.__sprite['up1_normal'],
              self.__sprite['up1_thin'], self.__sprite['up1_thinner']]]),
            Constants.FIRE_FRAME_DURATION * np.ones(21), stop=True)

        self.__up2_animation = Animation(np.concatenate(
            [[self.__sprite['up2_thinner'], self.__sprite['up1_thin']],
             np.tile([self.__sprite['up2_normal'],
                      self.__sprite['up2_thick'],
                      self.__sprite['up2_thicker']], 5),
             [self.__sprite['up2_thick'], self.__sprite['up2_normal'],
              self.__sprite['up2_thin'], self.__sprite['up2_thinner']]]),
            Constants.FIRE_FRAME_DURATION * np.ones(21), stop=True)

        self.__down1_animation = Animation(np.concatenate(
            [[self.__sprite['down1_thinner'], self.__sprite['down1_thin']],
             np.tile([self.__sprite['down1_normal'],
                      self.__sprite['down1_thick'],
                      self.__sprite['down1_thicker']], 5),
             [self.__sprite['down1_thick'], self.__sprite['down1_normal'],
              self.__sprite['down1_thin'], self.__sprite['down1_thinner']]]),
            Constants.FIRE_FRAME_DURATION * np.ones(21), stop=True)

        self.__down2_animation = Animation(np.concatenate(
            [[self.__sprite['down2_thinner'], self.__sprite['down2_thin']],
             np.tile([self.__sprite['down2_normal'],
                      self.__sprite['down2_thick'],
                      self.__sprite['down2_thicker']], 5),
             [self.__sprite['down2_thick'], self.__sprite['down2_normal'],
              self.__sprite['down2_thin'], self.__sprite['down2_thinner']]]),
            Constants.FIRE_FRAME_DURATION * np.ones(21), stop=True)

        self.__left1_animation = Animation(np.concatenate(
            [[self.__sprite['left1_thinner'], self.__sprite['left1_thin']],
             np.tile([self.__sprite['left1_normal'],
                      self.__sprite['left1_thick'],
                      self.__sprite['left1_thicker']], 5),
             [self.__sprite['left1_thick'], self.__sprite['left1_normal'],
              self.__sprite['left1_thin'], self.__sprite['left1_thinner']]]),
            Constants.FIRE_FRAME_DURATION * np.ones(21), stop=True)

        self.__left2_animation = Animation(np.concatenate(
            [[self.__sprite['left2_thinner'], self.__sprite['left2_thin']],
             np.tile([self.__sprite['left2_normal'],
                      self.__sprite['left2_thick'],
                      self.__sprite['left2_thicker']], 5),
             [self.__sprite['left2_thick'], self.__sprite['left2_normal'],
              self.__sprite['left2_thin'], self.__sprite['left2_thinner']]]),
            Constants.FIRE_FRAME_DURATION * np.ones(21), stop=True)

        self.__right1_animation = Animation(np.concatenate(
            [[self.__sprite['right1_thinner'], self.__sprite['right1_thin']],
             np.tile([self.__sprite['right1_normal'],
                      self.__sprite['right1_thick'],
                      self.__sprite['right1_thicker']], 5),
             [self.__sprite['right1_thick'], self.__sprite['right1_normal'],
              self.__sprite['right1_thin'], self.__sprite['right1_thinner']]]),
            Constants.FIRE_FRAME_DURATION * np.ones(21), stop=True)

        self.__right2_animation = Animation(np.concatenate(
            [[self.__sprite['right2_thinner'], self.__sprite['right2_thin']],
             np.tile([self.__sprite['right2_normal'],
                      self.__sprite['right2_thick'],
                      self.__sprite['right2_thicker']], 5),
             [self.__sprite['right2_thick'], self.__sprite['right2_normal'],
              self.__sprite['right2_thin'], self.__sprite['right2_thinner']]]),
            Constants.FIRE_FRAME_DURATION * np.ones(21), stop=True)
