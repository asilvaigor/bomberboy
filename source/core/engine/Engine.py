import sys
import pygame
from pygame.locals import *
from source.core.utils.Constants import *
from source.core.ui.Menu import Menu


class Engine:
    """
    Game engine class. This is the class that runs the game and contains the
    map, elements, sounds, status etc.
    """

    def __init__(self):
        """
        Set variables required for window creation.
        """
        pygame.init()

        self.fpsClock = pygame.time.Clock()

        self.__game_name = GAME_NAME
        self.__surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
        pygame.display.set_caption(self.__game_name)

        self.__state = MENU
        self.__menu = Menu()

    def play(self):
        while True:
            if self.__state == MENU:
                self.__menu.draw(self.__surface)
                self.__state = self.__menu.update(self.__surface)

            elif self.__state == FINISH:
                pygame.quit()
                sys.exit()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    pass

                if event.type == KEYUP:
                    pass

            pygame.display.update()

            self.fpsClock.tick(MAX_FPS)
