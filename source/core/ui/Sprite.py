import cv2
import numpy as np
import pygame.image
import pygame.surfarray

from source.core.utils import Constants


class Sprite:
    def __init__(self, image_path, scenes_names_path, delta=(0, 0)):
        """
        Animation sprite class. It reads a sprite image sheet and associates
        each icon with a name.
        :param image_path: Path to a .gif file with a sheet of different icons
        on the animation.
        :param scenes_names_path: Path to a .txt file with names for each icon.
        :param delta: Tuple which allows variation of the size of each icon.
        It can be negative, to decrease the total size, or positive. If it is
        zero, the icon's width will be equal to a square size.
        """

        self.__sheet = pygame.image.load(image_path).convert_alpha()
        self.__delta = delta

        scenes_file = open(scenes_names_path)
        self.__scenes = scenes_file.readlines()
        for i in range(len(self.__scenes)):
            self.__scenes[i] = self.__scenes[i][0:-1]

        self.__generate_sprite()

    def __generate_sprite(self):
        """
        Analyzes connected components in the sprite sheet and isolates them in a
        dictionary of icons by isolating each component.
        """

        # Calculates connected components using opencv
        image = np.array(pygame.surfarray.pixels3d(self.__sheet))
        occupied = pygame.surfarray.pixels_alpha(self.__sheet) != 0
        connections = cv2.connectedComponents(occupied.astype(np.uint8),
                                              connectivity=8)
        image[np.multiply(image[:, :, 0] == 0, connections[1] != 0), 0] = 1
        self.__icons = {'None': pygame.surfarray.make_surface(np.zeros((1, 1)))}

        # Puts them in a dict of icons
        max_width = 0
        for index in range(1, connections[0]):
            if index < len(self.__scenes) + 1:
                component = connections[1] == index
                component = np.where(component != 0)
                mini = np.min(component[0])
                maxi = np.max(component[0])
                minj = np.min(component[1])
                maxj = np.max(component[1])
                icon = image[mini:maxi + 1, minj:maxj + 1, :]
                icon = pygame.surfarray.make_surface(icon)
                icon.set_colorkey(0)

                if icon.get_size()[1] > max_width:
                    max_width = icon.get_size()[0]

                self.__icons[self.__scenes[index - 1]] = icon

        for key in self.__icons:
            width = int((Constants.SQUARE_SIZE + self.__delta[0]) *
                        self.__icons[key].get_size()[0] / max_width)
            height = round(self.__icons[key].get_size()[1] *
                           width / self.__icons[key].get_size()[0] +
                           self.__delta[1])
            self.__icons[key] = pygame.transform.scale(self.__icons[key],
                                                       (width, height))

    def get_dict(self):
        """
        Getter for the dictionary of icons.
        :return: Icons dictionary.
        """

        return self.__icons
