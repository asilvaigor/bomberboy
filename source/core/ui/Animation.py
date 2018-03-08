import numpy as np
import pygame.image
import pygame.surfarray
import cv2


class Animation:
    def __init__(self, image_path, scenes_names_path):
        """
        Animation sprite class. It reads an animation image sheet and associates
        each icon with a name.
        :param image_path: Path to a .gif file with a sheet of different icons
        on the animation.
        :param scenes_names_path: Path to a .txt file with names for each icon.
        """

        self.__sheet = pygame.image.load(image_path).convert_alpha()

        scenes_file = open(scenes_names_path)
        self.__scenes = scenes_file.readlines()
        for i in range(len(self.__scenes)):
            self.__scenes[i] = self.__scenes[i][0:-1]

        self.__generate_sprite()

    def __generate_sprite(self):
        """
        Analyzes connected components in the animation sheet and isolates them
        in a dictionary of icons.
        """

        image = np.array(pygame.surfarray.pixels3d(self.__sheet))
        occupied = np.logical_or(image[:, :, 0] != 0, np.logical_or(
            image[:, :, 1] != 0, image[:, :, 2] != 0))
        connections = cv2.connectedComponents(occupied.astype(np.uint8),
                                              connectivity=8)
        self.__icons = {}

        for index in range(1, connections[0]):
            if index < len(self.__scenes) + 1:
                component = connections[1] == index
                component = np.where(component != 0)
                mini = np.min(component[0])
                maxi = np.max(component[0])
                minj = np.min(component[1])
                maxj = np.max(component[1])
                icon = image[mini:maxi, minj:maxj, :]
                icon = pygame.surfarray.make_surface(icon)
                self.__icons[self.__scenes[index - 1]] = icon

    def get_sprite(self):
        """
        Getter for the dictionary of icons.
        :return: Icons dictionary.
        """

        return self.__icons
