from pygame import locals
import numpy as np
import pygame
import sys

from source.core.game_objects.Character.Character import Character
from source.core.utils import Constants
from source.core.utils.ObjectEvents import CharacterEvents
from source.core.utils.Pose import Pose

pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode((Constants.WINDOW_WIDTH,
                                   Constants.WINDOW_HEIGHT))

background = pygame.image.load('../../../../assets/image/background.png')
background = pygame.transform.scale(
    background, (Constants.MAP_WIDTH, Constants.MAP_HEIGTH))

character = Character((1, 1), 'bomberboy_white')
character_event = CharacterEvents.STOP_DOWN
character.update(character_event, clock, np.array([]))
character.draw(display)
character_velocity = np.array([0, 0])

while True:
    display.blit(background, (0, Constants.DISPLAY_HEIGTH))

    if character_event == CharacterEvents.INCREASE_SPEED:
        character_event = None
    for event in pygame.event.get():
        # Quitting game
        if event.type == locals.QUIT:
            pygame.quit()
            sys.exit()

        # If character wins or dies, it can't do anything else.
        if (character_event == CharacterEvents.WIN or
                character_event == CharacterEvents.DIE):
            break

        # Stopping character
        if event.type == locals.KEYUP:
            if event.key == locals.K_LEFT:
                character_velocity += (1, 0)
                character_event = CharacterEvents.STOP_LEFT
            elif event.key == locals.K_RIGHT:
                character_velocity += (-1, 0)
                character_event = CharacterEvents.STOP_RIGHT
            elif event.key == locals.K_UP:
                character_velocity += (0, 1)
                character_event = CharacterEvents.STOP_UP
            elif event.key == locals.K_DOWN:
                character_velocity += (0, -1)
                character_event = CharacterEvents.STOP_DOWN

        # Moving character, with adjustment to accept two keys pressed at the
        # same time.
        if event.type == locals.KEYDOWN:
            if event.key == locals.K_LEFT:
                character_velocity += (-1, 0)
            elif event.key == locals.K_RIGHT:
                character_velocity += (1, 0)
            elif event.key == locals.K_UP:
                character_velocity += (0, -1)
            elif event.key == locals.K_DOWN:
                character_velocity += (0, 1)
            elif event.key == locals.K_q:
                character_event = CharacterEvents.WIN
                break
            elif event.key == locals.K_w:
                character_event = CharacterEvents.DIE
                break
            elif event.key == locals.K_a:
                character_event = CharacterEvents.INCREASE_SPEED
                break

        if character_velocity[1] == 1:
            character_event = CharacterEvents.MOVE_DOWN
        elif character_velocity[1] == -1:
            character_event = CharacterEvents.MOVE_UP
        elif character_velocity[0] == 1:
            character_event = CharacterEvents.MOVE_RIGHT
        elif character_velocity[0] == -1:
            character_event = CharacterEvents.MOVE_LEFT

    # Updates and draws character
    if character.update(character_event, clock, np.array([])):
        character.draw(display)

    pygame.display.update()
    clock.tick(Constants.MAX_FPS)
