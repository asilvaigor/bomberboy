import pygame
import time
import sys
import os
from pygame.locals import *

from source.core.game_objects.Bomb.Bomb import Bomb
from source.core.game_objects.Bomb.Fire import Fire
from source.core.game_objects.character.Player import Player
from source.core.ui.Map import Map
from source.core.utils import Constants
from source.core.utils.ObjectEvents import CharacterEvents
from source.core.ui.Pause import Pause
from source.core.utils.Constants import *


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
        self.__fires = list()

        self.__initial_time = time.time()
        self.__pause = Pause()

    def play(self, clock, surface, state):
        self.__map.draw(self.__initial_time, surface)

        if state == PAUSE:
            self.__pause.draw(surface)

        # Checking for keyboard events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYUP:
                if event.key == K_BACKSPACE:
                    return Constants.MENU
                elif event.key == K_ESCAPE:
                    if state == PAUSE:
                        return PLAYING_SINGLE
                    else:
                        self.__pause.draw(surface)
                        return self.__pause.update()
                else:
                    self.__player.key_up(event.key)

            if event.type == KEYDOWN:
                # If placing bomb, check if character can place bomb and if
                # there is not another bomb already in this tile.
                if (event.key == self.__player1_keys['bomb'] and
                        self.__player.place_bomb()):
                    if self.__map.get_grid().get_tilemap()[
                           self.__player.tile] != Constants.UNIT_BOMB:
                        self.__bombs.append(Bomb(self.__player.tile,
                                                 self.__player.fire_range))
                    else:
                        self.__player.bomb_exploded()
                else:
                    self.__player.key_down(event.key)

        # Updates and draws bombs
        for bomb in self.__bombs:
            if bomb.update(clock, self.__map.get_grid().get_tilemap()):
                bomb.draw(surface)
            else:
                self.__fires.append(Fire(bomb.tile, bomb.range))
                self.__player.bomb_exploded()
                self.__bombs.remove(bomb)

        # Updates and draws fires
        for fire in self.__fires:
            if fire.update(clock, self.__map.get_grid().get_tilemap()):
                fire.draw(surface)
            else:
                self.__fires.remove(fire)

        # Updates and draws character
        if self.__player.update(clock, self.__map.get_grid().get_tilemap()):
            # TODO: Improve fire collision.
            if (self.__map.get_grid().get_tilemap()[self.__player.tile] ==
                    Constants.UNIT_FIRE):
                self.__player.special_event(CharacterEvents.DIE)
            self.__player.draw(surface)

        if state != PAUSE:
            return Constants.PLAYING_SINGLE
        return PAUSE
