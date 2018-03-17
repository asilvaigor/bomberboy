from pygame import locals
import pygame
import sys

from source.core.engine.Match import Match
from source.core.utils import Constants

pygame.init()
clock = pygame.time.Clock()
surface = pygame.display.set_mode((Constants.WINDOW_WIDTH,
                                   Constants.WINDOW_HEIGHT), 0, 32)
match = Match()

while True:
    match.play(clock, surface)
    pygame.display.update()
    clock.tick(Constants.MAX_FPS)
