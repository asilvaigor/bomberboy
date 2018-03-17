from pygame import locals
import numpy as np
import pygame
import sys

from source.core.game_objects.Character.Player import Player
from source.core.utils import Constants
from source.core.utils.ObjectEvents import CharacterEvents

pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode((Constants.WINDOW_WIDTH,
                                   Constants.WINDOW_HEIGHT))

background = pygame.image.load('../../../../assets/image/background.png')
background = pygame.transform.scale(
    background, (Constants.MAP_WIDTH, Constants.MAP_HEIGTH))

player = Player((1, 1), 'bomberboy_white', {
    'up': locals.K_UP, 'down': locals.K_DOWN, 'left': locals.K_LEFT,
    'right': locals.K_RIGHT})

tilemap = np.ones((11, 15), dtype=np.int) * Constants.UNIT_EMPTY
tilemap[0:11, 0] = Constants.UNIT_FIXED_BLOCK
tilemap[0:11, 14] = Constants.UNIT_FIXED_BLOCK
tilemap[0, 0:15] = Constants.UNIT_FIXED_BLOCK
tilemap[10, 0:15] = Constants.UNIT_FIXED_BLOCK
for i in range(2, 10, 2):
    for j in range(2, 14, 2):
        tilemap[i, j] = Constants.UNIT_FIXED_BLOCK

while True:
    display.blit(background, (0, Constants.DISPLAY_HEIGTH))

    for event in pygame.event.get():
        if event.type == locals.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == locals.KEYUP:
            player.key_up(event.key)

        if event.type == locals.KEYDOWN:
            if event.key == locals.K_q:
                player.special_event(CharacterEvents.WIN)
            elif event.key == locals.K_w:
                player.special_event(CharacterEvents.DIE)
            elif event.key == locals.K_a:
                player.special_event(CharacterEvents.INCREASE_SPEED)
            else:
                player.key_down(event.key)

    # Updates and draws character
    if player.update(clock, tilemap):
        player.draw(display)

    pygame.display.update()
    clock.tick(Constants.MAX_FPS)
