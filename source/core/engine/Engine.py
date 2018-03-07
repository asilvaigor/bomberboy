import pygame
import sys
from pygame.locals import *


class Engine:
    """
    Game engine class. This is the class that runs the game and contains the
    map, elements, sounds, status etc.
    """

    def __init__(self):
        """
        Set variables required for window creation.
        """
        self.screen_width = 500
        self.screen_height = 700
        self.game_name = "Bomber Boy"
        self.window_screen = None

    def play(self):
        self.start_window()

        self.main_loop()

    def start_window(self):
        """
        Creates the game play window
        """
        pygame.init()
        self.window_screen = pygame.display.set_mode((self.screen_height, self.screen_width), 0, 32)
        pygame.display.set_caption(self.game_name)

    def main_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
