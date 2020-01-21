from math import sqrt,cos,sin
from random import randint
# here there are all constants
# CAR_WH_RATIO
# CAR_DIM=36
TIME_SPEED = 60  # REAL 1s = GAME 60s

# Variables
FLOAT_PRECISION = 5

# window dimension
W_WIDTH = 800
W_HEIGHT = 800
W_TITLE = 'Traffico'
CAR_WIDTH = round(sqrt(W_WIDTH*W_HEIGHT/40*3/40*3),FLOAT_PRECISION)  # dimension of the car
CAR_HEIGHT = round(sqrt(W_WIDTH*W_HEIGHT/200*9/200*9),FLOAT_PRECISION)  # dimension of the car
TRUCK_WIDTH = round(sqrt(W_WIDTH*W_HEIGHT/40*2/40*2),FLOAT_PRECISION)  # dimension of the truck
TRUCK_HEIGHT = round(sqrt(W_WIDTH*W_HEIGHT/200*9/200*9),FLOAT_PRECISION)  # dimension of the truck
TRAILER_WIDTH = round(sqrt(W_WIDTH*W_HEIGHT/40*5/40*5),FLOAT_PRECISION)  # dimension of the trailer of the truck
TRAILER_HEIGHT = round(sqrt(W_WIDTH*W_HEIGHT/200*9/200*9),FLOAT_PRECISION)  # dimension of the trailer of the truck

ROAD_LINE_WIDTH = round(sqrt(W_WIDTH*W_HEIGHT/60/60)) # width of the white line
ROAD_LINE_SIZE = round(sqrt(W_WIDTH*W_HEIGHT/100/100)) # size of the white line
VEHICLE_RENDER = round(sqrt(W_WIDTH*W_HEIGHT/1600/1600)/6,FLOAT_PRECISION)
CAR_ACCELERATION = 249/1200 # this number permits to have a maximum velocity of 90
VEHICLE_FRICTION = 0.0006   # friction constant combined with car acceleration we get the maximum velocity of a vehicle
VEHICLE_SPAWN_SPEED = 30
TRUCK_ACCELERATION = 249/3000

# calculations for drawing lanes
POSITION_A_x = W_WIDTH/2-CAR_HEIGHT*0.75
POSITION_A_y = W_HEIGHT/2-CAR_HEIGHT*1.5
POSITION_B_x = W_WIDTH/2-CAR_HEIGHT*1.5
POSITION_B_y = W_HEIGHT/2-CAR_HEIGHT*0.75
POSITION_C_x = W_WIDTH/2+CAR_HEIGHT*0.75
POSITION_C_y = W_HEIGHT/2+CAR_HEIGHT*0.75
POSITION_D_x = W_WIDTH/2+CAR_HEIGHT*1.5
POSITION_D_y = W_HEIGHT/2+CAR_HEIGHT*1.5

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
BLUE = '#00A'
RANDOM_COLOR = lambda: randint(0,3)

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
FORWARD = 1

# Functions
def ROTATE(side, pos, rad):
    # note: the rotation is done in the opposite fashion from for a right-handed coordinate system due to the left-handedness of computer coordinates
    side.x -= pos.x
    side.y -= pos.y
    _x = side.x * cos(-rad) + side.y * sin(-rad)
    _y = -side.x * sin(-rad) + side.y * cos(-rad)
    side.x = _x + pos.x
    side.y = _y + pos.y