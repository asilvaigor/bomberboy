from random import random

from source.core.utils.ObjectEvents import CharacterEvents


class Agent:
    def __init__(self):
        pass

    def decide(self, tilemap, enemies_pos, reward):
        x = random()
        if x < 1 / 6:
            return CharacterEvents.NOTHING
        elif x < 2 / 6:
            return CharacterEvents.PLACE_BOMB
        elif x < 3 / 6:
            return CharacterEvents.MOVE_LEFT
        elif x < 4 / 6:
            return CharacterEvents.MOVE_UP
        elif x < 5 / 6:
            return CharacterEvents.MOVE_RIGHT
        else:
            return CharacterEvents.MOVE_DOWN
