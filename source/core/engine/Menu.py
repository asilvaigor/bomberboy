import sys
import pygame
from pygame.locals import *
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
        self.menu_font = pygame.font.Font("assets/font/04B_30__.TTF", FONT_SIZE)
        self.single = self.menu_font.render("single player", True, RED)
        self.multi = self.menu_font.render("multi player", True, RED)
        self.tutorial = self.menu_font.render("how to play", True, RED)
        self.exit = self.menu_font.render("exit", True, RED)

        # Set logo's image
        self.logo = pygame.image.load("assets/image/logo.png")
        logo_size = (int(WINDOW_WIDTH * 0.85),
                     int(WINDOW_WIDTH * 0.488 * 0.85))
        self.logo = pygame.transform.scale(self.logo, logo_size)

        # End page text
        self.end_font = pygame.font.Font("assets/font/04B_30__.TTF", int(FONT_SIZE / 1.3))
        self.institution = self.end_font.render("2018 - ITA", True, RED)
        self.authors = self.end_font.render("Heladio, Igor, Jose Otavio", True, RED)

        # Arrows
        self.right = pygame.image.load("assets/image/rightarrow.png")
        arrow_size = (int(FONT_SIZE * 1.375),
                      FONT_SIZE)
        self.right = pygame.transform.scale(self.right, arrow_size)

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

    def draw_arrow(self, surface, state):
        x_r = surface.get_rect().centerx - 3 * self.right.get_rect().centerx
        y = surface.get_rect().centery

        if state == "single":
            right_position = (x_r - self.single.get_rect().centerx, y)
        elif state == "multi":
            right_position = (x_r - self.multi.get_rect().centerx, y)
        elif state == "tutorial":
            right_position = (x_r - self.tutorial.get_rect().centerx, y)
        else:
            right_position = (x_r - self.exit.get_rect().centerx, y)

        surface.blit(self.right, right_position)

    def check_for_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                pass

            if event.type == MOUSEBUTTONUP:
                pass
