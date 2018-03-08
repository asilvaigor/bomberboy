class Velocity:
    """
    Class which represents a character walking velocity. Note: x is from left to
    right on the screen and y is from top to bottom on the screen.
    """

    def __init__(self, x, y):
        """
        Default constructor for the velocity.
        :param x: x coordinate velocity.
        :param y: y coordinate velocity.
        """

        self.x = x
        self.y = y
