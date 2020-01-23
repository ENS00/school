from math import sqrt,cos,sin
from random import randint
# here there are all constants
# CAR_WH_RATIO
# CAR_DIM=36
TIME_SPEED = 2000  # REAL 1s = GAME 2000s

# Variables
FLOAT_PRECISION = 5

# window dimension
W_WIDTH = 800
W_HEIGHT = 800
W_TITLE = 'Traffico'
PROPORTION = round(sqrt(W_WIDTH*W_HEIGHT)/100,FLOAT_PRECISION)   # proportion used for other calcs
CAR_WIDTH = PROPORTION*15/2         # dimension of the car
CAR_HEIGHT = PROPORTION*9/2         # dimension of the car
BUS_WIDTH = PROPORTION*10           # dimension of the bus
BUS_HEIGHT = PROPORTION*9/2         # dimension of the bus
TRUCK_WIDTH = PROPORTION*11/2       # dimension of the truck
TRUCK_HEIGHT = PROPORTION*13/2      # dimension of the truck
TRAILER_WIDTH = PROPORTION*9        # dimension of the trailer of the truck
TRAILER_HEIGHT = PROPORTION*11/2    # dimension of the trailer of the truck

ROAD_LINE_WIDTH = int(PROPORTION*11/4)  # width of the white line
ROAD_LINE_SIZE = int(PROPORTION)        # size of the white line
ROAD_LINE_THICKNESS = PROPORTION*100/11
VEHICLE_RENDER = PROPORTION*TIME_SPEED/200000
VEHICLE_SPAWN_SPEED = 30
VEHICLE_FRICTION = 0.0006   # friction constant combined with car acceleration we get the maximum velocity of a vehicle
CAR_ACCELERATION = 249/1200 # this number permits to have a maximum velocity of 90 TO VERIFY (TODO)
BUS_ACCELERATION = 249/3000
TRUCK_ACCELERATION = 249/3000

# calculations for drawing lanes
POSITION_A_x = W_WIDTH/2-ROAD_LINE_THICKNESS/2
POSITION_A_y = W_HEIGHT/2-ROAD_LINE_THICKNESS
POSITION_B_x = W_WIDTH/2-ROAD_LINE_THICKNESS
POSITION_B_y = W_HEIGHT/2-ROAD_LINE_THICKNESS/2
POSITION_C_x = W_WIDTH/2+ROAD_LINE_THICKNESS/2
POSITION_C_y = W_HEIGHT/2+ROAD_LINE_THICKNESS/2
POSITION_D_x = W_WIDTH/2+ROAD_LINE_THICKNESS
POSITION_D_y = W_HEIGHT/2+ROAD_LINE_THICKNESS

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
TL_DIST_X = 32+W_WIDTH/70
TL_DIST_Y = 2+W_HEIGHT/30
TL_SIZE = PROPORTION*25/4
TL_LIGHT_SIZE = PROPORTION*5/4

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