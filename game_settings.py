# Global variables definitions

ROTATION_SPEED = 4  # radians per second
ACCELERATION = 50
GAME_WINDOW = [1000, 600]  # Windows width and height

# Dictionary GAME = variables for game:
#           --> state - can be 'game', 'game_over', 'pause' ...
#           --> lifes - count of lifes
#           --> shield - value is time (in sec) when the Spaceship has a Shield
GAME = {'state': 'menu', 'lifes': 3, 'shield': 3, 'level': 1, 'score': 0}

OBJECTS = []

time_to_change_level = [0]
time_explosion = [0]
ufo_in_game = [0, 20]  # index 0 = count of Ufos in game (can be 0 or 1),
                       # index 1 = time in sec between 2 ufos in game
