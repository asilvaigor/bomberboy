import sys
import pygame
from pygame.locals import *
from source.core.utils.Constants import *
from source.core.ui.Menu import Menu
from source.core.engine.Match import Match
#from source.core.ui.Pause import Pause


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
        self.__menu = Menu()
        self.__match = Match()

    def play(self):
        # self.__song.play(-1)
        while True:
            if self.__state == MENU:
                self.__menu.draw(self.__surface)
                self.__state = self.__menu.update()

            elif self.__state == PLAYING_SINGLE or self.__state == PAUSE:
                self.__state = self.__match.play(self.fpsClock, self.__surface, self.__state)

            elif self.__state == FINISH:
                pygame.quit()
                sys.exit()

            pygame.display.update()

            self.fpsClock.tick(MAX_FPS)
