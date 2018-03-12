import numpy as np

from source.core.game_objects.GameObject import GameObject
from source.core.ui.Animation import Animation
from source.core.utils import Constants
from source.core.utils.ObjectEvents import CharacterEvents


class Character(GameObject):
    """
    Abstract class for a BomberBoy character.
    """

    def __init__(self, pose, sprite_name):
        """
        Default constructor for the character.
        :param pose: Initial pose for the character.
        :param sprite_name: String to select the character sprite.
        Possibilities: white_bomberboy.
        """

        super().__init__(pose, sprite_name)

        self.__speed = Constants.INITIAL_SPEED
        self.__icon = self.__sprite['down']
        self.__placed_bombs = 0
        self.__total_bombs = 1
        self.__fire = Constants.INITIAL_FIRE

        self.__setup_animations()

    def update(self, event, tilemap=None):
        """
        Updates the character according to a CharacterEvent given by the engine.
        :param event: CharacterEvent informing what the character must do.
        :param tilemap: Numpy array with the map information.
        :return: True if the object still exists.
        """

        if self.__die_animation.done():
            return False

        if event == CharacterEvents.MOVE_UP:
            self.__move((0, -1), tilemap)
        elif event == CharacterEvents.MOVE_DOWN:
            self.__move((0, 1), tilemap)
        elif event == CharacterEvents.MOVE_RIGHT:
            self.__move((1, 0), tilemap)
        elif event == CharacterEvents.MOVE_LEFT:
            self.__move((-1, 0), tilemap)
        elif event == CharacterEvents.INCREASE_SPEED:
            self.__speed += Constants.SPEED_INCREMENT
            if self.__speed > Constants.MAX_SPEED:
                self.__speed = Constants.MAX_SPEED
        elif event == CharacterEvents.INCREASE_BOMB:
            self.__total_bombs += 1
        elif event == CharacterEvents.INCREASE_FIRE:
            self.__fire += Constants.FIRE_INCREMENT

        return True

    def draw(self, event, display):
        """
        Updates the the character icon on the screen, according to its
        animations.
        :param event: CharacterEvents informing what the character must do.
        :param display: Pygame display object.
        """

        if event == CharacterEvents.MOVE_UP:
            self.__icon = self.__move_up_animation.update()
        elif event == CharacterEvents.STOP_UP:
            self.__icon = self.__sprite['up']
        elif event == CharacterEvents.MOVE_DOWN:
            self.__icon = self.__move_down_animation.update()
        elif event == CharacterEvents.STOP_DOWN:
            self.__icon = self.__sprite['down']
        elif event == CharacterEvents.MOVE_LEFT:
            self.__icon = self.__move_left_animation.update()
        elif event == CharacterEvents.STOP_LEFT:
            self.__icon = self.__sprite['left']
        elif event == CharacterEvents.MOVE_RIGHT:
            self.__icon = self.__move_right_animation.update()
        elif event == CharacterEvents.STOP_RIGHT:
            self.__icon = self.__sprite['right']
        elif event == CharacterEvents.WIN:
            self.__icon = self.__win_animation.update()
        elif event == CharacterEvents.DIE:
            self.__icon = self.__die_animation.update()

        display.blit(self.__icon, (self._pose.x - 0.5, self._pose.y - 0.5))

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
        self.__move_up_animation = Animation(
            [self.__sprite['move_up1'], self.__sprite['move_up2']],
            self.__speed * Constants.STEPS_PER_SQUARE * np.ones(2))
        self.__move_down_animation = Animation(
            [self.__sprite['move_down1'], self.__sprite['move_down2']],
            self.__speed * Constants.STEPS_PER_SQUARE * np.ones(2))
        self.__move_right_animation = Animation(
            [self.__sprite['move_right1'], self.__sprite['move_right2']],
            self.__speed * Constants.STEPS_PER_SQUARE * np.ones(2))
        self.__move_left_animation = Animation(
            [self.__sprite['move_left1'], self.__sprite['move_left2']],
            self.__speed * Constants.STEPS_PER_SQUARE * np.ones(2))

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
        die_durations = np.concatenate([np.tile(0.1, 20),
                                        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]])
        self.__die_animation = Animation(die_sprites, die_durations, stop=True)

    def __move(self, direction, tilemap):
        """
        Moves the character according to obstacles.
        :param direction: Tuple with x and y directions.
        :param tilemap: Numpy array with the map information.
        """

        self._pose.x += (direction[0] * self.__speed *
                         Constants.SQUARE_SIZE / Constants.FPS)
        self._pose.y += (direction[1] * self.__speed *
                         Constants.SQUARE_SIZE / Constants.FPS)

        # TODO
        # horiz_free = (math.floor(self._pose.y) + 0.333 < self._pose.y <
        #               math.ceil(self._pose.y) - 0.333)
        # vert_free = (math.floor(self._pose.x) + 0.333 < self._pose.x <
        #              math.ceil(self._pose.x) - 0.333)
