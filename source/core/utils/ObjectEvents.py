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
    PLACE_BOMB = 8
    WIN = 9
    DIE = 10
