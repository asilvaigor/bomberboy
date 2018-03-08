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

        self.x = x
        self.y = y
        self.psi = psi
