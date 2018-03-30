import os
import time
import pygame

from source.core.utils.Constants import *
from source.core.map.Grid import Grid

SCORE_SIZE = SQUARE_SIZE // 2


class Map:

    def __init__(self):
        assets_dir = (os.path.dirname(os.path.realpath(__file__)) +
                      '/../../../assets/')
        self.__brick = pygame.image.load(assets_dir + "image/brick.png")
        self.__block = pygame.image.load(assets_dir + "image/block.png")
        self.__fire = pygame.image.load(assets_dir + "image/fire.png")
        self.__bomb = pygame.image.load(assets_dir + "image/bomb.png")
        self.__shoes = pygame.image.load(assets_dir + "image/shoes.png")

        self.__grid = Grid()
        self.__dim = self.__grid.get_dimension()

        self.__block = pygame.transform.scale(self.__block, (SQUARE_SIZE,
                                                             SQUARE_SIZE))
        self.__brick = pygame.transform.scale(self.__brick, (SQUARE_SIZE,
                                                             SQUARE_SIZE))
        self.__fire = pygame.transform.scale(self.__fire, (SQUARE_SIZE,
                                                           SQUARE_SIZE))
        self.__bomb = pygame.transform.scale(self.__bomb, (SQUARE_SIZE,
                                                           SQUARE_SIZE))
        self.__shoes = pygame.transform.scale(self.__shoes, (SQUARE_SIZE,
                                                             SQUARE_SIZE))

        # Score elements
        self.__player_face = pygame.image.load(assets_dir + "image/bomber_face.png")
        self.__player_face = pygame.transform.scale(self.__player_face, (3 * SCORE_SIZE,
                                                                         3 * SCORE_SIZE))
        self.__font = pygame.font.Font(assets_dir + "font/04B_30__.TTF", 2 * FONT_SIZE)
        self.__time = (0, 0)
        self.__t0 = 0
        self.__last_pause = 0

    def draw(self, t0, ispaused, surface):
        surface.fill(GREEN)

        pos = (0, DISPLAY_HEIGTH)

        for x in range(self.__dim[0]):
            for y in range(self.__dim[1]):
                if self.__grid.__getattr__(position=(x, y)) == UNIT_FIXED_BLOCK:
                    surface.blit(self.__block, pos)
                elif self.__grid.__getattr__(position=(x, y)) == UNIT_BLOCK:
                    surface.blit(self.__brick, pos)
                elif self.__grid.__getattr__(position=(x, y)) == UNIT_POWERUP_FIRE_HIDE:
                    surface.blit(self.__brick, pos)
                elif self.__grid.__getattr__(position=(x, y)) == UNIT_POWERUP_VELOCITY_HIDE:
                    surface.blit(self.__brick, pos)
                elif self.__grid.__getattr__(position=(x, y)) == UNIT_POWERUP_BOMB_HIDE:
                    surface.blit(self.__brick, pos)
                elif self.__grid.__getattr__(position=(x, y)) == UNIT_POWERUP_FIRE_SHOW:
                    surface.blit(self.__fire, pos)
                elif self.__grid.__getattr__(position=(x, y)) == UNIT_POWERUP_VELOCITY_SHOW:
                    surface.blit(self.__shoes, pos)
                elif self.__grid.__getattr__(position=(x, y)) == UNIT_POWERUP_BOMB_SHOW:
                    surface.blit(self.__bomb, pos)

                pos = (pos[0] + SQUARE_SIZE, pos[1])

            pos = (0, pos[1] + SQUARE_SIZE)

        # Draw Score
        self.draw_score(t0, ispaused, surface)

    def update(self):
        pass

    def get_grid(self):
        return self.__grid

    def draw_score(self, t0, ispaused, surface):
        # pos = (3 * SCORE_SIZE, SCORE_SIZE)
        # surface.blit(self.__player_face, pos)

        time_text = self.__font.render(self.get_time(t0, ispaused), True, WHITE)
        time_pos = (surface.get_rect().centerx - time_text.get_rect().centerx,
                    DISPLAY_HEIGTH//2 - time_text.get_rect().centery)
        surface.blit(time_text, time_pos)

    def get_time(self, t0, ispaused):
        delta_t = time.time() - t0
        minute = int(GAME_TIME - (delta_t / 60))
        second = int(60 - (delta_t % 60))
        if not ispaused:
            self.__time = (minute, second)
        return str(self.__time[0]) + ":" + "{:0>2}".format(str(self.__time[1]))
