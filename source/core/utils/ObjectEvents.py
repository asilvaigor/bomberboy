from enum import Enum


class CharacterEvents(Enum):
    MOVE_UP = 0
    MOVE_DOWN = 1
    MOVE_RIGHT = 2
    MOVE_LEFT = 3
    STOP_UP = 4
    STOP_DOWN = 5
    STOP_RIGHT = 6
    STOP_LEFT = 7
    WIN = 8
    DIE = 9
    INCREASE_SPEED = 10
    INCREASE_BOMB = 11
    INCREASE_FIRE = 12
