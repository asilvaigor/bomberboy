from pygame.locals import *
import sys
import pygame

from source.core.game_objects.character.Player import Player
from source.core.game_objects.character.Cpu import Cpu
from source.core.utils import Constants


class CharacterSelection:
    """
    Class which handles the character selection block.
    """

    def __init__(self, id, xi, yi, xf, yf):
        """
        Default constructor. It initializes the variables used.
        :param id: Character's id on the match.
        :param xi: Left x coordinate for this block.
        :param yi: Top y coordinate for this block.
        :param xf: Right x coordinate for this block.
        :param yf: Bottom y coordinate for this block.
        """

        self.__id = id
        self.__xi = xi
        self.__yi = yi
        self.__width = xf - xi
        self.__height = yf - yi
        self.__is_selected = False

        # Default player selection options
        if id == 0:
            self.__type = 'Player'
            self.__sprite_name = 'bomberboy_white'
            self.__keys = {'up': K_w, 'down': K_s, 'left': K_a,
                           'right': K_d, 'bomb': K_v}
        elif id == 1:
            self.__type = 'Cpu'
            self.__sprite_name = 'bomberboy_black'
        elif id == 2:
            self.__type = 'Cpu'
            self.__sprite_name = 'bomberboy_blue'
        elif id == 3:
            self.__type = 'Cpu'
            self.__sprite_name = 'bomberboy_orange'

    def draw(self, surface):
        """
        Draws the block on the screen.
        :param surface: Pygame surface.
        """

        delta = 10
        rect = (self.__xi + delta, self.__yi + delta,
                self.__width - delta, self.__height - delta)
        if self.__is_selected:
            color = Constants.GREEN
        else:
            color = Constants.GRAY
        self.__roundedRect(surface, rect, color, 0.1)

    def update(self, selection):
        """
        Updates the block's animation and buttons.
        :param selection: Current block selected by the user.
        :return: Selection variable updated in case the user has finished
        selecting this block.
        """

        self.__is_selected = (selection == self.__id)
        if self.__is_selected:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYUP:
                    if event.key == K_RETURN or event.key == K_KP_ENTER:
                        selection += 1
                    elif event.key == K_BACKSPACE:
                        selection -= 1
                    elif event.key == K_ESCAPE:
                        selection = -1

        return selection

    def get_character(self):
        """
        Getter for the character object which must be generated in the game.
        :return: Character class object which will be in the game, or None if
        no character was selected.
        """

        pos = (1, 1)
        if self.__id == 1:
            pos = (1, 13)
        elif self.__id == 2:
            pos = (9, 1)
        elif self.__id == 3:
            pos = (9, 13)

        if self.__type == 'Player':
            return Player(pos, self.__sprite_name, self.__keys, self.__id)
        elif self.__type == 'Cpu':
            return Cpu(pos, self.__sprite_name, self.__id)
        else:
            return None

    @staticmethod
    def __roundedRect(surface, rect, color, radius):
        """
        Draws a filled rectangle with rounded edges on the surface.
        @param surface: Pygame surface.
        @param rect: Pygame rect object.
        @param color: Pygame color object.
        @param radius: Float from 0 to 1 representing the edges radius.
        """

        rect = pygame.Rect(rect)
        color = pygame.Color(*color)
        alpha = color.a
        color.a = 0
        pos = rect.topleft
        rect.topleft = 0, 0
        rectangle = pygame.Surface(rect.size, SRCALPHA)

        circle = pygame.Surface([min(rect.size) * 3] * 2, SRCALPHA)
        pygame.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
        circle = pygame.transform.smoothscale(circle,
                                       [int(min(rect.size) * radius)] * 2)

        radius = rectangle.blit(circle, (0, 0))
        radius.bottomright = rect.bottomright
        rectangle.blit(circle, radius)
        radius.topright = rect.topright
        rectangle.blit(circle, radius)
        radius.bottomleft = rect.bottomleft
        rectangle.blit(circle, radius)

        rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
        rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))

        rectangle.fill(color, special_flags=BLEND_RGBA_MAX)
        rectangle.fill((255, 255, 255, alpha), special_flags=BLEND_RGBA_MIN)

        return surface.blit(rectangle, pos)
