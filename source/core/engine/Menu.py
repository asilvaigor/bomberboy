import pygame
from source.core.utils.Constants import *


class Menu:

    def __init__(self):
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.title = self.font.render(GAME_NAME, True, (0, 0, 0))
        self.single = self.font.render("SINGLE PLAYER", True, (0, 0, 0))
        self.multi = self.font.render("MULTI PLAYER", True, (0, 0, 0))

    def draw_menu(self, surface):
        surface.fill((255, 255, 255))

        # Write the game title
        surface.blit(self.title, (surface.get_rect().centerx - self.title.get_rect().centerx,
                                  surface.get_rect().top + self.title.get_rect().centery))

