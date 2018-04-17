import os

from source.core.ui.Sprite import Sprite
from source.core.utils import Constants


class SpriteHandler:
    def __init__(self):
        path = (os.path.dirname(os.path.realpath(__file__)) +
                '/../../../assets/sprites/')
        self.sprites = {}

        # Loading bomberboy sprites
        for key in Constants.colors:
            self.sprites[key] = Sprite(
                path + 'bomberboy_' + key + '.png',
                path + 'bomberboy.txt', (-3, 0)).get_dict()

        # Loading bomb sprites
        self.sprites['fire'] = Sprite(path + 'fire.png',
                                      path + 'fire.txt', (0, 4)).get_dict()
        self.sprites['bomb'] = Sprite(path + 'bomb.png',
                                      path + 'bomb.txt', (-2, 0)).get_dict()
