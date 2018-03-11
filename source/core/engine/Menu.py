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
        # Set default font and texts
        self.menu_font = pygame.font.Font("assets/04B_30__.TTF", FONT_SIZE)
        self.single = self.menu_font.render("single player", True, RED)
        self.multi = self.menu_font.render("multi player", True, RED)
        self.tutorial = self.menu_font.render("how to play", True, RED)
        self.exit = self.menu_font.render("exit", True, RED)

        # Set logo's image
        self.logo = pygame.image.load("assets/logo.png")
        self.size = (int(WINDOW_WIDTH * 0.85),
                     int(WINDOW_WIDTH * 0.488 * 0.85))
        self.logo = pygame.transform.scale(self.logo, self.size)

        # End page text
        self.end_font = pygame.font.Font("assets/04B_30__.TTF", int(FONT_SIZE/1.3))
        self.institution = self.end_font.render("2018 - ITA", True, RED)
        self.authors = self.end_font.render("Heladio, Igor, Jose Otavio", True, RED)

    def draw_menu(self, surface):
        # Set background color
        surface.fill(BLUE)

        # Draw bomber boy's logo
        logo_position = (surface.get_rect().centerx - self.logo.get_rect().centerx,
                         surface.get_rect().top - self.logo.get_rect().top + int(WINDOW_HEIGHT * 0.03))
        surface.blit(self.logo, logo_position)

        # Draw menu buttons
        y = surface.get_rect().centery
        text = [self.single, self.multi, self.tutorial, self.exit]
        for t in text:
            position = (surface.get_rect().centerx - t.get_rect().centerx, y)
            surface.blit(t, position)
            y = y + t.get_rect().height + int(WINDOW_HEIGHT * 0.03)

        # Draw end page text
        authors_position = (surface.get_rect().centerx - self.authors.get_rect().centerx,
                            surface.get_rect().bottom - self.authors.get_rect().height - int(WINDOW_HEIGHT * 0.01))
        surface.blit(self.authors, authors_position)
        institution_position = (surface.get_rect().centerx - self.institution.get_rect().centerx,
                                authors_position[1] - self.institution.get_rect().height)
        surface.blit(self.institution, institution_position)
