import numpy as np
import pygame
import time
import sys
import os
from pygame.locals import *

from source.core.game_objects.bomb.Bomb import Bomb
from source.core.game_objects.bomb.Fire import Fire
from source.core.ui.Map import Map
from source.core.utils import Constants
from source.core.utils.ObjectEvents import CharacterEvents
from source.core.ui.Pause import Pause
from source.core.ui.GameOver import GameOver
from source.core.utils.Constants import *


class Match:

    def __init__(self, characters, sprites):
        assets_path = (os.path.dirname(os.path.realpath(__file__)) +
                       '/../../../assets/')
        self.__menu_font = pygame.font.Font(assets_path + "font/04B_30__.TTF",
                                            Constants.FONT_SIZE)

        self.__map = Map(time.time())
        self.__players = characters[0]
        self.__cpus = characters[1]
        self.__bombs = list()
        self.__fires = list()
        self.__sprites = sprites
        self.__alive_characters = False * np.ones(4)
        for player in self.__players:
            self.__alive_characters[player.id] = True
        for cpu in self.__cpus:
            self.__alive_characters[cpu.id] = True

        self.__game_state = IN_GAME

        self.__pause = None
        self.__game_over = None
        self.__time_pause = 0

    def play(self, clock, surface):
        self.__map.draw(surface)
        self.__map.set_is_paused(self.__game_state == PAUSE or
                                 self.__game_state == OVER)

        if self.__game_state == PAUSE:
            if not self.__pause:  # Verify that the pointer is null
                self.__time_pause = time.time()
                self.__pause = Pause()

            self.__pause.draw(surface)
            state = self.__pause.update()
            if state == IN_GAME:
                self.__game_state = IN_GAME
            elif state == MAIN_MENU:
                return MENU

        elif self.__game_state == OVER:
            if not self.__game_over:
                self.__game_over = GameOver()

            # Updates bombs animations
            for bomb in self.__bombs:
                if bomb.update(clock, self.__map.get_grid().get_tilemap()):
                    bomb.draw(surface)

            # Updates fire animations
            for fire in self.__fires:
                if fire.update(clock, self.__map.get_grid().get_tilemap()):
                    fire.draw(surface)

            # Updates character animations
            for player in self.__players:
                self.__update_character(player, clock, surface)
            for cpu in self.__cpus:
                self.__update_character(cpu, clock, surface)

            self.__game_over.draw(surface)
            if self.__game_over.update() == MAIN_MENU:
                return MENU

        elif self.__game_state == IN_GAME:
            if self.__pause:  # Verify that the pointer is null
                self.__map.increment_delta_pause(
                    time.time() - self.__time_pause)
                del self.__pause
                self.__pause = None

            # Checking for keyboard events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        self.__game_state = PAUSE
                    else:
                        for player in self.__players:
                            player.key_up(event.key)

                if event.type == KEYDOWN:
                    for player in self.__players:
                        player.key_down(event.key)

            # Decides IA's moves
            for cpu in self.__cpus:
                cpu.decide(self.__map.get_grid().get_tilemap(),
                           self.__players + self.__cpus)

            # Updates and draws bombs
            for bomb in self.__bombs:
                if bomb.update(clock, self.__map.get_grid().get_tilemap()):
                    bomb.draw(surface)
                else:
                    self.__fires.append(Fire(bomb.tile, bomb.range,
                                             self.__sprites['fire']))
                    for player in self.__players:
                        if player.id == bomb.character_id:
                            player.bomb_exploded()
                    for cpu in self.__cpus:
                        if cpu.id == bomb.character_id:
                            cpu.bomb_exploded()
                    self.__bombs.remove(bomb)

            # Updates and draws fires
            for fire in self.__fires:
                if fire.update(clock, self.__map.get_grid().get_tilemap()):
                    fire.draw(surface)
                    for tile in fire.get_triggered_bombs():
                        for bomb in self.__bombs:
                            if bomb.tile == tile:
                                bomb.explode()
                else:
                    self.__fires.remove(fire)

            # Updates and draws characters
            for player in self.__players:
                if not self.__update_character(player, clock, surface):
                    self.__alive_characters[player.id] = False
            for cpu in self.__cpus:
                if not self.__update_character(cpu, clock, surface):
                    self.__alive_characters[cpu.id] = False

            if np.count_nonzero(self.__alive_characters) == 0:
                self.__game_state = OVER
            elif np.count_nonzero(self.__alive_characters) == 1:
                for id in range(len(self.__alive_characters)):
                    if self.__alive_characters[id]:
                        for player in self.__players:
                            if player.id == id:
                                player.special_event(CharacterEvents.WIN)
                        for cpu in self.__cpus:
                            if cpu.id == id:
                                cpu.special_event(CharacterEvents.WIN)
                self.__game_state = OVER

        return PLAYING

    def __update_character(self, character, clock, surface):
        """
        Updates and draws a character according to the map and its events.
        :param character: Character to be updated.
        :param clock: Match clock.
        :param surface: Drawing surface.
        :return: True if the character is still alive.
        """

        if character.update(clock, self.__map.get_grid().get_tilemap()):
            # Check if character died
            if (self.__map.get_grid().get_tilemap()[character.tile] ==
                    Constants.UNIT_FIRE or
                    self.__map.get_grid().get_tilemap()[character.tile] ==
                    Constants.UNIT_CENTER_FIRE):
                character.special_event(CharacterEvents.DIE)
                character.draw(surface)
                return False
            # Check if character picked up a powerup
            elif (self.__map.get_grid().get_tilemap()[character.tile] ==
                  Constants.UNIT_POWERUP_BOMB_SHOW):
                character.increase_bomb()
                self.__map.get_grid().get_tilemap()[character.tile] = (
                    Constants.UNIT_EMPTY)
            elif (self.__map.get_grid().get_tilemap()[
                      character.tile] ==
                  Constants.UNIT_POWERUP_FIRE_SHOW):
                character.increase_fire()
                self.__map.get_grid().get_tilemap()[character.tile] = (
                    Constants.UNIT_EMPTY)
            elif (self.__map.get_grid().get_tilemap()[character.tile] ==
                  Constants.UNIT_POWERUP_VELOCITY_SHOW):
                character.increase_speed()
                self.__map.get_grid().get_tilemap()[character.tile] = (
                    Constants.UNIT_EMPTY)
            # Check if character placed a bomb
            elif character.placed_bomb(self.__map.get_grid().get_tilemap()[
                                           character.tile]):
                self.__bombs.append(Bomb(character.tile, character.fire_range,
                                         character.id, self.__sprites['bomb']))

            character.draw(surface)
            return True

        return False
