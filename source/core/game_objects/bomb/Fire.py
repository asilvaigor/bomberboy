import numpy as np
import os

from source.core.game_objects.GameObject import GameObject
from source.core.ui.Animation import Animation
from source.core.ui.Sprite import Sprite
from source.core.utils import Constants


class Fire(GameObject):
    """
    Represents a Fire object.
    """

    destroyable_block = list([Constants.UNIT_BLOCK,
                              Constants.UNIT_DESTROYING_BLOCK])
    powerups_hidden = list([Constants.UNIT_POWERUP_BOMB_HIDE,
                            Constants.UNIT_POWERUP_FIRE_HIDE,
                            Constants.UNIT_POWERUP_VELOCITY_HIDE])
    powerups_showed = list([Constants.UNIT_POWERUP_BOMB_SHOW,
                            Constants.UNIT_POWERUP_FIRE_SHOW,
                            Constants.UNIT_POWERUP_VELOCITY_SHOW,
                            Constants.UNIT_DESTROYING_POWERUP])

    def __init__(self, initial_tile, fire_range, character_id, sprite):
        """
        Default constructor for the character.
        :param initial_tile: Initial tile coordinates for the fire.
        :param fire_range: Fire's range in tile units.
        :param character_id: Id of the character which put the bomb.
        :param sprite: Dict of fire sprites.
        """

        super().__init__(initial_tile, character_id)

        self.__sprite = sprite
        self.__range = fire_range
        self.__reward = 0
        self.__setup_animations()
        self.__up_branch = list()
        self.__down_branch = list()
        self.__left_branch = list()
        self.__right_branch = list()

        self.__destroyed_powerups = list()
        self.__triggered_bombs = list()

    def update(self, clock, tilemap):
        """
        Updates the fire according to its intrinsic status.
        :param clock: Pygame.time.Clock object with the game's clock.
        :param tilemap: Numpy array with the map information.
        :return: True if the fire still exists.
        """

        if self.__middle_animation.done():
            self.__remove_fire(tilemap)
            return False

        # Clearing previous branches
        self.__up_branch.clear()
        self.__down_branch.clear()
        self.__left_branch.clear()
        self.__right_branch.clear()

        # Center tile
        tilemap[self.tile] = Constants.UNIT_CENTER_FIRE

        free = list([Constants.UNIT_EMPTY, Constants.UNIT_FIRE])

        # Up branch
        for i in range(1, self.__range):
            tile = (self.tile[0] - i, self.tile[1])
            if np.any(tilemap[tile] == free):
                tilemap[tile] = Constants.UNIT_FIRE
                if i != self.__range - 1:
                    self.__up_branch.append(self.__up1_animation)
                else:
                    self.__up_branch.append(self.__up2_animation)
            elif tilemap[tile] == Constants.UNIT_BOMB:
                self.__triggered_bombs.append(tile)
                break
            elif tilemap[tile] == Constants.UNIT_CENTER_FIRE:
                break
            else:
                self.__destroy_tile(tile, self.__up_branch, tilemap)
                break

        # Down branch
        for i in range(1, self.__range):
            tile = (self.tile[0] + i, self.tile[1])
            if np.any(tilemap[tile] == free):
                tilemap[tile] = Constants.UNIT_FIRE
                if i != self.__range - 1:
                    self.__down_branch.append(self.__down1_animation)
                else:
                    self.__down_branch.append(self.__down2_animation)
            elif tilemap[tile] == Constants.UNIT_BOMB:
                self.__triggered_bombs.append(tile)
                break
            elif tilemap[tile] == Constants.UNIT_CENTER_FIRE:
                break
            else:
                self.__destroy_tile(tile, self.__down_branch, tilemap)
                break

        # Left branch
        for i in range(1, self.__range):
            tile = (self.tile[0], self.tile[1] - i)
            if np.any(tilemap[tile] == free):
                tilemap[tile] = Constants.UNIT_FIRE
                if i != self.__range - 1:
                    self.__left_branch.append(self.__left1_animation)
                else:
                    self.__left_branch.append(self.__left2_animation)
            elif tilemap[tile] == Constants.UNIT_BOMB:
                self.__triggered_bombs.append(tile)
                break
            elif tilemap[tile] == Constants.UNIT_CENTER_FIRE:
                break
            else:
                self.__destroy_tile(tile, self.__left_branch, tilemap)
                break

        # Right branch
        for i in range(1, self.__range):
            tile = (self.tile[0], self.tile[1] + i)
            if np.any(tilemap[tile] == free):
                tilemap[tile] = Constants.UNIT_FIRE
                if i != self.__range - 1:
                    self.__right_branch.append(self.__right1_animation)
                else:
                    self.__right_branch.append(self.__right2_animation)
            elif tilemap[tile] == Constants.UNIT_BOMB:
                self.__triggered_bombs.append(tile)
                break
            elif tilemap[tile] == Constants.UNIT_CENTER_FIRE:
                break
            else:
                self.__destroy_tile(tile, self.__right_branch, tilemap)
                break

        return True

    def draw(self, display):
        """
        Updates the the bomb's icon on the screen, according to its
        animation. Note: This function should be called after update(), and
        only if update() returns True.
        :param display: Pygame display object.
        """

        icon = self.__middle_animation.update()
        display.blit(icon,
                     (self._pose.x - icon.get_size()[0] / 2,
                      self._pose.y + Constants.SQUARE_SIZE / 2 -
                      icon.get_size()[1] + Constants.DISPLAY_HEIGTH))

        for i in range(len(self.__up_branch)):
            icon = self.__up_branch[i].update()
            display.blit(icon,
                         (self._pose.x - icon.get_size()[0] / 2,
                          self._pose.y - (2 * i + 1) *
                          Constants.SQUARE_SIZE / 2 -
                          icon.get_size()[1] + Constants.DISPLAY_HEIGTH))

        for i in range(len(self.__down_branch)):
            icon = self.__down_branch[i].update()
            display.blit(icon,
                         (self._pose.x - icon.get_size()[0] / 2,
                          self._pose.y + (2 * i + 1) *
                          Constants.SQUARE_SIZE / 2 + Constants.DISPLAY_HEIGTH))

        for i in range(len(self.__left_branch)):
            icon = self.__left_branch[i].update()
            display.blit(icon,
                         (self._pose.x - (2 * i + 1) *
                          Constants.SQUARE_SIZE / 2 - icon.get_size()[0],
                          self._pose.y - icon.get_size()[1] / 2 +
                          Constants.DISPLAY_HEIGTH))

        for i in range(len(self.__right_branch)):
            icon = self.__right_branch[i].update()
            display.blit(icon,
                         (self._pose.x + (2 * i + 1) *
                          Constants.SQUARE_SIZE / 2,
                          self._pose.y - icon.get_size()[1] / 2 +
                          Constants.DISPLAY_HEIGTH))

    def get_triggered_bombs(self):
        """
        Getter for the list of triggered bombs caused by the explosion.
        :return: List of coordinates for bombs that were triggered.
        """

        return self.__triggered_bombs

    @property
    def reward(self):
        """
        Getter for the reward of this fire. Method used in ai training.
        :return: Fire's total reward.
        """

        return self.__reward

    def add_reward(self, reward):
        """
        Adds a reward to the fire.
        :param reward: Reward to be added.
        """

        self.__reward += reward

    def contains(self, tile):
        """
        Check if a tile is contained by this fire object.
        :param tile: Tile to be checked.
        :return: True if the fire contains this tile.
        """

        f = self.tile
        if tile[0] == f[0]:
            if tile[1] == f[1]:
                return True
            elif tile[1] < f[1] and f[1] - tile[1] <= len(self.__up_branch):
                    return True
            elif tile[1] - f[1] <= len(self.__down_branch):
                return True
        elif tile[1] == f[1]:
            if tile[0] < f[0] and f[0] - tile[0] <= len(self.__left_branch):
                return True
            elif tile[0] - f[0] <= len(self.__right_branch):
                return True

        return False

    def __destroy_tile(self, tile, branch, tilemap):
        """
        Handles the destruction of a block by changing its unit type and its
        animation.
        :param tile: Tile coordinate in a tuple.
        :param branch: Branch in which the block was destroyed.
        :param tilemap: Tilemap array.
        """

        if np.any(tilemap[tile] == self.destroyable_block):
            branch.append(self.__explosion_animation)
            tilemap[tile] = Constants.UNIT_DESTROYING_BLOCK
        elif np.any(tilemap[tile] == self.powerups_hidden):
            branch.append(self.__explosion_animation)
            if tilemap[tile] == Constants.UNIT_POWERUP_VELOCITY_HIDE:
                self.__destroyed_powerups.append(
                    (tile, Constants.UNIT_POWERUP_VELOCITY_SHOW))
            elif tilemap[tile] == Constants.UNIT_POWERUP_FIRE_HIDE:
                self.__destroyed_powerups.append(
                    (tile, Constants.UNIT_POWERUP_FIRE_SHOW))
            else:
                self.__destroyed_powerups.append(
                    (tile, Constants.UNIT_POWERUP_BOMB_SHOW))
            tilemap[tile] = Constants.UNIT_DESTROYING_BLOCK
        elif np.any(tilemap[tile] == self.powerups_showed):
            branch.append(self.__explosion_animation)
            tilemap[tile] = Constants.UNIT_DESTROYING_POWERUP

    def __remove_fire(self, tilemap):
        """
        Updates the tilemap, removing the fire.
        :param tilemap: Tilemap array.
        """

        def update_reward(t):
            if tilemap[t] == Constants.UNIT_DESTROYING_BLOCK:
                self.__reward += Constants.BLOCK_REWARD
            elif tilemap[t] == Constants.UNIT_DESTROYING_POWERUP:
                self.__reward += Constants.POWERUP_DESTROYED_REWARD
            tilemap[t] = Constants.UNIT_EMPTY

        tilemap[self.tile] = Constants.UNIT_EMPTY
        for i in range(len(self.__up_branch)):
            tile = (self.tile[0] - i - 1, self.tile[1])
            update_reward(tile)
        for i in range(len(self.__down_branch)):
            tile = (self.tile[0] + i + 1, self.tile[1])
            update_reward(tile)
        for i in range(len(self.__left_branch)):
            tile = (self.tile[0], self.tile[1] - i - 1)
            update_reward(tile)
        for i in range(len(self.__right_branch)):
            tile = (self.tile[0], self.tile[1] + i + 1)
            update_reward(tile)

        for powerup in self.__destroyed_powerups:
            tilemap[powerup[0]] = powerup[1]

    def __setup_animations(self):
        """
        Sets up the all the fire's animations, even if the fire does not have
        one of its parts due to the tilemap.
        """

        self.__middle_animation = Animation(np.concatenate(
            [[self.__sprite['middle_thinner'], self.__sprite['middle_thin']],
             np.tile([self.__sprite['middle_normal'],
                      self.__sprite['middle_thick'],
                      self.__sprite['middle_thicker']], 3),
             [self.__sprite['middle_thick'], self.__sprite['middle_normal'],
              self.__sprite['middle_thin'], self.__sprite['middle_thinner']]]),
            Constants.FIRE_FRAME_DURATION * np.ones(15), stop=True)

        self.__up1_animation = Animation(np.concatenate(
            [[self.__sprite['up1_thinner'], self.__sprite['up1_thin']],
             np.tile([self.__sprite['up1_normal'],
                      self.__sprite['up1_thick'],
                      self.__sprite['up1_thicker']], 3),
             [self.__sprite['up1_thick'], self.__sprite['up1_normal'],
              self.__sprite['up1_thin'], self.__sprite['up1_thinner']]]),
            Constants.FIRE_FRAME_DURATION * np.ones(15), stop=True)

        self.__up2_animation = Animation(np.concatenate(
            [[self.__sprite['up2_thinner'], self.__sprite['up1_thin']],
             np.tile([self.__sprite['up2_normal'],
                      self.__sprite['up2_thick'],
                      self.__sprite['up2_thicker']], 3),
             [self.__sprite['up2_thick'], self.__sprite['up2_normal'],
              self.__sprite['up2_thin'], self.__sprite['up2_thinner']]]),
            Constants.FIRE_FRAME_DURATION * np.ones(15), stop=True)

        self.__down1_animation = Animation(np.concatenate(
            [[self.__sprite['down1_thinner'], self.__sprite['down1_thin']],
             np.tile([self.__sprite['down1_normal'],
                      self.__sprite['down1_thick'],
                      self.__sprite['down1_thicker']], 3),
             [self.__sprite['down1_thick'], self.__sprite['down1_normal'],
              self.__sprite['down1_thin'], self.__sprite['down1_thinner']]]),
            Constants.FIRE_FRAME_DURATION * np.ones(15), stop=True)

        self.__down2_animation = Animation(np.concatenate(
            [[self.__sprite['down2_thinner'], self.__sprite['down2_thin']],
             np.tile([self.__sprite['down2_normal'],
                      self.__sprite['down2_thick'],
                      self.__sprite['down2_thicker']], 3),
             [self.__sprite['down2_thick'], self.__sprite['down2_normal'],
              self.__sprite['down2_thin'], self.__sprite['down2_thinner']]]),
            Constants.FIRE_FRAME_DURATION * np.ones(15), stop=True)

        self.__left1_animation = Animation(np.concatenate(
            [[self.__sprite['left1_thinner'], self.__sprite['left1_thin']],
             np.tile([self.__sprite['left1_normal'],
                      self.__sprite['left1_thick'],
                      self.__sprite['left1_thicker']], 3),
             [self.__sprite['left1_thick'], self.__sprite['left1_normal'],
              self.__sprite['left1_thin'], self.__sprite['left1_thinner']]]),
            Constants.FIRE_FRAME_DURATION * np.ones(15), stop=True)

        self.__left2_animation = Animation(np.concatenate(
            [[self.__sprite['left2_thinner'], self.__sprite['left2_thin']],
             np.tile([self.__sprite['left2_normal'],
                      self.__sprite['left2_thick'],
                      self.__sprite['left2_thicker']], 3),
             [self.__sprite['left2_thick'], self.__sprite['left2_normal'],
              self.__sprite['left2_thin'], self.__sprite['left2_thinner']]]),
            Constants.FIRE_FRAME_DURATION * np.ones(15), stop=True)

        self.__right1_animation = Animation(np.concatenate(
            [[self.__sprite['right1_thinner'], self.__sprite['right1_thin']],
             np.tile([self.__sprite['right1_normal'],
                      self.__sprite['right1_thick'],
                      self.__sprite['right1_thicker']], 3),
             [self.__sprite['right1_thick'], self.__sprite['right1_normal'],
              self.__sprite['right1_thin'], self.__sprite['right1_thinner']]]),
            Constants.FIRE_FRAME_DURATION * np.ones(15), stop=True)

        self.__right2_animation = Animation(np.concatenate(
            [[self.__sprite['right2_thinner'], self.__sprite['right2_thin']],
             np.tile([self.__sprite['right2_normal'],
                      self.__sprite['right2_thick'],
                      self.__sprite['right2_thicker']], 3),
             [self.__sprite['right2_thick'], self.__sprite['right2_normal'],
              self.__sprite['right2_thin'], self.__sprite['right2_thinner']]]),
            Constants.FIRE_FRAME_DURATION * np.ones(15), stop=True)

        self.__explosion_animation = Animation(
            [self.__sprite['explosion1'], self.__sprite['explosion2'],
             self.__sprite['explosion3'], self.__sprite['explosion4'],
             self.__sprite['explosion5']],
            Constants.FIRE_FRAME_DURATION * 15 / 5 * np.ones(5), stop=True)
