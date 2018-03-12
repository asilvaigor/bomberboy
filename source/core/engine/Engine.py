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

        self.fpsClock = pygame.time.Clock()

        self.game_name = GAME_NAME
        self.window_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
        pygame.display.set_caption(self.game_name)

        self.state = "menu"
        self.menu = Menu()

    def play(self):
        while True:
            if self.state == "menu":
                self.menu.draw_menu(self.window_screen)
                self.menu.check_for_event()

            for event in pygame.event.get():
                if event.type == QUIT:
                    quit_event()

                if event.type == KEYDOWN:
                    keydowm_event()

                if event.type == KEYUP:
                    keyup_event()

            pygame.display.update()

            self.fpsClock.tick(MAX_FPS)
