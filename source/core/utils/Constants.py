GAME_NAME = "bomberboy"
FONT_SIZE = 30
MAX_FPS = 200
NUMBER_POWERUPS = 15
NUMBER_EMPTY = 8
GAME_TIME = 5  # Time in minutes

# Display constants
WINDOW_WIDTH = 735
WINDOW_HEIGHT = 689
DISPLAY_HEIGTH = 150
MAP_WIDTH = WINDOW_WIDTH
MAP_HEIGTH = WINDOW_HEIGHT - DISPLAY_HEIGTH
SQUARE_SIZE = 49

# Map unit constants
UNIT_EMPTY = 2
UNIT_PLAYER = 1
UNIT_FIXED_BLOCK = 0
UNIT_BLOCK = 3
UNIT_POWERUP_FIRE_HIDE = 4
UNIT_POWERUP_VELOCITY_HIDE = 5
UNIT_POWERUP_BOMB_HIDE = 6
UNIT_BOMB = 7
UNIT_FIRE = 8
UNIT_CENTER_FIRE = 9
UNIT_POWERUP_FIRE_SHOW = 10
UNIT_POWERUP_VELOCITY_SHOW = 11
UNIT_POWERUP_BOMB_SHOW = 12
UNIT_DESTROYING_BLOCK = 13
UNIT_DESTROYING_POWERUP = 14

# Colors
RED = (227, 38, 54)
BLUE = (56, 176, 222)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (66, 111, 66)
GRAY = (110, 110, 110)

# Character constants
STEPS_PER_SQUARE = 2
INITIAL_SPEED = 2.333  # Nome: Speed is in squares per second.
SPEED_INCREMENT = 0.666
MAX_SPEED = 9
INITIAL_FIRE = 2
FIRE_INCREMENT = 1

# Bomb constants
BOMB_FRAME_DURATION = 0.25
FIRE_FRAME_DURATION = 0.075

# Game state
MENU = 0
PLAYING = 1
SETUP = 2
# PAUSE = 3
FINISH = 4

# Match states
IN_GAME = 0
MAIN_MENU = 1
PAUSE = 2
OVER = 3
