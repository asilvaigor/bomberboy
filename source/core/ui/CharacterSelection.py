from pygame.locals import *
import numpy as np
import os
import sys
import pygame

from source.core.game_objects.character.Player import Player
from source.core.game_objects.character.Cpu import Cpu
from source.core.ui.Animation import Animation
from source.core.utils import Constants


class CharacterSelection:
    """
    Class which handles the character selection block.
    """

    def __init__(self, id, sprites, xi, yi, xf, yf):
        """
        Default constructor. It initializes the variables used.
        :param id: Character's id on the match.
        :param sprites: Dict of sprites used in the game.
        :param xi: Left x coordinate for this block.
        :param yi: Top y coordinate for this block.
        :param xf: Right x coordinate for this block.
        :param yf: Bottom y coordinate for this block.
        """

        self.__id = id
        self.__sprites = sprites
        self.__xi = xi
        self.__yi = yi
        self.__width = xf - xi
        self.__height = yf - yi
        self.__selection = 0
        self.__option = 0

        # Loading font and arrows
        assets_path = (os.path.dirname(os.path.realpath(__file__)) +
                       '/../../../assets/')
        size = 20
        self.__font = pygame.font.Font(assets_path + "font/04B_30__.TTF", size)
        self.__font.set_italic(True)
        self.__right = pygame.image.load(assets_path + "image/left_arrow.png")
        self.__left = pygame.image.load(assets_path + "image/right_arrow.png")
        self.__right = pygame.transform.scale(self.__right, (size, size))
        self.__left = pygame.transform.scale(self.__left, (size, size))

        # Default player selection options
        if id == 0:
            self.__type_index = Constants.WASD
            self.__color_index = 0
        elif id == 1:
            self.__type_index = Constants.CPU
            self.__color_index = 1
        elif id == 2:
            self.__type_index = Constants.CPU
            self.__color_index = 2
        elif id == 3:
            self.__type_index = Constants.CPU
            self.__color_index = 3

        # Setting up animations
        self.__setup_animations()

        # Coordinates
        self.__msg_w = 0.32 * self.__width
        self.__msg1_h = 0.3 * self.__height
        self.__msg2_h = 0.4 * self.__height
        self.__msg3_h = 0.7 * self.__height - size

    def draw(self, surface):
        """
        Draws the block on the screen.
        :param surface: Pygame surface.
        :param sprites: Dict of sprites used in the game.
        """

        # Drawing background rectangle
        delta = 10
        rect = (self.__xi + delta, self.__yi + delta,
                self.__width - delta, self.__height - delta)
        if self.__selection < self.__id:
            color = Constants.GRAY
        elif self.__selection == self.__id:
            color = Constants.YELLOW
        else:
            color = Constants.LIGHT_GREEN
        self.__rounded_rect(surface, rect, color, 0.1)

        if self.__type_index == Constants.NONE:
            msg = self.__font.render('None', True, Constants.RED)
            surface.blit(msg, (
                self.__xi + self.__width / 2 - msg.get_rect().width / 2,
                self.__yi + self.__height * 0.4))
            return

        # Drawing current character
        if self.__selection < self.__id:
            icon = self.__not_chosed_animation[
                Constants.colors[self.__color_index]].update()
        elif self.__selection == self.__id:
            icon = self.__choosing_animation[
                Constants.colors[self.__color_index]].update()
        else:
            icon = self.__chosed_animation[
                Constants.colors[self.__color_index]].update()
        icon = pygame.transform.scale(icon, (icon.get_rect().width * 2,
                                             icon.get_rect().height * 2))
        if self.__type_index != Constants.NONE:
            surface.blit(icon, (
                self.__xi + self.__width * 0.65,
                self.__yi + (self.__height - icon.get_rect().height) / 2))

        # Drawing type options
        if self.__type_index == Constants.WASD:
            type_msg1 = 'Player'
            type_msg2 = '(WASD+C)'
        elif self.__type_index == Constants.IJKL:
            type_msg1 = 'Player'
            type_msg2 = '(IJKL+B)'
        elif self.__type_index == Constants.ARROWS:
            type_msg1 = 'Player'
            type_msg2 = '(Arrows+;)'
        else:
            type_msg1 = 'Cpu'
            type_msg2 = ''
        type_msg1 = self.__font.render(type_msg1, True, Constants.RED)
        type_msg2 = self.__font.render(type_msg2, True, Constants.RED)
        surface.blit(type_msg1, (
            self.__xi + self.__msg_w - type_msg1.get_rect().width / 2,
            self.__yi + self.__msg1_h))
        surface.blit(type_msg2, (
            self.__xi + self.__msg_w - type_msg2.get_rect().width / 2,
            self.__yi + self.__msg2_h))

        # Drawing color options
        color_msg = self.__font.render(Constants.colors[self.__color_index],
                                       True, Constants.RED)
        surface.blit(color_msg, (
            self.__xi + self.__msg_w - color_msg.get_rect().width / 2,
            self.__yi + self.__msg3_h))

        # Draws arrows
        if self.__selection == self.__id:
            delta = 3
            if self.__option == Constants.OPTION_TYPE:
                x_r = (self.__xi + self.__msg_w +
                       max(type_msg1.get_rect().width,
                           type_msg2.get_rect().width) / 2 + delta)
                x_l = (self.__xi +
                       self.__msg_w - max(type_msg1.get_rect().width,
                                          type_msg2.get_rect().width) / 2 -
                       self.__left.get_rect().width - delta)
                if self.__type_index != Constants.CPU:
                    y = self.__yi + (self.__msg1_h + self.__msg2_h) / 2
                else:
                    y = self.__yi + self.__msg1_h
            else:
                x_r = (self.__xi + self.__msg_w +
                       color_msg.get_rect().width / 2 + delta)
                x_l = (self.__xi +
                       self.__msg_w - color_msg.get_rect().width / 2 -
                       self.__left.get_rect().width - delta)
                y = self.__yi + self.__msg3_h

            surface.blit(self.__left, (x_l, y))
            surface.blit(self.__right, (x_r, y))

    def update(self, selection):
        """
        Updates the block's animation and buttons.
        :param selection: Current block selected by the user.
        :return: Selection variable updated in case the user has finished
        selecting this block.
        """

        self.__selection = selection
        if selection == self.__id:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYUP:
                    # Handling block switching
                    if event.key == K_RETURN or event.key == K_KP_ENTER:
                        selection += 1
                    elif event.key == K_BACKSPACE:
                        selection -= 1
                    elif event.key == K_ESCAPE:
                        selection = -1

                    # Handling option selection within the block
                    elif event.key == K_RIGHT:
                        if self.__option == Constants.OPTION_TYPE:
                            self.__type_index += 1
                            if self.__type_index == 5:
                                self.__type_index = 0
                        elif self.__option == Constants.OPTION_COLOR:
                            self.__color_index += 1
                            if self.__color_index == len(Constants.colors):
                                self.__color_index = 0
                    elif event.key == K_LEFT:
                        if self.__option == Constants.OPTION_TYPE:
                            self.__type_index -= 1
                            if self.__type_index == -1:
                                self.__type_index = 4
                        elif self.__option == Constants.OPTION_COLOR:
                            self.__color_index -= 1
                            if self.__color_index == -1:
                                self.__color_index = len(Constants.colors) - 1
                    elif event.key == K_DOWN:
                        self.__option += 1
                        if self.__option == 2:
                            self.__option = 1
                    elif event.key == K_UP:
                        self.__option -= 1
                        if self.__option == -1:
                            self.__option = 0

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

        if self.__type_index == Constants.WASD:
            keys = {'up': K_w, 'down': K_s, 'left': K_a,
                    'right': K_d, 'bomb': K_v}
            return Player(pos, self.__sprites[
                Constants.colors[self.__color_index]], keys, self.__id)
        elif self.__type_index == Constants.ARROWS:
            keys = {'up': K_UP, 'down': K_DOWN, 'left': K_LEFT,
                    'right': K_RIGHT, 'bomb': K_SEMICOLON}
            return Player(pos, self.__sprites[
                Constants.colors[self.__color_index]], keys, self.__id)
        elif self.__type_index == Constants.IJKL:
            keys = {'up': K_i, 'down': K_k, 'left': K_j,
                    'right': K_l, 'bomb': K_b}
            return Player(pos, self.__sprites[
                Constants.colors[self.__color_index]], keys, self.__id)
        elif self.__type_index == Constants.CPU:
            return Cpu(pos, self.__sprites[
                Constants.colors[self.__color_index]], self.__id)
        else:
            return None

    def __setup_animations(self):
        """
        Sets up the animations, creating a dict for each type.
        """

        # Not chosen yet
        self.__not_chosed_animation = {}
        for c in Constants.colors:
            s = self.__sprites[c]
            self.__not_chosed_animation[c] = Animation(
                [s['die4'], s['die5'], s['die6']], 0.5 * np.ones(3))

        # Choosing
        self.__choosing_animation = {}
        for c in Constants.colors:
            s = self.__sprites[c]
            self.__choosing_animation[c] = Animation(
                [s['move_down1'], s['move_down2']], 0.3 * np.ones(2))

        # Winning
        self.__chosed_animation = {}
        for c in Constants.colors:
            s = self.__sprites[c]
            self.__chosed_animation[c] = Animation(
                [s['win1'], s['win2'], s['win3']], np.array([0.25, 0.25, 0.5]))

    @staticmethod
    def __rounded_rect(surface, rect, color, radius):
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
                                              [int(
                                                  min(rect.size) * radius)] * 2)

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
