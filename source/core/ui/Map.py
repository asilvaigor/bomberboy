import sys
import pygame
from pygame.locals import *

from source.core.utils.Constants import *
from source.core.map.Grid import Grid


class Map:

    def __init__(self):
        self.brick = pygame.image.load("../../../assets/image/brick.png")
        self.block = pygame.image.load("../../../assets/image/block.png")

        self.grid = Grid()
        self.dim = self.grid.get_dimension()

        self.block = pygame.transform.scale(self.block, (SQUARE_SIZE,
                                                         SQUARE_SIZE))
        self.brick = pygame.transform.scale(self.brick, (SQUARE_SIZE,
                                                         SQUARE_SIZE))

    def draw(self, surface):
        surface.fill(GREEN)

        pos = (0, 0)

        for x in range(self.dim[0]):
            for y in range(self.dim[1]):
                if self.grid.__getattr__(position=(x, y)) == UNIT_FIXED_BLOCK:
                    surface.blit(self.block, pos)
                elif self.grid.__getattr__(position=(x, y)) == UNIT_BLOCK:
                    surface.blit(self.brick, pos)

                pos = (pos[0]+SQUARE_SIZE, pos[1])

            pos = (0, pos[1]+SQUARE_SIZE)

    def update(self):
        pass
