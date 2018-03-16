from pygame import locals
import numpy as np
import pygame
import sys

from source.core.game_objects.Character.Character import Character
from source.core.ui.Map import Map
from source.core.utils import Constants
from source.core.utils.ObjectEvents import CharacterEvents

pygame.init()
clock = pygame.time.Clock()
surface = pygame.display.set_mode((Constants.WINDOW_WIDTH,
                                   Constants.WINDOW_HEIGHT), 0, 32)
mapa = Map()

character = Character((1, 1), 'bomberboy_white')

while True:
    mapa.draw(surface)

    for event in pygame.event.get():
        if event.type == locals.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == locals.KEYUP:
            character.key_up(event.key)

        if event.type == locals.KEYDOWN:
            if event.key == locals.K_q:
                character.special_event(CharacterEvents.WIN)
            elif event.key == locals.K_w:
                character.special_event(CharacterEvents.DIE)
            elif event.key == locals.K_a:
                character.special_event(CharacterEvents.INCREASE_SPEED)
            else:
                character.key_down(event.key)

    # Updates and draws character
    if character.update(clock, mapa.get_grid().get_tilemap()):
        character.draw(surface)

    pygame.display.update()
    clock.tick(Constants.MAX_FPS)
