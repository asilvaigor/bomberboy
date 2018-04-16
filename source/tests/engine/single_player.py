from pygame.locals import *
import pygame

from source.core.engine.Match import Match
from source.core.utils import Constants
from source.core.game_objects.character.Player import Player

pygame.init()
clock = pygame.time.Clock()
surface = pygame.display.set_mode((Constants.WINDOW_WIDTH,
                                   Constants.WINDOW_HEIGHT), 0, 32)

players = list()
cpus = list()

player1_keys = {'up': K_w, 'down': K_s, 'left': K_a,
                'right': K_d, 'bomb': K_v}
player1 = Player((1, 1), 'bomberboy_white', player1_keys, 0)
players.append(player1)

match = Match((players, cpus))

while True:
    match.play(clock, surface)
    pygame.display.update()
    clock.tick(Constants.MAX_FPS)
