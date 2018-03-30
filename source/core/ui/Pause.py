import sys
import pygame
from source.core.utils.Constants import *
from pygame.locals import *


class Pause:

    def __init__(self):
        self.__title_font = pygame.font.Font("assets/font/04B_30__.TTF", int(1.5 * FONT_SIZE))
        self.__menu_font = pygame.font.Font("assets/font/04B_30__.TTF", FONT_SIZE)
        self.__pause_msg = self.__title_font.render("Game paused", True, RED)
        self.__resume = self.__menu_font.render("Resume", True, RED)
        self.__return = self.__menu_font.render("Main menu", True, RED)

        self.__state = IN_GAME
        self.__right = pygame.image.load("assets/image/right_arrow.png")
        self.__left = pygame.image.load("assets/image/left_arrow.png")
        arrow_size = (int(FONT_SIZE * 1.375),
                      FONT_SIZE)
        self.__right = pygame.transform.scale(self.__right, arrow_size)
        self.__left = pygame.transform.scale(self.__left, arrow_size)

    def draw(self, surface):
        # Constants measures
        y = surface.get_rect().centery - self.__pause_msg.get_rect().height - int(FONT_SIZE/2)
        delta = int(WINDOW_HEIGHT * 0.02)

        # Draw blue rect under text
        rect = (surface.get_rect().centerx - self.__pause_msg.get_rect().centerx - 2*delta, y - 2*delta,
                self.__pause_msg.get_rect().width + 4*delta, int(3.5*FONT_SIZE) + 6*delta)
        pygame.draw.rect(surface, BLUE, rect)

        # Write the text
        text = [self.__pause_msg, self.__resume, self.__return]
        for t in text:
            pos = (surface.get_rect().centerx - t.get_rect().centerx, y)
            surface.blit(t, pos)
            y = y + t.get_rect().height + delta

        # Draw arrow selection
        self.draw_arrow(surface)

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYUP:
                # if event.key == K_ESCAPE:
                #     return PLAYING_SINGLE
                if event.key == K_RETURN or event.key == K_KP_ENTER:
                    return self.__state
                elif event.key == K_ESCAPE:
                    return IN_GAME
                elif event.key == K_UP:
                    self.__state -= 1
                    self.__state %= 2
                elif event.key == K_DOWN:
                    self.__state += 1
                    self.__state %= 2

        return PAUSE

    def draw_arrow(self, surface):
        x_r = surface.get_rect().centerx - 3 * self.__right.get_rect().centerx
        x_l = surface.get_rect().centerx + self.__right.get_rect().centerx
        y_0 = int(surface.get_rect().centery)
        delta_y = self.__left.get_rect().height + int(WINDOW_HEIGHT * 0.02)

        if self.__state == IN_GAME:
            right_position = (x_r - self.__resume.get_rect().centerx, y_0)
            left_position = (x_l + self.__resume.get_rect().centerx, y_0)
        elif self.__state == MAIN_MENU:
            right_position = (x_r - self.__return.get_rect().centerx, y_0 + delta_y)
            left_position = (x_l + self.__return.get_rect().centerx, y_0 + delta_y)

        surface.blit(self.__right, right_position)
        surface.blit(self.__left, left_position)
