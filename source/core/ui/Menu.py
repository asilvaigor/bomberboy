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
        self.__menu_font = pygame.font.Font("assets/font/04B_30__.TTF", FONT_SIZE)
        self.__single = self.__menu_font.render("single player", True, RED)
        self.__multi = self.__menu_font.render("multi player", True, RED)
        self.__tutorial = self.__menu_font.render("how to play", True, RED)
        self.__exit = self.__menu_font.render("exit", True, RED)

        # Set logo's image
        self.__logo = pygame.image.load("assets/image/logo.png")
        logo_size = (int(WINDOW_WIDTH * 0.85),
                     int(WINDOW_WIDTH * 0.488 * 0.85))
        self.__logo = pygame.transform.scale(self.__logo, logo_size)

        # End page text
        self.___end_font = pygame.font.Font("assets/font/04B_30__.TTF", int(FONT_SIZE / 1.4))
        self.__institution = self.___end_font.render("2018 - ITA", True, RED)
        self.__authors = self.___end_font.render("Heladio, Igor, Jose Otavio", True, RED)

        # Arrows
        self.__right = pygame.image.load("assets/image/rightarrow.png")
        arrow_size = (int(FONT_SIZE * 1.375),
                      FONT_SIZE)
        self.__right = pygame.transform.scale(self.__right, arrow_size)

    def draw(self, surface):
        # Set background color
        surface.fill(BLUE)

        # Draw bomber boy's logo
        logo_position = (surface.get_rect().centerx - self.__logo.get_rect().centerx,
                         surface.get_rect().top - self.__logo.get_rect().top + int(WINDOW_HEIGHT * 0.03))
        surface.blit(self.__logo, logo_position)

        # Draw menu buttons
        y = int(surface.get_rect().centery + 1.5 * FONT_SIZE)
        text = [self.__single, self.__multi, self.__tutorial, self.__exit]
        for t in text:
            position = (surface.get_rect().centerx - t.get_rect().centerx, y)
            surface.blit(t, position)
            y = y + t.get_rect().height + int(WINDOW_HEIGHT * 0.03)

        # Draw end page text
        authors_position = (surface.get_rect().centerx - self.__authors.get_rect().centerx,
                            surface.get_rect().bottom - self.__authors.get_rect().height - int(WINDOW_HEIGHT * 0.01))
        surface.blit(self.__authors, authors_position)
        institution_position = (surface.get_rect().centerx - self.__institution.get_rect().centerx,
                                authors_position[1] - self.__institution.get_rect().height)
        surface.blit(self.__institution, institution_position)

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                pass

            if event.type == KEYUP:
                pass

            if event.type == K_KP_ENTER:
                pass

    def draw_arrow(self, surface, state):
        x_r = surface.get_rect().centerx - 3 * self.__right.get_rect().centerx
        y_0 = int(surface.get_rect().centery + 1.5 * FONT_SIZE)

        if state == "single":
            right_position = (x_r - self.__single.get_rect().centerx, y_0)
        elif state == "multi":
            right_position = (x_r - self.__multi.get_rect().centerx, y_0)
        elif state == "tutorial":
            right_position = (x_r - self.__tutorial.get_rect().centerx, y_0)
        else:
            right_position = (x_r - self.__exit.get_rect().centerx, y_0)

        surface.blit(self.__right, right_position)
