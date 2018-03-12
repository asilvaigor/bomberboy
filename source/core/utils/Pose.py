class Pose:
    """
    Class which represents a pose in the map, i.e. represents x and y
    corrdinates and rotation. Note: x coordinate is from left to right of the
    screen and y coordinate is from top to bottom of the screen.
    """

    def __init__(self, x=None, y=None):
        """
        Default constructor for the pose.
        :param x: x coordinate.
        :param y: y coordinate.
        """

        self.x = x
        self.y = y
