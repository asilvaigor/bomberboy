from source.core.engine.Events import *


class Engine:
    """
    Game engine class. This is the class that runs the game and contains the
    map, elements, sounds, status etc.
    """

    def __init__(self):
        """
        Set variables required for window creation.
        """
        pygame.init()

        self.screen_width = 500
        self.screen_height = 700
        self.game_name = "Bomber Boy"
        self.window_screen = pygame.display.set_mode((self.screen_height, self.screen_width), 0, 32)

        pygame.display.set_caption(self.game_name)

    def play(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    quit_event()

                if event.type == KEYDOWN:
                    keydowm_event()

                if event.type == KEYUP:
                    keyup_event()

            pygame.display.update()
