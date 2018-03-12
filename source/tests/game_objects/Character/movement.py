import pygame
from pygame.locals import *
import sys
from source.core.game_objects.Character.Character import Character
from source.core.utils.ObjectEvents import CharacterEvents
from source.core.utils.Pose import Pose
import numpy as np
from source.core.utils.Constants import MAX_FPS

pygame.init()
clock = pygame.time.Clock()

width = 450
height = 330
display = pygame.display.set_mode((width, height), 0, 32)

background = pygame.image.load('../../../../assets/image/background_test.png')
character = Character(Pose(0, 0), 'bomberboy_white')
character_event = CharacterEvents.STOP_DOWN
character.update(character_event, clock, np.array([]))
character.draw(display)
character_velocity = np.array([0, 0])

while True:
    display.blit(background, (0, 0))

    for event in pygame.event.get():
        # Quitting game
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # If character wins or dies, it can't do anything else.
        if (character_event == CharacterEvents.WIN or
                character_event == CharacterEvents.DIE):
            break

        # Stopping character
        if event.type == KEYUP:
            if event.key == K_LEFT:
                character_velocity += (1, 0)
                character_event = CharacterEvents.STOP_LEFT
            elif event.key == K_RIGHT:
                character_velocity += (-1, 0)
                character_event = CharacterEvents.STOP_RIGHT
            elif event.key == K_UP:
                character_velocity += (0, 1)
                character_event = CharacterEvents.STOP_UP
            elif event.key == K_DOWN:
                character_velocity += (0, -1)
                character_event = CharacterEvents.STOP_DOWN

        # Moving character, with adjustment to accept two keys pressed at the
        # same time.
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                character_velocity += (-1, 0)
            elif event.key == K_RIGHT:
                character_velocity += (1, 0)
            elif event.key == K_UP:
                character_velocity += (0, -1)
            elif event.key == K_DOWN:
                character_velocity += (0, 1)
            elif event.key == K_q:
                character_event = CharacterEvents.WIN
                break
            elif event.key == K_w:
                character_event = CharacterEvents.DIE
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
    clock.tick(MAX_FPS)
