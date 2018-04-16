from pygame.locals import *
import os
import pygame
import sys

from source.core.game_objects.character.Player import Player
from source.core.utils import Constants
from source.core.ui.CharacterSelection import CharacterSelection


class Setup:
    """
    Class handles the 4 character selections blocks.
    """

    def __init__(self):
        """
        Default constructor. It creates 4 character selection blocks and a play
        button.
        """

        # Creating play button and arrows
        assets_path = (os.path.dirname(os.path.realpath(__file__)) +
                       '/../../../assets/')
        font_size = int(1.5 * Constants.FONT_SIZE)
        font = pygame.font.Font(assets_path + "font/04B_30__.TTF", font_size)
        self.__play_msg = font.render("Play", True, Constants.RED)
        self.__right = pygame.image.load(assets_path + "image/right_arrow.png")
        self.__left = pygame.image.load(assets_path + "image/left_arrow.png")
        arrow_size = (font_size, font_size)
        self.__right = pygame.transform.scale(self.__right, arrow_size)
        self.__left = pygame.transform.scale(self.__left, arrow_size)

        # Creating character selection blocks
        self.__c1_selection = CharacterSelection(
            0, 0, 0, Constants.WINDOW_WIDTH / 2, Constants.WINDOW_HEIGHT / 3)
        self.__c2_selection = CharacterSelection(
            1, Constants.WINDOW_WIDTH / 2, 0,
            Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT / 3)
        self.__c3_selection = CharacterSelection(
            2, 0, Constants.WINDOW_HEIGHT / 3,
                  Constants.WINDOW_WIDTH / 2, 2 * Constants.WINDOW_HEIGHT / 3)
        self.__c4_selection = CharacterSelection(
            3, Constants.WINDOW_WIDTH / 2, Constants.WINDOW_HEIGHT / 3,
            Constants.WINDOW_WIDTH, 2 * Constants.WINDOW_HEIGHT / 3)

        # Variable which controls which block is currently selected
        self.__selection = 0

    def draw(self, surface):
        """
        Draws blocks and play button on screen.
        :param surface: Pygame surface.
        """

        # Background
        surface.fill(Constants.BLUE)

        # Each selection block
        self.__c1_selection.draw(surface)
        self.__c2_selection.draw(surface)
        self.__c3_selection.draw(surface)
        self.__c4_selection.draw(surface)

        # Draws button and arrows, if necessary
        y = int(Constants.WINDOW_HEIGHT * 0.8)
        surface.blit(self.__play_msg, (
            Constants.WINDOW_WIDTH / 2 - self.__play_msg.get_rect().centerx, y))

        if self.__selection == 4:
            x_r = (Constants.WINDOW_WIDTH / 2 -
                   self.__play_msg.get_rect().centerx -
                   3 * self.__right.get_rect().centerx)
            x_l = (Constants.WINDOW_WIDTH / 2 +
                   self.__play_msg.get_rect().centerx +
                   self.__right.get_rect().centerx)
            surface.blit(self.__right, (x_r, y))
            surface.blit(self.__left, (x_l, y))

    def update(self):
        """
        Updates each selection block and the game mode.
        :return: Game mode used to update the engine.
        """

        # Updates character selection blocks
        self.__selection = self.__c1_selection.update(self.__selection)
        self.__selection = self.__c2_selection.update(self.__selection)
        self.__selection = self.__c3_selection.update(self.__selection)
        self.__selection = self.__c4_selection.update(self.__selection)

        # Returns to menu
        if self.__selection == -1:
            return Constants.MENU
        # Updates play button
        elif self.__selection == 4:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYUP:
                    if event.key == K_RETURN or event.key == K_KP_ENTER:
                        return Constants.PLAYING
                    elif event.key == K_BACKSPACE:
                        self.__selection -= 1

        return Constants.SETUP

    def get_characters(self):
        """
        Getter for the lists of players and cpus that will be on the match, and
        were decided by the character selection blocks.
        :return: Tuple with list of players and list of cpus on the match.
        """

        characters = list()
        players = list()
        cpus = list()

        characters.append(self.__c1_selection.get_character())
        characters.append(self.__c2_selection.get_character())
        characters.append(self.__c3_selection.get_character())
        characters.append(self.__c4_selection.get_character())

        for c in characters:
            if c is not None:
                if isinstance(c, Player):
                    players.append(c)
                else:
                    cpus.append(c)

        return players, cpus
