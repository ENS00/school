from math import sqrt
# here there are all constants
# CAR_WH_RATIO
# CAR_DIM=36
CAR_MAX_SPEED = 90
TIME_SPEED = 60  # REAL 1s = GAME 60s

# Variables
FLOAT_PRECISION = 5

# window dimension
W_WIDTH = 800
W_HEIGHT = 800
W_TITLE = 'Traffico'
CAR_WIDTH = round(sqrt(W_WIDTH*W_HEIGHT/40*3/40*3),FLOAT_PRECISION)  # dimension of the car
CAR_HEIGHT = round(sqrt(W_WIDTH*W_HEIGHT/200*9/200*9),FLOAT_PRECISION)  # dimension of the car
ROAD_LINE_WIDTH = round(sqrt(W_WIDTH*W_HEIGHT/60/60)) # width of the white line
ROAD_LINE_SIZE = round(sqrt(W_WIDTH*W_HEIGHT/100/100)) # size of the white line
CAR_POWER = round(sqrt(W_WIDTH*W_HEIGHT/1600/1600),FLOAT_PRECISION)

# Colors
W_BACKGROUND = 'lightgreen'
COLOR_ROAD = '#888'
WHITE = '#FFF'
GREEN_ON = '#0F0'
GREEN_OFF = '#0A0'
YELLOW_ON = '#FF0'
YELLOW_OFF = '#AA0'
RED_ON = '#F00'
RED_OFF = '#A00'

# TrafficLight positions
TL_DIST_X = 20+W_WIDTH/70
TL_DIST_Y = 2+W_HEIGHT/30
TL_SIZE = sqrt(W_WIDTH*W_HEIGHT/16/16)
TL_LIGHT_SIZE = sqrt(W_WIDTH*W_HEIGHT/80/80)

# TrafficLight states
TL_OFF = 3
TL_GREEN = 2
TL_YELLOW = 1
TL_RED = 0

# Orientation
HORIZONTAL = 0
VERTICAL = 1
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3