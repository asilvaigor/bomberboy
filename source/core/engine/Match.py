from pygame.locals import *
import numpy as np
import os
import pygame
import sys
import time

from source.core.game_objects.bomb.Bomb import Bomb
from source.core.game_objects.bomb.Fire import Fire
from source.core.ui.GameOver import GameOver
from source.core.ui.Map import Map
from source.core.ui.Pause import Pause
from source.core.utils import Constants
from source.core.utils.ObjectEvents import CharacterEvents


class Match:
    """
    Class which represents a match. It handles all game objects interactions,
    user inputs and cpu decisions.
    """

    def __init__(self, characters, sprites):
        """
        Default constructor. It assigns initial values to all variables.
        :param characters: Tuple of characters, with the first element being the
        list of players and the second the list of cpus in the match.
        :param sprites: Dict of sprites previously loaded.
        """

        self.__sprites = sprites

        # Loading font
        assets_path = (os.path.dirname(os.path.realpath(__file__)) +
                       '/../../../assets/')
        self.__menu_font = pygame.font.Font(assets_path + "font/04B_30__.TTF",
                                            Constants.FONT_SIZE)

        # Creating map and game objects
        self.__map = Map(time.time())
        self.__players = characters[0]
        self.__cpus = characters[1]
        self.__bombs = list()
        self.__fires = list()

        # Array indicating characters which are still alive
        self.__alive_characters = False * np.ones(4)
        for player in self.__players:
            self.__alive_characters[player.id] = True
        for cpu in self.__cpus:
            self.__alive_characters[cpu.id] = True

        # Handles game pausing and game over
        self.__game_state = Constants.IN_GAME
        self.__pause = None
        self.__game_over = None
        self.__time_pause = 0

    def play(self, clock, surface):
        """
        Match loop, which handles different game states.
        :param clock: Pygame clock object.
        :param surface: Pygame surface object.
        :return: Current state the game is in.
        """

        # Draws map and clock
        self.__map.draw(surface)
        self.__map.set_is_paused(self.__game_state == Constants.PAUSE or
                                 self.__game_state == Constants.OVER)

        # State machine
        if self.__game_state == Constants.PAUSE:
            self.__update_pause_screen(surface)
        elif self.__game_state == Constants.OVER:
            self.__update_game_over_screen(clock, surface)
        elif self.__game_state == Constants.IN_GAME:
            self.__update_match(clock, surface)
        elif self.__game_state == Constants.MAIN_MENU:
            return Constants.STATE_MENU

        return Constants.STATE_PLAYING

    def __update_match(self, clock, surface):
        """
        Updates the match itself, handling game object interactions, player
        inputs and ai decisions.
        :param clock: Pygame clock object.
        :param surface: Pygame surface.
        :return: Match updated state.
        """
        t = time.time()

        # Handles keyboard events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self.__game_state = Constants.PAUSE
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

        # Checks if game is over
        if np.count_nonzero(self.__alive_characters) == 0:
            self.__game_state = Constants.OVER
        elif np.count_nonzero(self.__alive_characters) == 1:
            for i in range(len(self.__alive_characters)):
                if self.__alive_characters[i]:
                    for player in self.__players:
                        if player.id == i:
                            player.special_event(CharacterEvents.WIN)
                    for cpu in self.__cpus:
                        if cpu.id == i:
                            cpu.special_event(CharacterEvents.WIN)
            self.__game_state = Constants.OVER

    def __update_pause_screen(self, surface):
        """
        Handles the paused screen interface and updates game state.
        :param surface: Pygame surface.
        """

        if not self.__pause:
            self.__time_pause = time.time()
            self.__pause = Pause()

        self.__pause.draw(surface)
        self.__game_state = self.__pause.update()

        if self.__game_state == Constants.IN_GAME:
            self.__map.increment_delta_pause(
                time.time() - self.__time_pause)
            del self.__pause
            self.__pause = None

    def __update_game_over_screen(self, clock, surface):
        """
        Handles the game over screen interface and updates game state. It also
        continues the game objects animations already started.
        :param clock: Pygame clock object.
        :param surface: Pygame surface.
        """

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
        self.__game_state = self.__game_over.update()

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
