from source.core.ui.Sprite import Sprite


class GameObject:
    """
    A GameObject is an element that will be placed on the map. Possible
    GameObjects: BomberBoy, bomb, powerup and obstacles.
    """

    def __init__(self, pose, sprite_name):
        """
        Default constructor for the GameObject.
        :param pose: Initial pose for the object.
        :param sprite_name:
        """

        sprites_dir = '../../../../assets/sprites/'
        self._sprite = Sprite(sprites_dir + sprite_name + '.gif',
                              sprites_dir + sprite_name + '.txt').get_dict()

        self._pose = pose

    def update(self, event, clock, tilemap=None):
        """
        Abstract method which updates the game object intrinsic information.
        :param event: ObjectEvents variable.
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
