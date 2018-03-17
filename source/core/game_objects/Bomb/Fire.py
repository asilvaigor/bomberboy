from source.core.game_objects.GameObject import GameObject


class Fire(GameObject):
    """
    Represents a Fire object.
    """

    def __init__(self, initial_tile, range):
        """
        Default constructor for the character.
        :param initial_tile: Initial tile coordinates for the fire.
        :param range: Fire's range in tile units.
        """

        super().__init__(initial_tile, 'fire')

        self.__range = range
