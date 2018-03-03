class Pose:
    """
    Class which represents a pose in the map, i.e. represents x and y
    corrdinates and rotation. Note: x coordinate is from left to right of the
    screen, y coordinate is from top to bottom of the screen and rotation is
    counter-clockwise and starts on the right.
    """

    def __init__(self, x=None, y=None, psi=0):
        """
        Default constructor for the pose.
        :param x: x coordinate.
        :param y: y coordinate.
        :param psi: psi coordinate.
        """

        self.__x = x
        self.__y = y
        self.__psi = psi

    @property
    def x(self):
        """
        Getter for x coordinate.
        :return: x coordinate.
        """

        return self.__x

    @x.setter
    def x(self, value):
        """
        Setter for x coordinate.
        :param value: Desired x value.
        """

        self.__x = value

    @property
    def y(self):
        """
        Getter for y coordinate.
        :return: y coordinate.
        """

        return self.__y

    @y.setter
    def y(self, value):
        """
        Setter for y coordinate.
        :param value: Desired y value.
        """

        self.__y = value

    @property
    def psi(self):
        """
        Getter for psi coordinate.
        :return: psi coordinate.
        """

        return self.__psi

    @psi.setter
    def psi(self, value):
        """
        Setter for psi coordinate.
        :param value: Desired psi value.
        """

        self.__psi = value
