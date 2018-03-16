import os

from source.core.ui.Sprite import Sprite
from source.core.utils import Constants
from source.core.utils.Pose import Pose


class GameObject:
    """
    A GameObject is an element that will be placed on the map. Possible
    GameObjects: BomberBoy, bomb, powerup and obstacles.
    """

    def __init__(self, initial_tile, sprite_name):
        """
        Default constructor for the GameObject.
        :param initial_tile: Initial tile coordinates for the object.
        :param sprite_name:
        """

        sprites_dir = (os.path.dirname(os.path.realpath(__file__)) +
                       '/../../../assets/sprites/')
        self._sprite = Sprite(sprites_dir + sprite_name + '.gif',
                              sprites_dir + sprite_name + '.txt').get_dict()

        self._pose = Pose(3 * initial_tile[0] * Constants.SQUARE_SIZE / 2,
                          3 * initial_tile[1] * Constants.SQUARE_SIZE / 2)

    def update(self, clock, tilemap=None):
        """
        Abstract method which updates the game object intrinsic information.
        :param clock: Pygame.time.Clock object with the game's clock.
        :param tilemap: Numpy array, optional, which contains the current map
        information.
        :return: True if the object still exists.
        """

        pass

    def draw(self, display):
        """
        Abstract method which updates the game object icon on the screen.
        :param display: Pygame display object.
        """

        pass

    @property
    def pose(self):
        """
        Getter for the game object's pose on the map in pixels.
        :return: Object's pose in pixels.
        """

        return self._pose
