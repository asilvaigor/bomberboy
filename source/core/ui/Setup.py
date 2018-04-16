import sys
import pygame
from pygame.locals import *
from source.core.utils.Constants import *
from source.core.game_objects.character.Player import Player

PLAY = 0
EXIT = 1


class Setup:

    def __init__(self):
        pass

    def draw(self, surface):
        pass

    def update(self):
        return PLAYING

    def get_characters(self):
        players = list()
        cpus = list()

        player1_keys = {'up': K_w, 'down': K_s, 'left': K_a,
                        'right': K_d, 'bomb': K_v}
        player1 = Player((1, 1), 'bomberboy_white', player1_keys, 0)

        player2_keys = {'up': K_UP, 'down': K_DOWN, 'left': K_LEFT,
                        'right': K_RIGHT, 'bomb': K_m}
        player2 = Player((9, 13), 'bomberboy_black', player2_keys, 1)

        players.append(player1)
        players.append(player2)

        return players, cpus
