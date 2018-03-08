from source.core.engine.Events import *
from source.core.engine.Menu import Menu
from source.core.utils.Constants import *


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

        self.screen_width = WINDOW_WIDTH
        self.screen_height = WINDOW_HEIGHT
        self.game_name = GAME_NAME
        self.window_screen = pygame.display.set_mode((self.screen_height, self.screen_width), 0, 32)
        pygame.display.set_caption(self.game_name)

        self.state = "menu"
        self.menu = Menu()

    def play(self):
        while True:
            if self.state == "menu":
                self.menu.draw_menu(self.window_screen)

            for event in pygame.event.get():
                if event.type == QUIT:
                    quit_event()

                if event.type == KEYDOWN:
                    keydowm_event()

                if event.type == KEYUP:
                    keyup_event()

            pygame.display.update()
