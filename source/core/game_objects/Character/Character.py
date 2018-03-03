from source.core.game_objects.GameObject import GameObject


class Character(GameObject):
    """
    Abstract class for a BomberBoy character.
    """

    def __init__(self, pose):
        """
        Default constructor for the character.
        :param pose: Initial pose for the character.
        """

        super().__init__(pose)

    def move(self, velocity):
        """
        Moves the character with a desired velocity.
        :param velocity: Tuple with x and y velocities.
        """

        pass
