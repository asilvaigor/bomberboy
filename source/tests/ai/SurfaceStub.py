from pygame import Surface


class SurfaceStub(Surface):
    def __init__(self):
        super().__init__((0, 0))
        pass

    def blit(self, source, dest, area=None, special_flags=0):
        pass
