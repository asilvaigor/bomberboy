import sys
import pygame
from pygame.locals import *
from source.core.utils.Constants import *
from source.core.ui.Menu import Menu
from source.core.engine.Match import Match


# from source.core.ui.Pause import Pause


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

        self.__song = pygame.mixer.Sound("assets/song/song.ogg")

        self.__state = MENU
        self.__menu = None
        self.__match = None

    def play(self):
        # self.__song.play(-1)
        while True:
            if self.__state == MENU:
                if not self.__menu:  # Verify that the pointer is null
                    self.__menu = Menu()
                    del self.__match
                    self.__match = None
                self.__menu.draw(self.__surface)
                self.__state = self.__menu.update()

            elif self.__state == PLAYING_SINGLE:
                if not self.__match:  # Verify that the pointer is null
                    self.__match = Match()
                    del self.__menu
                    self.__menu = None
                self.__state = self.__match.play(self.fpsClock, self.__surface)

            elif self.__state == FINISH:
                pygame.quit()
                sys.exit()

            pygame.display.update()

            self.fpsClock.tick(MAX_FPS)
