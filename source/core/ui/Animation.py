from pygame import time


class Animation:
    """
    Class which represents an animation, i.e. it runs a list of keyframes with a
    duration for each one.
    """

    def __init__(self, keyframe_list, durations, stop=False):
        """
        Default constructor, which stores each icon of the sprite and its
        duration.
        Note: If the update function is not called on frame, the animation will
        stop on that icon and return to it when called again. This can be bad if
        the animation must start at a specific icon or if the game object will
        not be deleted after the animation, but I (@igor) dont think this will
        happen in the game.
        :param keyframe_list: List of pygame.image's with each keyframe of the
        animation in order.
        :param durations: List of time duration for each icon in seconds.
        :param stop: Bool which chooses a looping animation or one that has an
        end. If it is true, the animation will stop after iterating through all
        icons, activating the done() method.
        """

        self.__keyframes = keyframe_list
        self.__durations = durations
        self.__stop = stop
        self.__done = False

        self.__last_transition_time = 0
        self.__current_id = -1

    def update(self):
        """
        Updates the animation icon according to the durations and elapsed time.
        :return: Keyframe the animation is currently in.
        """

        if (self.__current_id == -1 or
                time.get_ticks() - self.__last_transition_time >
                self.__durations[self.__current_id] * 1000):
            self.__last_transition_time = time.get_ticks()

            if self.__current_id < len(self.__durations) - 1:
                self.__current_id += 1
            elif not self.__stop:
                self.__current_id = 0
            else:
                self.__done = True

        return self.__keyframes[self.__current_id]

    def set_durations(self, durations):
        """
        Sets new durations for each icon.
        :param durations: List of new durations in seconds.
        """

        self.__durations = durations

    def done(self):
        """
        Checks if the animation is finished. This method only returns True if
        'stop' is True in the constructor.
        :return: If the animation is finished.
        """

        return self.__done
