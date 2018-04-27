GAME_NAME = "bomberboy"
FONT_SIZE = 30
MAX_FPS = 200
NUMBER_POWERUPS = 15
NUMBER_EMPTY = 8
GAME_TIME = 5  # Time in minutes
TIME_SPEEDER = 1

# Display constants
WINDOW_WIDTH = 735
WINDOW_HEIGHT = 689
DISPLAY_HEIGTH = 150
MAP_WIDTH = WINDOW_WIDTH
MAP_HEIGTH = WINDOW_HEIGHT - DISPLAY_HEIGTH
SQUARE_SIZE = 49
NUM_ROWS = 11
NUM_COLUMNS = 15

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
UNIT_SELF = 15
UNIT_ENEMY = 16
NUM_UNITS = 17

# Colors
RED = (227, 38, 54)
BLUE = (117, 218, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (76, 119, 76)
LIGHT_GREEN = (122, 204, 135)
GRAY = (153, 178, 159)
YELLOW = (184, 224, 134)

# Character constants
STEPS_PER_SQUARE = 2
INITIAL_SPEED = 3.5 * TIME_SPEEDER  # Note: Speed is in squares per second.
SPEED_INCREMENT = 0.666 * TIME_SPEEDER
MAX_SPEED = 9 * TIME_SPEEDER
INITIAL_FIRE = 2
FIRE_INCREMENT = 1

# Bomb constants
BOMB_FRAME_DURATION = 0.25 / TIME_SPEEDER
FIRE_FRAME_DURATION = 0.075 / TIME_SPEEDER

# Game state
STATE_MENU = 0
STATE_PLAYING = 1
STATE_SETUP = 2
STATE_CLOSE = 4

# Match states
IN_GAME = 0
MAIN_MENU = 1
PAUSE = 2
OVER = 3

# Character selection
colors = ['white', 'black', 'blue', 'brown', 'magenta', 'gray',
          'green', 'orange', 'pink', 'purple', 'yellow']
WASD = 0
IJKL = 1
ARROWS = 2
CPU = 3
NONE = 4
OPTION_TYPE = 0
OPTION_COLOR = 1

# AI parameters
UPDATE_DELAY = 500 / TIME_SPEEDER
NUM_ACTIONS = 6
BLOCK_REWARD = 2
KILL_REWARD = 5
DEATH_REWARD = -1
POWERUP_REWARD = 2
POWERUP_DESTROYED_REWARD = -1
GAMMA = 0.99
RANDOM_ACTION_PROBABILITY = 0.01
RANDOM_SLOPE = 10e-6
LEARNING_RATE = 0.00025
MEMORY_SIZE = 1000000
BATCH_SIZE = 32
MODEL_UPDATE_COUNTER = 10000
