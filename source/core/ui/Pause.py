import sys
import pygame
from source.core.utils.Constants import *
from pygame.locals import *


class Pause:

    def __init__(self):
        self.__menu_font = pygame.font.Font("assets/font/04B_30__.TTF", FONT_SIZE)
        self.__msg = self.__menu_font.render("Paused", True, RED)
        self.__msg_rect = self.__msg.get_rect()

    def draw(self, surface):
        self.__msg_rect.centerx = surface.get_rect().centerx
        self.__msg_rect.centery = surface.get_rect().centery
        pygame.draw.rect(surface, BLUE, (self.__msg_rect.left - 20, self.__msg_rect.top - 20,
                                         self.__msg_rect.width + 40, self.__msg_rect.height + 40))
        surface.blit(self.__msg, self.__msg_rect)

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    return PLAYING_SINGLE

        return PAUSE
