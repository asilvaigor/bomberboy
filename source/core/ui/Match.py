import sys
import pygame
from source.core.utils.Constants import *
from pygame.locals import *
from source.core.ui.Map import Map


class Match:

    def __init__(self):
        self.__menu_font = pygame.font.Font("assets/font/04B_30__.TTF", FONT_SIZE)
        self.__msg = self.__menu_font.render("funcao nao disponivel", True, RED)

        self.__map = Map()

    def draw(self, surface):
        self.__map.draw(surface)
        # surface.fill(BLUE)
        # surface.blit(self.__msg, (surface.get_rect().centerx - self.__msg.get_rect().centerx,
        #                           surface.get_rect().centery - self.__msg.get_rect().centery))

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYUP:
                if event.key == K_BACKSPACE:
                    return MENU
                if event.key == K_ESCAPE:
                    return PAUSE

        return PLAYING_SINGLE
