import os
import sys
import pygame
from source.core.utils.Constants import *
from pygame.locals import *


class GameOver:

    def __init__(self):
        assets_path = (os.path.dirname(os.path.realpath(__file__)) +
                       '/../../../assets/')

        self.__font_size = int(FONT_SIZE / 1.2)
        self.__title_font = pygame.font.Font(assets_path + "font/04B_30__.TTF",
                                             self.__font_size)
        self.__msg1 = self.__title_font.render("Game Over!", True, RED)
        self.__msg2 = self.__title_font.render(
            " Press ESC to return to Main Menu.", True, RED)

        self.__state = OVER

    def draw(self, surface):
        # Constants measures
        y = (surface.get_rect().centery -
             self.__msg1.get_rect().height - int(FONT_SIZE / 2))
        delta = FONT_SIZE / 10

        # Draw blue rect under text
        rect = (surface.get_rect().centerx -
                self.__msg2.get_rect().centerx - delta,
                y - 3 * delta,
                self.__msg2.get_rect().width + 2 * delta,
                2 * self.__font_size + 6 * delta)
        pygame.draw.rect(surface, BLUE, rect)

        # Write the text
        text = [self.__msg1, self.__msg2]
        for t in text:
            pos = (surface.get_rect().centerx - t.get_rect().centerx, y)
            surface.blit(t, pos)
            y = y + t.get_rect().height + delta

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    return MAIN_MENU

        return OVER
