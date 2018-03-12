import numpy as np

from source.core.game_objects.GameObject import GameObject
from source.core.ui.Animation import Animation
from source.core.utils import Constants
from source.core.utils.ObjectEvents import CharacterEvents


class Character(GameObject):
    """
    Abstract class for a BomberBoy character.
    """

    def __init__(self, initial_tile, sprite_name):
        """
        Default constructor for the character.
        :param initial_tile: Initial tile coordinates for the character.
        :param sprite_name: String to select the character sprite.
        Possibilities: white_bomberboy.
        """

        super().__init__(initial_tile, sprite_name)

        self.__speed = Constants.INITIAL_SPEED
        self.__icon = self._sprite['down']
        self.__placed_bombs = 0
        self.__total_bombs = 1
        self.__fire = Constants.INITIAL_FIRE
        self.__event = CharacterEvents.STOP_DOWN

        self.__setup_animations()

    def update(self, event, clock, tilemap=None):
        """
        Updates the character according to a CharacterEvent given by the engine.
        :param event: CharacterEvent informing what the character must do.
        :param clock: Pygame.time.Clock object with the game's clock.
        :param tilemap: Numpy array with the map information.
        :return: True if the object still exists.
        """

        if self.__die_animation.done():
            return False

        if event == CharacterEvents.MOVE_UP:
            self.__move((0, -1), clock, tilemap)
        elif event == CharacterEvents.MOVE_DOWN:
            self.__move((0, 1), clock, tilemap)
        elif event == CharacterEvents.MOVE_RIGHT:
            self.__move((1, 0), clock, tilemap)
        elif event == CharacterEvents.MOVE_LEFT:
            self.__move((-1, 0), clock, tilemap)
        elif event == CharacterEvents.INCREASE_SPEED:
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
        elif event == CharacterEvents.INCREASE_BOMB:
            self.__total_bombs += 1
        elif event == CharacterEvents.INCREASE_FIRE:
            self.__fire += Constants.FIRE_INCREMENT

        self.__event = event

        return True

    def draw(self, display):
        """
        Updates the the character icon on the screen, according to its
        animations.
        :param display: Pygame display object.
        """

        if self.__event == CharacterEvents.MOVE_UP:
            self.__icon = self.__move_up_animation.update()
        elif self.__event == CharacterEvents.STOP_UP:
            self.__icon = self._sprite['up']
        elif self.__event == CharacterEvents.MOVE_DOWN:
            self.__icon = self.__move_down_animation.update()
        elif self.__event == CharacterEvents.STOP_DOWN:
            self.__icon = self._sprite['down']
        elif self.__event == CharacterEvents.MOVE_LEFT:
            self.__icon = self.__move_left_animation.update()
        elif self.__event == CharacterEvents.STOP_LEFT:
            self.__icon = self._sprite['left']
        elif self.__event == CharacterEvents.MOVE_RIGHT:
            self.__icon = self.__move_right_animation.update()
        elif self.__event == CharacterEvents.STOP_RIGHT:
            self.__icon = self._sprite['right']
        elif self.__event == CharacterEvents.WIN:
            self.__icon = self.__win_animation.update()
        elif self.__event == CharacterEvents.DIE:
            self.__icon = self.__die_animation.update()

        display.blit(self.__icon, (self._pose.x - 0.5 * Constants.SQUARE_SIZE,
                                   self._pose.y - Constants.SQUARE_SIZE))

    def place_bomb(self):
        """
        Tries placing a bomb.
        :return: True if it was successful.
        """

        if self.__placed_bombs < self.__total_bombs:
            self.__placed_bombs += 1
            return True
        else:
            return False

    def bomb_exploded(self):
        """
        Informs the character that one of his bombs exploded, allowing him to
        place another bomb.
        """

        self.__placed_bombs -= 1

    def __setup_animations(self):
        """
        Sets up the character animations, creating an object for each one.
        """

        # Movements
        step_frequency = self.__speed * Constants.STEPS_PER_SQUARE
        self.__move_up_animation = Animation(
            [self._sprite['move_up1'], self._sprite['move_up2']],
            np.ones(2) / step_frequency)
        self.__move_down_animation = Animation(
            [self._sprite['move_down1'], self._sprite['move_down2']],
            1 / (self.__speed * Constants.STEPS_PER_SQUARE * np.ones(2)))
        self.__move_right_animation = Animation(
            [self._sprite['move_right1'], self._sprite['move_right2']],
            1 / (self.__speed * Constants.STEPS_PER_SQUARE * np.ones(2)))
        self.__move_left_animation = Animation(
            [self._sprite['move_left1'], self._sprite['move_left2']],
            1 / (self.__speed * Constants.STEPS_PER_SQUARE * np.ones(2)))

        # Winning
        self.__win_animation = Animation([
            self._sprite['win1'], self._sprite['win2'],
            self._sprite['win3']], np.array([0.25, 0.25, 0.5]))

        # Dying: The character spins 5 times than falls on the ground.
        die_sprites = np.concatenate([np.tile(
            [self._sprite['die_down'], self._sprite['die_right'],
             self._sprite['die_up'], self._sprite['die_left']], 5),
            [self._sprite['die_down'],
             self._sprite['die1'], self._sprite['die1'],
             self._sprite['die3'], self._sprite['die4'],
             self._sprite['die5'], self._sprite['die6']]])
        die_durations = np.concatenate([np.tile(0.1, 20),
                                        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]])
        self.__die_animation = Animation(die_sprites, die_durations, stop=True)

    def __move(self, direction, clock, tilemap):
        """
        Moves the character according to obstacles.
        :param direction: Tuple with x and y directions.
        :param tilemap: Numpy array with the map information.
        """

        self._pose.x += (direction[0] * self.__speed *
                         Constants.SQUARE_SIZE / clock.get_fps())
        self._pose.y += (direction[1] * self.__speed *
                         Constants.SQUARE_SIZE / clock.get_fps())

        # TODO
        # horiz_free = (math.floor(self._pose.y) + 0.333 < self._pose.y <
        #               math.ceil(self._pose.y) - 0.333)
        # vert_free = (math.floor(self._pose.x) + 0.333 < self._pose.x <
        #              math.ceil(self._pose.x) - 0.333)
