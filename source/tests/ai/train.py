import pygame
import time

from source.tests.ai.SurfaceStub import SurfaceStub
from source.core.engine.Match import Match
from source.core.game_objects.character.Cpu import Cpu
from source.core.utils import Constants
from source.core.ui.SpriteHandler import SpriteHandler


"""
Trains the reinforcement learning ai algorithm. This script allows or not 
visualization and controlling game speed.
"""

# Script constants
VISUALIZE = True
Constants.TIME_SPEEDER = 3
Constants.INITIAL_SPEED *= Constants.TIME_SPEEDER
Constants.SPEED_INCREMENT *= Constants.TIME_SPEEDER
Constants.MAX_SPEED *= Constants.TIME_SPEEDER
Constants.BOMB_FRAME_DURATION /= Constants.TIME_SPEEDER
Constants.FIRE_FRAME_DURATION /= Constants.TIME_SPEEDER
Constants.UPDATE_DELAY /= Constants.TIME_SPEEDER
Constants.INITIAL_DELAY /= Constants.TIME_SPEEDER

# Initiating pygame
pygame.init()
clock = pygame.time.Clock()
surface = pygame.display.set_mode((Constants.WINDOW_WIDTH,
                                   Constants.WINDOW_HEIGHT), 0, 32)
if not VISUALIZE:
    surface = SurfaceStub()

# Initiating sprites and ai's
sprites = SpriteHandler().sprites
characters = (list(), list())
positions = [(1, 1), (1, 13), (9, 1), (9, 13)]
for i in range(len(positions)):
    characters[1].append(Cpu(positions[i], sprites[Constants.colors[0]], i))

# Game loop
match_id = 0
while match_id < 5000:
    match = Match(characters, sprites)

    state = Constants.STATE_PLAYING
    t = time.time()
    while not match.is_over():
        match.play(clock, surface)
        pygame.display.update()
        clock.tick()

    print("Match", match_id, "completed. Duration:", time.time() - t)
    match_id += 1

    for c in characters[1]:
        c.reset()
    del match
