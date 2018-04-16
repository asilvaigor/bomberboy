from pygame.locals import *
import sys
import pygame

from source.core.game_objects.character.Player import Player
from source.core.game_objects.character.Cpu import Cpu


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

        pass

    def update(self, selection):
        """
        Updates the block's animation and buttons.
        :param selection: Current block selected by the user.
        :return: Selection variable updated in case the user has finished
        selecting this block.
        """

        if selection == self.__id:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYUP:
                    if event.key == K_RETURN or event.key == K_KP_ENTER:
                        selection += 1
                    elif event.key == K_BACKSPACE:
                        selection -= 1

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
