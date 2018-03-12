from pygame import time


class Animation:
    def __init__(self, icons_list, durations, stop=False):
        self.__icons = icons_list
        pass

    def update(self):
        return self.__icons[0]

    def set_transition_frequency(self):
        pass

    def done(self):
        pass
