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

        self.game_name = GAME_NAME
        self.window_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
        pygame.display.set_caption(self.game_name)

        self.state = MENU
        self.menu = Menu()

    def play(self):
        while True:
            if self.state == MENU:
                self.menu.draw(self.window_screen)
                self.menu.update()

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
