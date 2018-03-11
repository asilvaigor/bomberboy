import pygame
from source.core.utils.Constants import *


class Menu:
    """
    Game menu class. This is the class that runs the menu interface
    """

    def __init__(self):
        """
        Set variables required for menu creation.
        """

        self.game_font = pygame.font.Font("assets/04B_30__.TTF", FONT_SIZE)
        self.single = self.game_font.render("single player", True, RED)
        self.multi = self.game_font.render("multi player", True, RED)
        self.tutorial = self.game_font.render("how to play", True, RED)
        self.exit = self.game_font.render("exit", True, RED)

        self.logo = pygame.image.load("assets/logo.png")
        self.size = (int(WINDOW_WIDTH*0.85),
                     int(WINDOW_WIDTH*0.488*0.85))
        self.logo = pygame.transform.scale(self.logo, self.size)

    def draw_menu(self, surface):
        surface.fill(BLUE)

        logo_position = (surface.get_rect().centerx - self.logo.get_rect().centerx,
                         surface.get_rect().top - self.logo.get_rect().top + int(WINDOW_HEIGHT*0.03))
        surface.blit(self.logo, logo_position)

        single_position = (surface.get_rect().centerx - self.single.get_rect().centerx,
                           logo_position[1] + self.logo.get_rect().height + 10)
        surface.blit(self.single, single_position)

        multi_position = (surface.get_rect().centerx - self.multi.get_rect().centerx,
                          single_position[1] + self.single.get_rect().height + 10)
        surface.blit(self.multi, multi_position)

        tutorial_position = (surface.get_rect().centerx - self.tutorial.get_rect().centerx,
                             multi_position[1] + self.multi.get_rect().height + 10)
        surface.blit(self.tutorial, tutorial_position)

        exit_position = (surface.get_rect().centerx - self.exit.get_rect().centerx,
                         tutorial_position[1] + self.tutorial.get_rect().height + 10)
        surface.blit(self.exit, exit_position)

