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

        self.__x = x
        self.__y = y

    @property
    def x(self):
        """
        Getter for x velocity.
        :return: x velocity.
        """

        return self.__x

    @x.setter
    def x(self, value):
        """
        Setter for x velocity.
        :param value: Desired x velocity value.
        """

        self.__x = value

    @property
    def y(self):
        """
        Getter for y velocity.
        :return: y velocity.
        """

        return self.__y

    @y.setter
    def y(self, value):
        """
        Setter for y velocity.
        :param value: Desired y velocity value.
        """

        self.__y = value
