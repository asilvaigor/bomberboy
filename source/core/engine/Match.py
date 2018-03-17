import pygame
import sys
import os
from pygame.locals import *

from source.core.game_objects.Bomb.Bomb import Bomb
from source.core.game_objects.Character.Player import Player
from source.core.ui.Map import Map
from source.core.utils import Constants


class Match:

    def __init__(self):
        assets_path = (os.path.dirname(os.path.realpath(__file__)) +
                       '/../../../assets/')
        self.__menu_font = pygame.font.Font(assets_path + "font/04B_30__.TTF",
                                            Constants.FONT_SIZE)
        self.__msg = self.__menu_font.render("funcao nao disponivel", True,
                                             Constants.RED)

        self.__map = Map()
        self.__player1_keys = {'up': K_w, 'down': K_s, 'left': K_a,
                               'right': K_d, 'bomb': K_v}
        self.__player = Player((1, 1), 'bomberboy_white', self.__player1_keys)
        self.__bombs = list()

    def play(self, clock, surface):
        self.__map.draw(surface)

        # Checking for keyboard events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYUP:
                if event.key == K_BACKSPACE:
                    return Constants.MENU
                elif event.key == K_ESCAPE:
                    return Constants.PAUSE
                else:
                    self.__player.key_up(event.key)

            if event.type == KEYDOWN:
                # If placing bomb, check if character can place bomb and if
                # there is not another bomb already in this tile.
                if (event.key == self.__player1_keys['bomb'] and
                        self.__player.place_bomb()):
                    if self.__map.get_grid().get_tilemap()[
                           self.__player.tile] != Constants.UNIT_BOMB:
                        self.__bombs.append(Bomb(self.__player.tile))
                        self.__map.get_grid().update(self.__player.tile,
                                                     Constants.UNIT_BOMB)
                    else:
                        self.__player.bomb_exploded()
                else:
                    self.__player.key_down(event.key)

        # Updates and draws bombs
        for bomb in self.__bombs:
            if bomb.update():
                bomb.draw(surface)
            else:
                # TODO: Bomb exploded!
                self.__player.bomb_exploded()
                self.__bombs.remove(bomb)
                self.__map.get_grid().update(bomb.tile, Constants.UNIT_EMPTY)

        # Updates and draws character
        if self.__player.update(clock, self.__map.get_grid().get_tilemap()):
            self.__player.draw(surface)

        return Constants.PLAYING_SINGLE
