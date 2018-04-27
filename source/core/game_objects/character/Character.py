import numpy as np
import os
import pygame

from source.core.game_objects.GameObject import GameObject
from source.core.ui.Animation import Animation
from source.core.ui.Sprite import Sprite
from source.core.utils import Constants
from source.core.utils.ObjectEvents import CharacterEvents


class Character(GameObject):
    """
    Abstract class for a BomberBoy character.
    """

    def __init__(self, initial_tile, sprite, id):
        """
        Default constructor for the character.
        :param initial_tile: Initial tile coordinates for the character.
        :param sprite: Dict of sprites for this character.
        :param id: Character's id.
        Possibilities: white_bomberboy.
        """

        super().__init__(initial_tile, id)

        self.__sprite = sprite

        self.__speed = Constants.INITIAL_SPEED
        self.__icon = self.__sprite['down']
        self.__placed_bombs = 0
        self.__total_bombs = 1
        self.__fire = Constants.INITIAL_FIRE
        self._event = CharacterEvents.STOP_DOWN
        self._new_event = CharacterEvents.STOP_DOWN
        self._got_special_event = False
        self._just_placed_bomb = False
        self.__is_alive = True

        self.__setup_animations()
        self.__assets_path = (os.path.dirname(os.path.realpath(__file__)) +
                              '/../../../../assets/')

    def update(self, clock, tilemap=None):
        """
        Updates the character according to its intrinsic status.
        :param clock: Pygame.time.Clock object with the game's clock.
        :param tilemap: Numpy array with the map information.
        :return: True if the object still exists.
        """

        # If the dying animation ended, returns False: this character must not
        # be drawed.
        if self.__die_animation.done():
            return False

        # Handles event variables
        previous_event = self._event
        self._event = self._new_event
        if self._got_special_event:
            self._got_special_event = False

        # Finite state machine
        if self._new_event == CharacterEvents.MOVE_UP:
            self.__move((0, -1), clock, tilemap)
        elif self._new_event == CharacterEvents.MOVE_DOWN:
            self.__move((0, 1), clock, tilemap)
        elif self._new_event == CharacterEvents.MOVE_RIGHT:
            self.__move((1, 0), clock, tilemap)
        elif self._new_event == CharacterEvents.MOVE_LEFT:
            self.__move((-1, 0), clock, tilemap)
        elif self._new_event == CharacterEvents.PLACE_BOMB:
            self._just_placed_bomb = True
        elif self._new_event == CharacterEvents.NOTHING:
            if previous_event == CharacterEvents.MOVE_LEFT:
                self._event = CharacterEvents.STOP_LEFT
            elif previous_event == CharacterEvents.MOVE_UP:
                self._event = CharacterEvents.STOP_UP
            elif previous_event == CharacterEvents.MOVE_RIGHT:
                self._event = CharacterEvents.STOP_RIGHT
            elif previous_event == CharacterEvents.MOVE_DOWN:
                self._event = CharacterEvents.STOP_DOWN

        return True

    def draw(self, display):
        """
        Updates the the character icon on the screen, according to its
        animations. Note: This function should be called after update(), and
        only if update() returns True.
        :param display: Pygame display object.
        """

        # Finite state machine
        if self._event == CharacterEvents.MOVE_UP:
            self.__icon = self.__move_up_animation.update()
        elif self._event == CharacterEvents.STOP_UP:
            self.__icon = self.__sprite['up']
        elif self._event == CharacterEvents.MOVE_DOWN:
            self.__icon = self.__move_down_animation.update()
        elif self._event == CharacterEvents.STOP_DOWN:
            self.__icon = self.__sprite['down']
        elif self._event == CharacterEvents.MOVE_LEFT:
            self.__icon = self.__move_left_animation.update()
        elif self._event == CharacterEvents.STOP_LEFT:
            self.__icon = self.__sprite['left']
        elif self._event == CharacterEvents.MOVE_RIGHT:
            self.__icon = self.__move_right_animation.update()
        elif self._event == CharacterEvents.STOP_RIGHT:
            self.__icon = self.__sprite['right']
        elif self._event == CharacterEvents.WIN:
            self.__icon = self.__win_animation.update()
        elif self._event == CharacterEvents.DIE:
            self.__icon = self.__die_animation.update()

        # Positioning the blit according to the icon size
        display.blit(self.__icon, (self._pose.x - self.__icon.get_size()[0] / 2,
                                   self._pose.y + Constants.SQUARE_SIZE / 2 -
                                   self.__icon.get_size()[1] +
                                   Constants.DISPLAY_HEIGTH))

    def placed_bomb(self, map_unit):
        """
        Checks if the character placed a bomb.
        :param map_unit Current player tile's map unit.
        :return: True if the character just placed a bomb.
        """

        if (self._just_placed_bomb and self.__placed_bombs < self.__total_bombs
                and map_unit != Constants.UNIT_BOMB):
            self._just_placed_bomb = False
            self.__placed_bombs += 1
            return True
        self._just_placed_bomb = False
        return False

    def bomb_exploded(self):
        """
        Informs the character that one of his bombs exploded, allowing him to
        place another bomb.
        """

        self.__placed_bombs -= 1

    def special_event(self, event):
        """
        Updates the character status given that a special event (win, die)
        occurred.
        :param event: CharacterEvent event id.
        """

        self._new_event = event
        self._got_special_event = True

        if event == CharacterEvents.DIE:
            if self.__is_alive:
                music_path = self.__assets_path + "song/die.wav"
                music = pygame.mixer.Sound(music_path)
                music.play(0)
            self.__is_alive = False
        elif event == CharacterEvents.WIN:
            music_path = self.__assets_path + "song/win.wav"
            music = pygame.mixer.Sound(music_path)
            music.play(0)

    def increase_speed(self):
        """
        Increases the character's speed.
        """

        self.__speed += Constants.SPEED_INCREMENT

        if self.__speed > Constants.MAX_SPEED:
            self.__speed = Constants.MAX_SPEED

        step_frequency = Constants.STEPS_PER_SQUARE * (
                Constants.INITIAL_SPEED + self.__speed / Constants.MAX_SPEED)
        self.__move_up_animation.set_durations(
            np.ones(2) / step_frequency)
        self.__move_down_animation.set_durations(
            np.ones(2) / step_frequency)
        self.__move_right_animation.set_durations(
            np.ones(2) / step_frequency)
        self.__move_left_animation.set_durations(
            np.ones(2) / step_frequency)

        music_path = self.__assets_path + "song/powerup_shoe.wav"
        music = pygame.mixer.Sound(music_path)
        music.play(0)

    def increase_fire(self):
        """
        Increases the character's fire range.
        """

        self.__fire += Constants.FIRE_INCREMENT

        music_path = self.__assets_path + "song/powerup_fire.wav"
        music = pygame.mixer.Sound(music_path)
        music.play(0)

    def increase_bomb(self):
        """
        Increases the character's maximum bomb limit.
        """

        self.__total_bombs += 1

        music_path = self.__assets_path + "song/powerup_bomb.wav"
        music = pygame.mixer.Sound(music_path)
        music.play(0)

    @property
    def tile(self):
        """
        Getter for the character's tile coordinate on the map.
        :return: Character's coordinate.
        """

        return (int((self._pose.y + self.__icon.get_size()[1] - 3 *
                     Constants.SQUARE_SIZE / 2 - 1) / Constants.SQUARE_SIZE),
                int(self._pose.x / Constants.SQUARE_SIZE))

    def set_tile(self, tile):
        """
        Setter for the character's tile.
        :param tile: Tuple of ints with the character's tile.
        """

        self._pose.x = tile[1] * Constants.SQUARE_SIZE
        self._pose.y = (tile[0] * Constants.SQUARE_SIZE -
                        self.__icon.get_size()[1] + 1.5 * Constants.SQUARE_SIZE
                        + 1)


    @property
    def fire_range(self):
        """
        Getter for the character's fire range in tiles.
        :return: Character's fire range.
        """

        return self.__fire

    @property
    def is_alive(self):
        """
        Getter for the character alive status.
        :return: True if the character is still alive.
        """

        return self.__is_alive

    def __setup_animations(self):
        """
        Sets up the character animations, creating an object for each one.
        """

        # Movements
        step_frequency = self.__speed * Constants.STEPS_PER_SQUARE
        self.__move_up_animation = Animation(
            [self.__sprite['move_up1'], self.__sprite['move_up2']],
            np.ones(2) / step_frequency)
        self.__move_down_animation = Animation(
            [self.__sprite['move_down1'], self.__sprite['move_down2']],
            1 / (self.__speed * Constants.STEPS_PER_SQUARE * np.ones(2)))
        self.__move_right_animation = Animation(
            [self.__sprite['move_right1'], self.__sprite['move_right2']],
            1 / (self.__speed * Constants.STEPS_PER_SQUARE * np.ones(2)))
        self.__move_left_animation = Animation(
            [self.__sprite['move_left1'], self.__sprite['move_left2']],
            1 / (self.__speed * Constants.STEPS_PER_SQUARE * np.ones(2)))

        # Winning
        self.__win_animation = Animation([
            self.__sprite['win1'], self.__sprite['win2'],
            self.__sprite['win3']], np.array([0.25, 0.25, 0.5]))

        # Dying: The character spins 5 times than falls on the ground.
        die_sprites = np.concatenate([np.tile(
            [self.__sprite['die_down'], self.__sprite['die_right'],
             self.__sprite['die_up'], self.__sprite['die_left']], 5),
            [self.__sprite['die_down'],
             self.__sprite['die1'], self.__sprite['die1'],
             self.__sprite['die3'], self.__sprite['die4'],
             self.__sprite['die5'], self.__sprite['die6']]])
        die_durations = np.concatenate([np.tile(0.1, 20), 0.5 * np.ones(7)])
        self.__die_animation = Animation(die_sprites, die_durations, stop=True)

    def __move(self, direction, clock, tilemap):
        """
        Moves the character according to obstacles.
        :param direction: Tuple with x and y directions.
        :param tilemap: Numpy array with the map information.
        """

        # Auxiliar variables
        sq = Constants.SQUARE_SIZE
        obstacles = np.array([Constants.UNIT_BLOCK, Constants.UNIT_FIXED_BLOCK,
                              Constants.UNIT_POWERUP_FIRE_HIDE,
                              Constants.UNIT_POWERUP_VELOCITY_HIDE,
                              Constants.UNIT_POWERUP_BOMB_HIDE,
                              Constants.UNIT_DESTROYING_BLOCK])
        bomb = Constants.UNIT_BOMB

        x = self._pose.x
        x_tile = int(x / sq)

        # Choosing most natural movement upwards according to blocked blocks
        y = self._pose.y + sq / 2 - 2
        y_tile = int(y / sq)
        if self._event == CharacterEvents.MOVE_UP:
            if not np.any(obstacles == tilemap[y_tile - 1, x_tile]) and (
                    tilemap[y_tile - 1, x_tile] != bomb or
                    tilemap[self.tile] == bomb):
                if sq * 0.35 < x % sq < sq * 0.65:
                    self._pose.x = (x_tile + 0.5) * sq
                elif x % sq <= sq * 0.35:
                    direction = (1, 0)
                    self._event = CharacterEvents.MOVE_RIGHT
                else:
                    direction = (-1, 0)
                    self._event = CharacterEvents.MOVE_LEFT
            elif (not np.any(obstacles == tilemap[y_tile - 1, x_tile - 1]) and
                  0 < x % sq < sq / 4 and (tilemap[y_tile - 1, x_tile - 1] !=
                                           bomb or tilemap[self.tile] == bomb)):
                direction = (-1, 0)
                self._event = CharacterEvents.MOVE_LEFT
            elif (not np.any(obstacles == tilemap[y_tile - 1, x_tile + 1]) and
                  3 * sq / 4 < x % sq < sq and (
                          tilemap[y_tile - 1, x_tile + 1] != bomb or
                          tilemap[self.tile] == bomb)):
                direction = (1, 0)
                self._event = CharacterEvents.MOVE_RIGHT
            else:
                direction = (0, 0)
                self._event = CharacterEvents.STOP_UP

        # Choosing most natural movement downwards according to blocked blocks
        y = self._pose.y - sq / 2
        y_tile = int(y / sq)
        if self._event == CharacterEvents.MOVE_DOWN:
            if not np.any(obstacles == tilemap[y_tile + 1, x_tile]) and (
                    tilemap[y_tile + 1, x_tile] != bomb or
                    tilemap[self.tile] == bomb):
                if sq * 0.35 < x % sq < sq * 0.65:
                    self._pose.x = (x_tile + 0.5) * sq
                elif x % sq <= sq * 0.35:
                    direction = (1, 0)
                    self._event = CharacterEvents.MOVE_RIGHT
                else:
                    direction = (-1, 0)
                    self._event = CharacterEvents.MOVE_LEFT
            elif (not np.any(obstacles == tilemap[y_tile + 1, x_tile - 1]) and
                  0 <= x % sq < sq / 4 and (
                          tilemap[y_tile + 1, x_tile - 1] != bomb or
                          tilemap[self.tile] == bomb)):
                direction = (-1, 0)
                self._event = CharacterEvents.MOVE_LEFT
            elif (not np.any(obstacles == tilemap[y_tile + 1, x_tile + 1]) and
                  3 * sq / 4 < x % sq < sq and (
                          tilemap[y_tile + 1, x_tile + 1] != bomb or
                          tilemap[self.tile] == bomb)):
                direction = (1, 0)
                self._event = CharacterEvents.MOVE_RIGHT
            else:
                direction = (0, 0)
                self._event = CharacterEvents.STOP_DOWN

        y = self._pose.y
        y_tile = int(y / sq)

        # Choosing most natural movement rightwards according to blocked blocks
        x = self._pose.x - sq / 2
        x_tile = int(x / sq)
        if self._event == CharacterEvents.MOVE_RIGHT:
            if not np.any(obstacles == tilemap[y_tile, x_tile + 1]) and (
                    tilemap[y_tile, x_tile + 1] != bomb or
                    tilemap[self.tile] == bomb):
                if sq * 0.35 < y % sq < sq * 0.65:
                    self._pose.y = (y_tile + 0.5) * sq
                elif y % sq <= sq * 0.35:
                    direction = (0, 1)
                    self._event = CharacterEvents.MOVE_DOWN
                else:
                    direction = (0, -1)
                    self._event = CharacterEvents.MOVE_UP
            elif (not np.any(obstacles == tilemap[y_tile - 1, x_tile + 1]) and
                  0 <= y % sq < sq / 4 and (
                          tilemap[y_tile - 1, x_tile + 1] != bomb or
                          tilemap[self.tile] == bomb)):
                direction = (0, -1)
                self._event = CharacterEvents.MOVE_UP
            elif (not np.any(obstacles == tilemap[y_tile + 1, x_tile + 1]) and
                  3 * sq / 4 < y % sq < sq and (
                          tilemap[y_tile + 1, x_tile + 1] != bomb or
                          tilemap[self.tile] == bomb)):
                direction = (0, 1)
                self._event = CharacterEvents.MOVE_DOWN
            else:
                direction = (0, 0)
                self._event = CharacterEvents.STOP_RIGHT

        # Choosing most natural movement leftwards according to blocked blocks
        x = self._pose.x + sq / 2 - 2
        x_tile = int(x / sq)
        if self._event == CharacterEvents.MOVE_LEFT:
            if not np.any(obstacles == tilemap[y_tile, x_tile - 1]) and (
                    tilemap[y_tile, x_tile - 1] != bomb or
                    tilemap[self.tile] == bomb):
                if sq * 0.35 < y % sq < sq * 0.65:
                    self._pose.y = (y_tile + 0.5) * sq
                elif y % sq <= sq * 0.35:
                    direction = (0, 1)
                    self._event = CharacterEvents.MOVE_DOWN
                else:
                    direction = (0, -1)
                    self._event = CharacterEvents.MOVE_UP
            elif (not np.any(obstacles == tilemap[y_tile - 1, x_tile - 1]) and
                  0 <= y % sq < sq / 4 and (
                          tilemap[y_tile - 1, x_tile - 1] != bomb or
                          tilemap[self.tile] == bomb)):
                direction = (0, -1)
                self._event = CharacterEvents.MOVE_UP
            elif (not np.any(obstacles == tilemap[y_tile + 1, x_tile - 1]) and
                  3 * sq / 4 < y % sq < sq and (
                          tilemap[y_tile + 1, x_tile - 1] != bomb or
                          tilemap[self.tile] == bomb)):
                direction = (0, 1)
                self._event = CharacterEvents.MOVE_DOWN
            else:
                direction = (0, 0)
                self._event = CharacterEvents.STOP_LEFT

        # Walking towards best direction
        if clock.get_fps() != 0:
            self._pose.x += (direction[0] * self.__speed *
                             Constants.SQUARE_SIZE / clock.get_fps())
            self._pose.y += (direction[1] * self.__speed *
                             Constants.SQUARE_SIZE / clock.get_fps())
