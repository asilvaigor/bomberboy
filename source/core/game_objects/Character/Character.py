from source.core.game_objects.GameObject import GameObject
import math


class Character(GameObject):
    """
    Abstract class for a BomberBoy character.
    """

    INITIAL_SPEED = 4
    SPEED_INCREMENT = 1.333

    def __init__(self, pose):
        """
        Default constructor for the character.
        :param pose: Initial pose for the character.
        """

        super().__init__(pose)
        self.__velocity = Character.INITIAL_SPEED

    def move(self, direction):
        """
        Moves the character in a desired direction.
        :param direction: Tuple with x and y directions.
        """

        self._pose.x += direction[0] * self.__velocity
        self._pose.y += direction[1] * self.__velocity

        # TODO
        # horiz_free = (math.floor(self._pose.y) + 0.333 < self._pose.y <
        #               math.ceil(self._pose.y) - 0.333)
        # vert_free = (math.floor(self._pose.x) + 0.333 < self._pose.x <
        #              math.ceil(self._pose.x) - 0.333)

    def increase_velocity(self):
        self.__velocity += Character.SPEED_INCREMENT
