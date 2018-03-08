from pygame.sprite import Sprite


class GameObject(Sprite):
    """
    A GameObject is an element that will be placed on the map. Possible
    GameObjects: BomberBoy, bomb, powerup and obstacles.
    """

    def __init__(self, pose):
        super().__init__()
        self._pose = pose

    def update(self, *args):
        pass
