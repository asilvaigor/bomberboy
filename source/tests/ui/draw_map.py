import sys
import time
import pygame
from pygame.locals import *
from source.core.utils.Constants import *

from source.core.ui.Map import Map

pygame.init()
clock = pygame.time.Clock()
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
pygame.display.set_caption("Map Test")

mapa = Map()

t0 = time.time()

while True:

    mapa.draw(t0, surface)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()

    clock.tick(MAX_FPS)
