import const
import math
import copy
from random import randint


class GraphicObject():
    def __init__(self, canvas):
        self.canvas = canvas
        self.id = canvas.idassigner.getNewID()

    def draw(self):
        raise Exception('Not yet implemented')

    def move(self, x, y, render_graphic=True):
        # if hasattr(self, 'sides'):
        #     prevSides = []
        #     for i in self.sides:
        #         prevSides.append(i.clonePosition())
        if render_graphic:
            if hasattr(self, 'graphicitems'):
                [self.canvas.move(self.graphicitems[i], round(x, const.FLOAT_PRECISION), round(y, const.FLOAT_PRECISION))
                for i in self.graphicitems]
            if hasattr(self, 'graphic'):
                self.canvas.move(self.graphic, round(x, const.FLOAT_PRECISION), round(y, const.FLOAT_PRECISION))
            # if hasattr(self, 'graphic_trailer'):
            #     self.canvas.move(self.graphic_trailer, round(x, const.FLOAT_PRECISION), round(y, const.FLOAT_PRECISION))
                
        if hasattr(self, 'position'):
            self.position.move(x, y)
        if hasattr(self, 'sides'):
            for i in self.sides:
                i.move(x, y)
        # if hasattr(self, 'trailer_sides'):
        #     hook1 = Position(math.fabs(self.trailer_sides[0].x-self.trailer_sides[1].x),math.fabs(self.trailer_sides[0].y-self.trailer_sides[1].y))
        #     hook2 = Position(math.fabs(self.sides[0].x-self.sides[1].x),math.fabs(self.sides[0].y-self.sides[1].y))
        #     prevhook2 = Position(math.fabs(prevSides[0].x-prevSides[1].x),math.fabs(prevSides[0].y-prevSides[1].y))
        #     hookDist = hook1.distance(hook2)
        #     # diff = hookDist-self.hookDist
        #     newhook1 = prevhook2.projection(hook1,hook2)
            

            # rad = math.atan2(newhook1.y-hook1.y,newhook1.x-hook1.x) 

            # x, y = _rot(self.trailer_sides[0].x, self.trailer_sides[0].y)
            # self.trailer_sides[0].moveTo(x, y)
            # x, y = _rot(self.trailer_sides[1].x, self.trailer_sides[1].y)
            # self.trailer_sides[1].moveTo(x, y)
            # x, y = _rot(self.trailer_sides[2].x, self.trailer_sides[2].y)
            # self.trailer_sides[2].moveTo(x, y)
            # x, y = _rot(self.trailer_sides[3].x, self.trailer_sides[3].y)
            # self.trailer_sides[3].moveTo(x, y)
        # if render_graphic and hasattr(self, 'graphic_trailer'):
        #     self.canvas.coords(self.graphic_trailer, self.trailer_sides[0].x, self.trailer_sides[0].y,
        #                        self.trailer_sides[1].x, self.trailer_sides[1].y,
        #                        self.trailer_sides[2].x, self.trailer_sides[2].y,
        #                        self.trailer_sides[3].x, self.trailer_sides[3].y)

    def moveTo(self, x, y, render_graphic=True):
        if render_graphic:
            if hasattr(self, 'graphicitems'):
                [self.canvas.moveTo(self.graphicitems[i], round(x, const.FLOAT_PRECISION), round(y, const.FLOAT_PRECISION))
                for i in self.graphicitems]
            if hasattr(self, 'graphic'):
                self.canvas.moveTo(self.graphic, round(x, const.FLOAT_PRECISION), round(y, const.FLOAT_PRECISION))
        if hasattr(self, 'position'):
            self.position.moveTo(x, y)

    def rotate(self, rad, render_graphic=True):
        self.degrees = self.degrees+rad
        if self.degrees > math.pi:
            self.degrees = self.degrees-math.pi*2
        if self.degrees < -math.pi:
            self.degrees = self.degrees+math.pi*2

        const.ROTATE(self.sides[0], self.position, rad)
        const.ROTATE(self.sides[1], self.position, rad)
        const.ROTATE(self.sides[2], self.position, rad)
        const.ROTATE(self.sides[3], self.position, rad)
        if render_graphic and hasattr(self, 'graphic'):
            self.canvas.coords(self.graphic, self.sides[0].x, self.sides[0].y,
                               self.sides[1].x, self.sides[1].y,
                               self.sides[2].x, self.sides[2].y,
                               self.sides[3].x, self.sides[3].y)


class Position():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Position({},{})'.format(self.x, self.y)

    def moveTo(self, x, y):
        if(hasattr(self,'sides')):
            for i in sides:
                i.x += self.x-x
                i.y += self.y-y
        self.x = x
        self.y = y

    def move(self, x, y):
        self.x += x
        self.y += y
        # self.x = round(self.x+x, const.FLOAT_PRECISION)
        # self.y = round(self.y+y, const.FLOAT_PRECISION)

    # this point is between two points? (with projection)
    def betweenProjection(self, pos1, pos2, tollerance=2):
        projectionPoint = self.projection(pos1,pos2)
        if (projectionPoint.x <= pos1.x+tollerance and projectionPoint.x >= pos2.x-tollerance) or (projectionPoint.x >= pos1.x-tollerance and projectionPoint.x <= pos2.x+tollerance):
            if projectionPoint.y <= pos1.y+tollerance and projectionPoint.y >= pos2.y-tollerance:
                return True
            if projectionPoint.y >= pos1.y-tollerance and projectionPoint.y <= pos2.y+tollerance:
                return True
        return False
    
    # this point is between two points?
    def between(self, pos1, pos2, tollerance=10):
        if (self.x <= pos1.x+tollerance and self.x >= pos2.x-tollerance) or (self.x >= pos1.x-tollerance and self.x <= pos2.x+tollerance):
            if self.y <= pos1.y+tollerance and self.y >= pos2.y-tollerance:
                return True
            if self.y >= pos1.y-tollerance and self.y <= pos2.y+tollerance:
                return True
        return False
        
    # pos1 and pos2 define the line
    def projection(self,pos1,pos2):
        # find a point in a line that is the nearest to another point
        # that point is the projection of the point in the line
        # find line from 2 points
        if math.fabs(pos2.x-pos1.x)>0:
            # y = mx + q
            m = (pos2.y-pos1.y)/(pos2.x-pos1.x)
            q = pos1.y - pos1.x*m
            # perpendicular
            if math.fabs(m)>0:
                # y = mx + q
                m2 = -1/m
                q2 = self.y - self.x*m2
                # solution
                valx = (q2-q)/(m-m2)
                valy = m*valx + q
                projectionOnLine = Position(valx,valy)
            else:
                # y = c
                valx = self.x
                valy = pos1.y
                projectionOnLine = Position(valx,valy)
        else:
            # x = c
            valx = pos1.x
            valy = self.y
            projectionOnLine = Position(valx,valy)
        return projectionOnLine

    def near(self, pos, tollerance=2):
        if self.x <= pos.x+tollerance and self.x >= pos.x-tollerance and self.y <= pos.y+tollerance and self.y >= pos.y-tollerance:
            return True
        return False

    def distance(self, pos):
        return math.sqrt((self.x-pos.x)*(self.x-pos.x)+(self.y-pos.y)*(self.y-pos.y))
    # starting from pos1, where i am going if i want to arrive in pos2?
    @staticmethod
    def getDirection(pos1, pos2):
        rad = math.atan2(pos2.y-pos1.y, pos2.x-pos1.x)
        ret = []
        if rad > -math.pi/2+0.001 and rad < math.pi/2-0.001:
            ret.append('right')
        if (rad > math.pi/2+0.001 and rad < math.pi+0.001) or (rad > -math.pi-0.001 and rad < -math.pi/2-0.001):
            ret.append('left')
        if rad > 0.001 and rad < math.pi-0.001:
            ret.append('down')
        if rad > -math.pi+0.001 and rad < -0.001:
            ret.append('up')
        return ret
    
    def equals(self,pos):
        return hasattr(pos,'x') and hasattr(pos,'y') and self.x==pos.x and self.y==pos.y

    def clonePosition(self):
        return Position(self.x,self.y)


class Waypoint(Position):
    def __init__(self, x, y, velocity=None, desidered=True):
        # position of waypoint
        super().__init__(x, y)
        # target velocity
        self.velocity = velocity
        # is this the point I was waiting for?
        self.desidered=desidered
    
    # do not clone me
    def __deepcopy__(self,memo=None):
        return self


class TrafficLight(GraphicObject):
    def __init__(self, canvas, posred, direction=const.DOWN, state=const.TL_RED, on=False):
        super().__init__(canvas)
        self.on = on
        self.state = state
        if self.state == const.TL_RED:
            self.count = 5
        elif self.state == const.TL_YELLOW:
            self.count = 4
        else:
            self.count = -1

        self.posred = posred
        if direction == const.LEFT:
            self.posgreen = Position((self.posred.x+const.TL_SIZE), (self.posred.y))
        elif direction == const.RIGHT:
            self.posgreen = Position((self.posred.x-const.TL_SIZE), (self.posred.y))
        elif direction == const.UP:
            self.posgreen = Position((self.posred.x), (self.posred.y+const.TL_SIZE))
        else:
            self.posgreen = Position((self.posred.x), (self.posred.y-const.TL_SIZE))
        self.posyellow = Position((self.posgreen.x+self.posred.x)/2, (self.posgreen.y+self.posred.y)/2)

        if self.posgreen.x == self.posred.x:
            self.orientation = const.HORIZONTAL
        else:
            self.orientation = const.VERTICAL

    def changeState(self):
        if self.on:
            if self.state == const.TL_RED:
                self.state = const.TL_GREEN
            elif self.state == const.TL_YELLOW:
                self.state = const.TL_RED
            elif self.state == const.TL_GREEN:
                self.state = const.TL_YELLOW
        else:
            if self.state == const.TL_YELLOW:
                self.state = const.TL_OFF
            else:
                self.state = const.TL_YELLOW

    def turnOn(self):
        self.on = True

    def turnOff(self):
        self.on = False

    def update(self):
        self.count += 1
        if self.count >= 12:
            self.count = 0
        if self.on:
            if self.state == const.TL_GREEN and self.count >= 4:
                self.changeState()
            elif self.state == const.TL_YELLOW and self.count != 4:
                self.changeState()
            elif self.state == const.TL_RED and self.count <= 4:
                self.changeState()
        else:
            self.changeState()

    def draw(self):
        if not (hasattr(self, 'redLight') or hasattr(self, 'yellowLight') or hasattr(self, 'greenLight')):
            self.redLight = self.canvas.create_oval(
                self.posred.x-const.TL_LIGHT_SIZE, self.posred.y-const.TL_LIGHT_SIZE,
                self.posred.x+const.TL_LIGHT_SIZE, self.posred.y+const.TL_LIGHT_SIZE, fill=const.RED_OFF)
            self.yellowLight = self.canvas.create_oval(
                self.posyellow.x-const.TL_LIGHT_SIZE, self.posyellow.y-const.TL_LIGHT_SIZE,
                self.posyellow.x+const.TL_LIGHT_SIZE, self.posyellow.y+const.TL_LIGHT_SIZE, fill=const.YELLOW_OFF)
            self.greenLight = self.canvas.create_oval(
                self.posgreen.x-const.TL_LIGHT_SIZE, self.posgreen.y-const.TL_LIGHT_SIZE,
                self.posgreen.x+const.TL_LIGHT_SIZE, self.posgreen.y+const.TL_LIGHT_SIZE, fill=const.GREEN_OFF)
            self.graphicitems = (self.redLight, self.yellowLight, self.greenLight)
        if self.state == const.TL_RED:
            self.canvas.itemconfigure(self.redLight, fill=const.RED_ON)
            self.canvas.itemconfigure(self.yellowLight, fill=const.YELLOW_OFF)
            self.canvas.itemconfigure(self.greenLight, fill=const.GREEN_OFF)
        elif self.state == const.TL_YELLOW:
            self.canvas.itemconfigure(self.redLight, fill=const.RED_OFF)
            self.canvas.itemconfigure(self.yellowLight, fill=const.YELLOW_ON)
            self.canvas.itemconfigure(self.greenLight, fill=const.GREEN_OFF)
        elif self.state == const.TL_GREEN:
            self.canvas.itemconfigure(self.redLight, fill=const.RED_OFF)
            self.canvas.itemconfigure(self.yellowLight, fill=const.YELLOW_OFF)
            self.canvas.itemconfigure(self.greenLight, fill=const.GREEN_ON)
        elif self.state == const.TL_OFF:
            self.canvas.itemconfigure(self.redLight, fill=const.RED_OFF)
            self.canvas.itemconfigure(self.yellowLight, fill=const.YELLOW_OFF)
            self.canvas.itemconfigure(self.greenLight, fill=const.GREEN_OFF)


class RoadObject(GraphicObject):
    def __init__(self, canvas):
        super().__init__(canvas)

    def isA(self, prop):
        if prop in self.tags:
            return True
        return False

    def hasSameTags(self,obj):
        if True in [True for prop in self.tags if not prop in obj.tags]:
            return True
        return False

    def clone(self):
        return copy.deepcopy(self)


class Road(RoadObject):
    def __init__(self, canvas, pstart, pstop, dim, lineW=const.ROAD_LINE_WIDTH, lineS=const.ROAD_LINE_SIZE, tags=[]):
        super().__init__(canvas)
        self.pstart = pstart
        self.pstop = pstop
        self.dim = dim
        self.lineW = lineW
        self.lineS = lineS
        self.tags = tags
        if self.pstart.x != self.pstop.x:
            self.orientation = const.HORIZONTAL
        else:
            self.orientation = const.VERTICAL

    def draw(self):
        if not hasattr(self, 'graphicitems'):
            if self.orientation == const.HORIZONTAL:
                # draw road
                self.graphicitems = [self.canvas.create_rectangle(self.pstart.x, self.pstart.y-self.dim/2,
                                                                  self.pstop.x, self.pstart.y+self.dim/2,
                                                                  fill=const.COLOR_ROAD, width=0)]
                # draw border lines
                self.graphicitems.append(self.canvas.create_rectangle(self.pstart.x, self.pstart.y-self.dim/2+const.PROPORTION/4,
                                                                  self.pstop.x, self.pstart.y-self.dim/2-const.PROPORTION/4,
                                                                  fill=const.WHITE, width=0))
                self.graphicitems.append(self.canvas.create_rectangle(self.pstart.x, self.pstart.y+self.dim/2+const.PROPORTION/4,
                                                                  self.pstop.x, self.pstart.y+self.dim/2-const.PROPORTION/4,
                                                                  fill=const.WHITE, width=0))
                # draw white lines
                step = self.lineS*2+self.lineW
                if self.pstart.x < self.pstop.x:
                    road_lines = range(round(self.pstart.x),
                                       round(self.pstop.x), step)
                    stopline = self.lineS+2
                else:
                    road_lines = range(round(self.pstop.x),
                                       round(self.pstart.x), step)
                    stopline = -self.lineS-2
                for posx in road_lines:
                    self.graphicitems.append(self.canvas.create_rectangle(posx, self.pstart.y-self.dim/24,
                                                                          posx+self.lineW, self.pstart.y+self.dim/24,
                                                                          fill=const.WHITE, width=0))
                # draw stop line
                if super().isA('entry'):
                    self.graphicitems.append(self.canvas.create_rectangle(self.pstop.x, self.pstart.y-self.dim/2,
                                                                          self.pstop.x-stopline, self.pstart.y+self.dim/2,
                                                                          fill=const.WHITE, width=0))
            else:
                self.graphicitems = [self.canvas.create_rectangle(self.pstart.x-self.dim/2, self.pstart.y,
                                                                  self.pstart.x+self.dim/2, self.pstop.y,
                                                                  fill=const.COLOR_ROAD, width=0)]
                # draw border lines
                self.graphicitems.append(self.canvas.create_rectangle(self.pstart.x-self.dim/2+const.PROPORTION/4, self.pstart.y,
                                                                  self.pstart.x-self.dim/2-const.PROPORTION/4, self.pstop.y,
                                                                  fill=const.WHITE, width=0))
                self.graphicitems.append(self.canvas.create_rectangle(self.pstart.x+self.dim/2+const.PROPORTION/4, self.pstart.y,
                                                                  self.pstart.x+self.dim/2-const.PROPORTION/4, self.pstop.y,
                                                                  fill=const.WHITE, width=0))
                # draw white lines
                step = self.lineS*2+self.lineW
                if self.pstart.y < self.pstop.y:
                    road_lines = range(round(self.pstart.y),
                                       round(self.pstop.y), step)
                    stopline = self.lineS+2
                else:
                    road_lines = range(round(self.pstop.y),
                                       round(self.pstart.y), step)
                    stopline = -self.lineS-2
                for posy in road_lines:
                    self.graphicitems.append(self.canvas.create_rectangle(self.pstart.x-self.dim/24, posy,
                                                                          self.pstart.x+self.dim/24, posy+self.lineW,
                                                                          fill=const.WHITE, width=0))
                # draw stop line
                if super().isA('entry'):
                    self.graphicitems.append(self.canvas.create_rectangle(self.pstart.x-self.dim/2, self.pstop.y,
                                                                          self.pstart.x+self.dim/2, self.pstop.y-stopline,
                                                                          fill=const.WHITE, width=0))


class Lane(Road):
    # pstart and pstop centered
    def __init__(self, canvas, pstart, pstop, tLight=None, dim=const.ROAD_LINE_THICKNESS):
        tags = Position.getDirection(pstart, pstop)
        tags.extend(['exit'])
        super().__init__(canvas, pstart, pstop, dim, tags=tags)
        if self.isA('left'):
            self.startLanePoints = (
                Position(pstart.x, pstart.y+2-const.CAR_HEIGHT/2),
                Position(pstart.x, pstart.y-2+const.CAR_HEIGHT/2)
            )
            self.endLanePoints = (
                Position(pstop.x, pstop.y+2-const.CAR_HEIGHT/2),
                Position(pstop.x, pstop.y-2+const.CAR_HEIGHT/2)
            )
        elif self.isA('right'):
            self.startLanePoints = (
                Position(pstart.x, pstart.y-2+const.CAR_HEIGHT/2),
                Position(pstart.x, pstart.y+2-const.CAR_HEIGHT/2)
            )
            self.endLanePoints = (
                Position(pstop.x, pstop.y-2+const.CAR_HEIGHT/2),
                Position(pstop.x, pstop.y+2-const.CAR_HEIGHT/2)
            )
        elif self.isA('up'):
            self.startLanePoints = (
                Position(pstart.x-2+const.CAR_HEIGHT/2, pstart.y),
                Position(pstart.x+2-const.CAR_HEIGHT/2, pstart.y)
            )
            self.endLanePoints = (
                Position(pstop.x-2+const.CAR_HEIGHT/2, pstop.y),
                Position(pstop.x+2-const.CAR_HEIGHT/2, pstop.y)
            )
        else:
            self.startLanePoints = (
                Position(pstart.x+2-const.CAR_HEIGHT/2, pstart.y),
                Position(pstart.x-2+const.CAR_HEIGHT/2, pstart.y)
            )
            self.endLanePoints = (
                Position(pstop.x+2-const.CAR_HEIGHT/2, pstop.y),
                Position(pstop.x-2+const.CAR_HEIGHT/2, pstop.y)
            )

    def createTrafficLight(self, status=const.TL_RED):
        self.tags.remove('exit')
        self.tags.append('entry')
        self.tLight = None
        # create the tl near the right side of the road
        if self.isA('down'):
            self.tLight = TrafficLight(self.canvas,
                                       Position(self.endLanePoints[0].x-const.TL_DIST_X, self.endLanePoints[0].y-const.TL_DIST_Y),
                                       const.DOWN,status)
        elif self.isA('up'):
            self.tLight = TrafficLight(self.canvas,
                                       Position(self.endLanePoints[0].x+const.TL_DIST_X, self.endLanePoints[0].y+const.TL_DIST_Y),
                                       const.UP,status)
        elif self.isA('left'):
            self.tLight = TrafficLight(self.canvas,
                                       Position(self.endLanePoints[0].x+const.TL_DIST_Y, self.endLanePoints[0].y-const.TL_DIST_X),
                                       const.LEFT,status)
        elif self.isA('right'):
            self.tLight = TrafficLight(self.canvas,
                                       Position(self.endLanePoints[0].x-const.TL_DIST_Y, self.endLanePoints[0].y+const.TL_DIST_X),
                                       const.RIGHT,status)
        return self.tLight

    def removeTrafficLight(self):
        self.tags.remove('entry')
        self.tags.append('exit')
        del self.tLight

    def draw(self):
        if not (hasattr(self, 'graphic') or hasattr(self, 'graphicitems')):
            super().draw()

    # do not clone me
    def __deepcopy__(self,memo=None):
        return self


class Crossroad(RoadObject):
    def __init__(self, canvas, lanes):
        super().__init__(canvas)
        self.entries = [i for i in lanes if i.isA('entry')]
        self.exits = [i for i in lanes if i.isA('exit')]
        # assuming all lanes have equal dimensions
        self.dim = self.entries[0].dim
        minpstop = Position(2000, 2000)
        maxpstop = Position(0, 0)
        for i in self.exits:
            i.crossroad = self
        for i in self.entries:
            i.crossroad = self
            if i.pstop.x < minpstop.x:
                minpstop.x = i.pstop.x
            if i.pstop.y < minpstop.y:
                minpstop.y = i.pstop.y
            if i.pstop.x > maxpstop.x:
                maxpstop.x = i.pstop.x
            if i.pstop.y > maxpstop.y:
                maxpstop.y = i.pstop.y
        self.points = (Position(minpstop.x, minpstop.y), Position(maxpstop.x, minpstop.y),
                       Position(minpstop.x, maxpstop.y), Position(maxpstop.x, maxpstop.y))

    def draw(self):
        if not (hasattr(self, 'graphic') or hasattr(self, 'graphic')):
            self.graphic = self.canvas.create_rectangle(self.points[0].x, self.points[0].y,
                                                        self.points[3].x, self.points[3].y,
                                                        fill=const.COLOR_ROAD, width=0)
   # we get where the point is (in which specific lane)

    def getLaneFromPos(self, pos, tollerance=10):
        for i in self.entries:
            if pos.between(i.startLanePoints[0], i.endLanePoints[0],tollerance):
                return i, 0
            if pos.between(i.startLanePoints[1], i.endLanePoints[1],tollerance):
                return i, 1
        for i in self.exits:
            if pos.between(i.startLanePoints[0], i.endLanePoints[0],tollerance):
                return i, 0
            if pos.between(i.startLanePoints[1], i.endLanePoints[1],tollerance):
                return i, 1
        # this point is not in a lane
        return None, None
    
    def hasPrecedence(self,vehicle1,vehicle2):
        if(vehicle1.spawnDirection == vehicle2.spawnDirection):
            return vehicle1.id < vehicle2.id
        ## it's possible to get collisions from vehicles that turn
        if vehicle2.objectiveDirection == const.RIGHT:
            return False
        if vehicle1.objectiveDirection == const.RIGHT:
            return True
        if vehicle1.objectiveDirection == vehicle2.objectiveDirection:
            if(vehicle1.spawnDirection == const.UP and vehicle2.spawnDirection == const.RIGHT):
                return True
            if(vehicle1.spawnDirection == const.LEFT and vehicle2.spawnDirection == const.UP):
                return True
            if(vehicle1.spawnDirection == const.DOWN and vehicle2.spawnDirection == const.LEFT):
                return True
            if(vehicle1.spawnDirection == const.RIGHT and vehicle2.spawnDirection == const.DOWN):
                return True
            return False
        if vehicle2.objectiveDirection == const.FORWARD:
            return False
        if vehicle1.objectiveDirection == const.FORWARD:
            return True

    def spawnVehicle(self):
        r = randint(0,3)
        o = [0,1,2,3]
        o.remove(r)
        if(randint(0,7)>5):
            newVehicle = Bus(self.canvas,self.entries[r].startLanePoints[randint(0,1)],self)
        else:
            newVehicle = Car(self.canvas,self.entries[r].startLanePoints[randint(0,1)],self)
        newVehicle.draw()
        newVehicle.setObjective(self.exits[o[randint(0,2)]])
        return newVehicle

    # do not clone me
    def __deepcopy__(self,memo=None):
        return self
        


class Vehicle(RoadObject):
    def __init__(self, canvas, pos, crossroad, tags=[]):
        super().__init__(canvas)
        self.position = pos.clonePosition()
        self.tags = tags
        self.velocity = const.VEHICLE_SPAWN_SPEED
        self.degrees = 0
        self.steerDeg = 0
        self.acceleration = 0
        self.deceleration = 0
        self.sensibility = 1
        self.crossroad = crossroad

    def clone(self):
        return copy.deepcopy(self)

    def draw(self):
        # not implemented in father class
        pass

    def alignToLine(self):
        currentLane, rightS = self.crossroad.getLaneFromPos(self.position)
        if not currentLane:
            raise Exception('This object is not in a lane')
        if not currentLane.isA('entry'):
            raise Exception('This vehicle is in the wrong side')
        if currentLane.isA('up'):
            self.rotate(-math.pi/2)
            self.spawnDirection = const.UP
        elif currentLane.isA('down'):
            self.rotate(math.pi/2)
            self.spawnDirection = const.DOWN
        elif currentLane.isA('left'):
            self.rotate(math.pi)
            self.spawnDirection = const.LEFT
        else:
            self.spawnDirection = const.RIGHT
        # if hasattr(self,'trailer_sides'):
        #     distance = 40
        #     if currentLane.isA('up'):
        #         self.trailer_sides[0].move(0,distance)
        #         self.trailer_sides[1].move(0,distance)
        #         self.trailer_sides[2].move(0,distance)
        #         self.trailer_sides[3].move(0,distance)
        #     elif currentLane.isA('down'):
        #         self.trailer_sides[0].move(0,-distance)
        #         self.trailer_sides[1].move(0,-distance)
        #         self.trailer_sides[2].move(0,-distance)
        #         self.trailer_sides[3].move(0,-distance)
        #     elif currentLane.isA('left'):
        #         self.trailer_sides[0].move(distance,0)
        #         self.trailer_sides[1].move(distance,0)
        #         self.trailer_sides[2].move(distance,0)
        #         self.trailer_sides[3].move(distance,0)
        #     else:
        #         self.trailer_sides[0].move(-distance,0)
        #         self.trailer_sides[1].move(-distance,0)
        #         self.trailer_sides[2].move(-distance,0)
        #         self.trailer_sides[3].move(-distance,0)

    def update(self):
        self.velocity += self.acceleration*self.power
        if self.velocity > 0:
            self.velocity -= self.deceleration/1.5
        self.acceleration = 0
        self.deceleration = 0
        if self.velocity > 0:
            self.velocity = round(self.velocity - const.VEHICLE_FRICTION*self.velocity - math.fabs(self.steerDeg/10), const.FLOAT_PRECISION)
        if self.velocity < 0:
            self.velocity = 0
        else:
            self.rotate(self.steerDeg*self.velocity / (self.velocity*self.velocity*1.25+1))
            calc_x = round(math.cos(self.degrees)*self.velocity*const.VEHICLE_RENDER, const.FLOAT_PRECISION)
            calc_y = round(math.sin(self.degrees)*self.velocity*const.VEHICLE_RENDER, const.FLOAT_PRECISION)
            self.move(calc_x, calc_y)

    def steer(self, pow=0):
        if pow < -1:
            pow = -1
        if pow > 1:
            pow = 1
        self.steerDeg = round(pow,const.FLOAT_PRECISION)

    def accelerate(self, pow=0.5):
        if pow < 0:
            pow = 0
        if pow > 1:
            pow = 1
        self.acceleration = pow*pow
        self.deceleration = 0

    def brake(self, pow=0.5):
        if pow < 0:
            pow = 0
        if pow > 1:
            pow = 1
        self.deceleration = pow*pow
        self.acceleration = 0
    # we tell to the vehicle where to go and we set a step by step guide to get there

    def setObjective(self, lane):
        self.waypoints = []
        if not lane.isA('exit'):
            raise Exception('Lane selected is not an exit')
        currentLane, rightS = self.crossroad.getLaneFromPos(self.position)
        if not currentLane:
            raise Exception('This object is not in a lane')
        if not currentLane.isA('entry'):
            raise Exception('Cannot set objective when the vehicle is already leaving')
        if ((currentLane.isA('right') and lane.isA('left')) or
            (currentLane.isA('up') and lane.isA('down')) or
            (currentLane.isA('left') and lane.isA('right')) or
                (currentLane.isA('down') and lane.isA('up'))):
            raise Exception('Cannot set objective same road (you can only move right, forward or left)')
        # find if we want to turn left or right or go forward
        # then think if we need extra waypoints
        if (currentLane.isA('left') and lane.isA('down')) or (currentLane.isA('up') and lane.isA('left')) or (currentLane.isA('right') and lane.isA('up')) or (currentLane.isA('down') and lane.isA('right')):
            self.objectiveDirection = const.LEFT
            if(rightS == 0):
                # we are on the wrong side
                rightS = 1
                if currentLane.isA('right'):
                    self.waypoints.append(Waypoint(currentLane.endLanePoints[rightS].x/2+const.PROPORTION, currentLane.endLanePoints[rightS].y, 25))
                elif currentLane.isA('left'):
                    self.waypoints.append(Waypoint(currentLane.endLanePoints[rightS].x*4/3-const.PROPORTION, currentLane.endLanePoints[rightS].y, 25))
                elif currentLane.isA('up'):
                    self.waypoints.append(Waypoint(currentLane.endLanePoints[rightS].x, currentLane.endLanePoints[rightS].y*4/3-const.PROPORTION, 25))
                else:
                    self.waypoints.append(Waypoint(currentLane.endLanePoints[rightS].x, currentLane.endLanePoints[rightS].y/2+const.PROPORTION, 25))
            # end of current line
            if currentLane.isA('right'):
                self.waypoints.append(Waypoint(currentLane.endLanePoints[rightS].x+50, currentLane.endLanePoints[rightS].y, 10))
            elif currentLane.isA('left'):
                self.waypoints.append(Waypoint(currentLane.endLanePoints[rightS].x-50, currentLane.endLanePoints[rightS].y, 10))
            elif currentLane.isA('up'):
                self.waypoints.append(Waypoint(currentLane.endLanePoints[rightS].x, currentLane.endLanePoints[rightS].y-50, 10))
            else:
                self.waypoints.append(Waypoint(currentLane.endLanePoints[rightS].x, currentLane.endLanePoints[rightS].y+50, 10))
            # start of new line
            if currentLane.isA('right'):
                self.waypoints.append(Waypoint(lane.startLanePoints[rightS].x-const.PROPORTION*2, lane.startLanePoints[rightS].y, 25))
            elif currentLane.isA('left'):
                self.waypoints.append(Waypoint(lane.startLanePoints[rightS].x+const.PROPORTION*2, lane.startLanePoints[rightS].y, 25))
            elif currentLane.isA('up'):
                self.waypoints.append(Waypoint(lane.startLanePoints[rightS].x, lane.startLanePoints[rightS].y+const.PROPORTION*2, 25))
            else:
                self.waypoints.append(Waypoint(lane.startLanePoints[rightS].x, lane.startLanePoints[rightS].y-const.PROPORTION*2, 25))
            #self.waypoints.append(Waypoint(lane.startLanePoints[rightS].x, lane.startLanePoints[rightS].y, 20))
        elif (currentLane.isA('left') and lane.isA('up')) or (currentLane.isA('up') and lane.isA('right')) or (currentLane.isA('right') and lane.isA('down')) or (currentLane.isA('down') and lane.isA('left')):
            self.objectiveDirection = const.RIGHT
            if(rightS == 1):
                # we are on the wrong side
                rightS = 0
                if currentLane.isA('right'):
                    self.waypoints.append(Waypoint(currentLane.endLanePoints[rightS].x/2+const.PROPORTION, currentLane.endLanePoints[rightS].y, 25))
                elif currentLane.isA('left'):
                    self.waypoints.append(Waypoint(currentLane.endLanePoints[rightS].x*4/3-const.PROPORTION, currentLane.endLanePoints[rightS].y, 25))
                elif currentLane.isA('up'):
                    self.waypoints.append(Waypoint(currentLane.endLanePoints[rightS].x, currentLane.endLanePoints[rightS].y*4/3-const.PROPORTION, 25))
                else:
                    self.waypoints.append(Waypoint(currentLane.endLanePoints[rightS].x, currentLane.endLanePoints[rightS].y/2+const.PROPORTION, 25))
            # end of current line
            self.waypoints.append(Waypoint(currentLane.endLanePoints[rightS].x, currentLane.endLanePoints[rightS].y, 10))
            # start of new line
            if currentLane.isA('right'):
                self.waypoints.append(Waypoint(lane.startLanePoints[rightS].x-const.PROPORTION, lane.startLanePoints[rightS].y, 25))
            elif currentLane.isA('left'):
                self.waypoints.append(Waypoint(lane.startLanePoints[rightS].x+const.PROPORTION, lane.startLanePoints[rightS].y, 25))
            elif currentLane.isA('up'):
                self.waypoints.append(Waypoint(lane.startLanePoints[rightS].x, lane.startLanePoints[rightS].y+const.PROPORTION, 25))
            else:
                self.waypoints.append(Waypoint(lane.startLanePoints[rightS].x, lane.startLanePoints[rightS].y-const.PROPORTION, 25))
        else:
            # exit is on the other line
            self.objectiveDirection = const.FORWARD

        # exit of new line
        self.waypoints.append(Waypoint(lane.endLanePoints[rightS].x, lane.endLanePoints[rightS].y, 90))

        #debug
        # for i in self.waypoints:
        #     self.canvas.create_oval(
        #             i.x-5,i.y-5,
        #             i.x+5,i.y+5, fill=const.RED_OFF)
    # predict where it will be in t time

    def predict(self, t=0, objective=None):

        if not t and not objective:
            t=1

        velocity = self.velocity
        degrees = self.degrees
        calc_x = 0
        calc_y = 0
        myp = self.position.clonePosition()

        if not objective:
            for i in range(1, t+1):
                velocity += self.acceleration*self.power
                if velocity > 0:
                    velocity -= self.deceleration/1.5
                if velocity > 0:
                    velocity = round(self.velocity-const.VEHICLE_FRICTION*self.velocity -
                                    math.fabs(self.steerDeg/10), const.FLOAT_PRECISION)
                if velocity < 0:
                    velocity = 0
                degrees += round(self.steerDeg*velocity / (velocity*velocity*1.25+1), const.FLOAT_PRECISION)
                calc_x += round(math.cos(degrees)*velocity *const.VEHICLE_RENDER, const.FLOAT_PRECISION)
                calc_y += round(math.sin(degrees)*velocity *const.VEHICLE_RENDER, const.FLOAT_PRECISION)
            myp.move(calc_x, calc_y)
        # predict a non-linear movement until it moves far away the desidered point
        else:
            # if not (velocity > 0):
            #     return Waypoint(self.position.x, self.position.y, 0, False)
            last_distance = 100000
            count = 0
            while velocity > 0 and last_distance>=Position.distance(myp,objective):
                last_distance = Position.distance(myp,objective)
                velocity += self.acceleration*self.power
                if velocity > 0:
                    velocity -= self.deceleration/1.5
                if velocity > 0:
                    velocity = round(self.velocity-const.VEHICLE_FRICTION*self.velocity -
                                    math.fabs(self.steerDeg/10), const.FLOAT_PRECISION)
                if velocity < 0:
                    velocity = 0
                degrees += round(self.steerDeg*velocity / (velocity*velocity*1.25+1), const.FLOAT_PRECISION)
                calc_x += round(math.cos(degrees)*velocity *const.VEHICLE_RENDER, const.FLOAT_PRECISION)
                calc_y += round(math.sin(degrees)*velocity *const.VEHICLE_RENDER, const.FLOAT_PRECISION)
                myp.move(calc_x, calc_y)

            myp2 = myp.clonePosition()
            myp.move(-calc_x,-calc_y)
            nearestPoint = objective.projection(myp,myp2)
            
            if t and t < count:
                return Waypoint(nearestPoint.x, nearestPoint.y, velocity, False)
            else:
                return Waypoint(myp.x, myp.y, velocity)
            if not myp.near(nearestPoint,20) and velocity > 0:
                return Waypoint(nearestPoint.x, nearestPoint.y, velocity, False)
        return Waypoint(myp.x, myp.y, velocity)

    def predictCollide(self,vehicle,t=1,tollerance=6):
        velocity1 = self.velocity
        degrees1 = self.degrees
        velocity2 = vehicle.velocity
        degrees2 = vehicle.degrees
        
        myp1 = self.position.clonePosition()
        myp2 = vehicle.position.clonePosition()

        distance = myp1.distance(myp2)

        for i in range(1, t+1):
            velocity1 += self.acceleration*self.power
            velocity2 += vehicle.acceleration*vehicle.power
            if velocity1 > 0:
                velocity1 -= self.deceleration/3*2
            if velocity2 > 0:
                velocity2 -= vehicle.deceleration/3*2
            if velocity1 > 0:
                velocity1 = self.velocity - self.velocity*const.VEHICLE_FRICTION - math.fabs(self.steerDeg/10)
            if velocity2 > 0:
                velocity2 = vehicle.velocity - vehicle.velocity*const.VEHICLE_FRICTION - math.fabs(vehicle.steerDeg/10)
            if velocity1 < 0:
                velocity1 = 0
            if velocity2 < 0:
                velocity2 = 0
            degrees1 += self.steerDeg*velocity1 / (velocity1*velocity1*1.25+1)
            degrees2 += vehicle.steerDeg*velocity2 / (velocity2*velocity2*1.25+1)

            oldp1 = myp1.clonePosition()
            oldp2 = myp2.clonePosition()
            myp1.move(math.cos(degrees1)*velocity1 *const.VEHICLE_RENDER,
                        math.sin(degrees1)*velocity1 *const.VEHICLE_RENDER)
            myp2.move(math.cos(degrees2)*velocity2 *const.VEHICLE_RENDER,
                        math.sin(degrees2)*velocity2 *const.VEHICLE_RENDER)
            newDistance=myp1.distance(myp2)
            if newDistance>=distance:
                # from now vehicles are moving away
                if i>1:
                    selfSide00 = Position(self.sides[0].x+oldp1.x-self.position.x,self.sides[0].y+oldp1.y-self.position.y)
                    selfSide01 = Position(self.sides[1].x+oldp1.x-self.position.x,self.sides[1].y+oldp1.y-self.position.y)
                    selfSide02 = Position(self.sides[2].x+oldp1.x-self.position.x,self.sides[2].y+oldp1.y-self.position.y)
                    selfSide03 = Position(self.sides[3].x+oldp1.x-self.position.x,self.sides[3].y+oldp1.y-self.position.y)
                    selfSide10 = Position(vehicle.sides[0].x+oldp2.x-vehicle.position.x,vehicle.sides[0].y+oldp2.y-vehicle.position.y)
                    selfSide11 = Position(vehicle.sides[1].x+oldp2.x-vehicle.position.x,vehicle.sides[1].y+oldp2.y-vehicle.position.y)
                    selfSide12 = Position(vehicle.sides[2].x+oldp2.x-vehicle.position.x,vehicle.sides[2].y+oldp2.y-vehicle.position.y)
                    if (selfSide00.betweenProjection(selfSide10,selfSide11,tollerance) and selfSide00.betweenProjection(selfSide11,selfSide12,tollerance)) or (selfSide01.betweenProjection(selfSide10,selfSide11,tollerance) and selfSide01.betweenProjection(selfSide11,selfSide12,tollerance)) or (selfSide02.betweenProjection(selfSide10,selfSide11,tollerance) and selfSide02.betweenProjection(selfSide11,selfSide12,tollerance)) or (selfSide03.betweenProjection(selfSide10,selfSide11,tollerance) and selfSide03.betweenProjection(selfSide11,selfSide12,tollerance)):
                        return True
                return False
            else:
                distance = newDistance
        # vehicles will move even closer
        selfSide00 = Position(self.sides[0].x+oldp1.x-self.position.x,self.sides[0].y+oldp1.y-self.position.y)
        selfSide01 = Position(self.sides[1].x+oldp1.x-self.position.x,self.sides[1].y+oldp1.y-self.position.y)
        selfSide02 = Position(self.sides[2].x+oldp1.x-self.position.x,self.sides[2].y+oldp1.y-self.position.y)
        selfSide03 = Position(self.sides[3].x+oldp1.x-self.position.x,self.sides[3].y+oldp1.y-self.position.y)
        selfSide10 = Position(vehicle.sides[0].x+oldp2.x-vehicle.position.x,vehicle.sides[0].y+oldp2.y-vehicle.position.y)
        selfSide11 = Position(vehicle.sides[1].x+oldp2.x-vehicle.position.x,vehicle.sides[1].y+oldp2.y-vehicle.position.y)
        selfSide12 = Position(vehicle.sides[2].x+oldp2.x-vehicle.position.x,vehicle.sides[2].y+oldp2.y-vehicle.position.y)
        if (selfSide00.betweenProjection(selfSide10,selfSide11,tollerance) and selfSide00.betweenProjection(selfSide11,selfSide12,tollerance)) or (selfSide01.betweenProjection(selfSide10,selfSide11,tollerance) and selfSide01.betweenProjection(selfSide11,selfSide12,tollerance)) or (selfSide02.betweenProjection(selfSide10,selfSide11,tollerance) and selfSide02.betweenProjection(selfSide11,selfSide12,tollerance)) or (selfSide03.betweenProjection(selfSide10,selfSide11,tollerance) and selfSide03.betweenProjection(selfSide11,selfSide12,tollerance)):
            return True
        return False


    def drive(self,allvehicles):
        if not hasattr(self, 'waypoints') or len(self.waypoints) < 1:
            return
        if self.sensibility > 1:
            self.sensibility = 1
        if self.position.near(self.waypoints[0], 6):
            # we passed the target
            self.waypoints.pop(0)
            if len(self.waypoints) < 1:
                return

        objective = self.waypoints[0]# Waypoint(self.waypoints[0].x,self.waypoints[0].y,self.waypoints[0].velocity)
        futureWaypoint = self.predict(objective=objective)
        rad = round(math.atan2(objective.y-self.position.y,
                               objective.x-self.position.x), const.FLOAT_PRECISION)
        left = self.degrees - rad
        if left < 0:
            left = round(left+math.pi*2, const.FLOAT_PRECISION)
        right = rad - self.degrees
        if right < 0:
            right = round(right+math.pi*2, const.FLOAT_PRECISION)
        if right < left:
            self.steer(right)
        else:
            self.steer(-left)
        
        currentLane,laneN = self.crossroad.getLaneFromPos(self.position)
        objectiveLane,laneObjN = self.crossroad.getLaneFromPos(objective,-1)
        if currentLane and currentLane.isA('entry') and currentLane.tLight.on:
            #we need to check tlight
            currentEndLane = currentLane.endLanePoints[laneN]
            if objectiveLane:
                objectiveEndLane = objectiveLane.endLanePoints[laneObjN]
            else:
                objectiveEndLane = None

            if currentLane.tLight.state==const.TL_RED and not currentEndLane.equals(objectiveEndLane):
                if currentLane.isA('up'):
                    objective=Waypoint(currentEndLane.x,currentEndLane.y+const.PROPORTION*5/2,0)
                elif currentLane.isA('down'):
                    objective=Waypoint(currentEndLane.x,currentEndLane.y-const.PROPORTION*5/2,0)
                elif currentLane.isA('left'):
                    objective=Waypoint(currentEndLane.x+const.PROPORTION*5/2,currentEndLane.y,0)
                elif currentLane.isA('right'):
                    objective=Waypoint(currentEndLane.x-const.PROPORTION*5/2,currentEndLane.y,0)

            if currentLane.tLight.state==const.TL_YELLOW and not currentEndLane.equals(objectiveEndLane):
                if currentLane.isA('up'):
                    objective1=Waypoint(currentEndLane.x,currentEndLane.y+const.PROPORTION,30)
                elif currentLane.isA('down'):
                    objective1=Waypoint(currentEndLane.x,currentEndLane.y-const.PROPORTION,30)
                elif currentLane.isA('left'):
                    objective1=Waypoint(currentEndLane.x+const.PROPORTION,currentEndLane.y,30)
                elif currentLane.isA('right'):
                    objective1=Waypoint(currentEndLane.x-const.PROPORTION,currentEndLane.y,30)
                # in n cycles I would had passed tlight
                canPassTL = self.predict(20,objective1).desidered
                if not canPassTL:
                    objective=objective1
                    objective.velocity=0
#  or Position.distance(self.position,objective)>self.velocity*40
        if (objective.velocity > futureWaypoint.velocity) and futureWaypoint.desidered:
            self.accelerate(self.sensibility)
            #print(self.id,'OK! :) but slow',self.sensibility)
            futureWaypoint = self.predict(objective=objective)
            if objective.velocity > futureWaypoint.velocity:
                self.sensibility += 0.1
                self.accelerate(self.sensibility)
            else:
                self.sensibility = Position.distance(self.position,objective)/80
                self.accelerate(self.sensibility)
        elif not futureWaypoint.desidered and Position.distance(self.position,objective)<self.velocity*10:
            # print(self.id,'i have to turn badly')
            self.sensibility = 0.8#40/Position.distance(self.position,objective)
            self.brake(self.sensibility)
        elif self.velocity>Position.distance(self.position,objective)/100 or objective.velocity < futureWaypoint.velocity:
            # print(self.id,'brake',self.sensibility)
            self.sensibility = 3/Position.distance(self.position,objective)*self.velocity
            self.brake(self.sensibility)
        
        # check for vehicles with more precedence
        for vehicle in allvehicles:
            if vehicle.position.distance(self.position)<300 and (self.crossroad.hasPrecedence(vehicle,self) or (not self.crossroad.hasPrecedence(self,vehicle) and vehicle.id<self.id)):
                if (self.predictCollide(vehicle,40)):
                    self.brake(1)#FIX
                    # print('WARNING',self.id,self.deceleration)
                    break

class Car(Vehicle):
    def __init__(self, canvas, pos, crossroad, tags=[]):
        tags.append('Car')
        super().__init__(canvas, pos, crossroad, tags)
        # SIDES
        self.sides = (
            Position(self.position.x-const.CAR_WIDTH/4,
                     self.position.y-const.CAR_HEIGHT/4),
            Position(self.position.x+const.CAR_WIDTH/4,
                     self.position.y-const.CAR_HEIGHT/4),
            Position(self.position.x+const.CAR_WIDTH/4,
                     self.position.y+const.CAR_HEIGHT/4),
            Position(self.position.x-const.CAR_WIDTH/4,
                     self.position.y+const.CAR_HEIGHT/4)
        )
        # POWER OF THE CAR
        self.power = const.CAR_ACCELERATION
        self.alignToLine()

    def draw(self):
        if not hasattr(self, 'graphic'):
            self.graphic = self.canvas.create_polygon(self.sides[0].x, self.sides[0].y,
                                                      self.sides[1].x, self.sides[1].y,
                                                      self.sides[2].x, self.sides[2].y,
                                                      self.sides[3].x, self.sides[3].y,
                                                      fill=const.RED_ON,outline='black',width=1)
                                                      
# class Truck(Vehicle):
#     def __init__(self, canvas, pos, crossroad, tags=[]):
#         tags.append('Truck')
#         super().__init__(canvas, pos, crossroad, tags)
#         # SIDES
#         self.sides = (
#             Position(self.position.x-const.TRUCK_WIDTH/4,
#                      self.position.y-const.TRUCK_HEIGHT/4),
#             Position(self.position.x+const.TRUCK_WIDTH/4,
#                      self.position.y-const.TRUCK_HEIGHT/4),
#             Position(self.position.x+const.TRUCK_WIDTH/4,
#                      self.position.y+const.TRUCK_HEIGHT/4),
#             Position(self.position.x-const.TRUCK_WIDTH/4,
#                      self.position.y+const.TRUCK_HEIGHT/4)
#         )
#         self.trailer_sides = (
#             Position(self.position.x-const.TRAILER_WIDTH/4,
#                      self.position.y-const.TRAILER_HEIGHT/4),
#             Position(self.position.x+const.TRAILER_WIDTH/4,
#                      self.position.y-const.TRAILER_HEIGHT/4),
#             Position(self.position.x+const.TRAILER_WIDTH/4,
#                      self.position.y+const.TRAILER_HEIGHT/4),
#             Position(self.position.x-const.TRAILER_WIDTH/4,
#                      self.position.y+const.TRAILER_HEIGHT/4)
#         )
#         # POWER OF THE CAR
#         self.power = const.TRUCK_ACCELERATION
#         self.alignToLine()
#         hook1 = Position(math.fabs(self.trailer_sides[0].x-self.trailer_sides[1].x),math.fabs(self.trailer_sides[0].y-self.trailer_sides[1].y))
#         hook2 = Position(math.fabs(self.sides[0].x-self.sides[1].x),math.fabs(self.sides[0].y-self.sides[1].y))
#         self.hookDist = hook1.distance(hook2)

#     def draw(self):
#         if not hasattr(self, 'graphic'):
#             self.graphic = self.canvas.create_polygon(self.sides[0].x, self.sides[0].y,
#                                                       self.sides[1].x, self.sides[1].y,
#                                                       self.sides[2].x, self.sides[2].y,
#                                                       self.sides[3].x, self.sides[3].y,
#                                                       fill=const.WHITE,outline='black',width=1)
#         if not hasattr(self, 'graphic_trailer'):
#             self.graphic_trailer = self.canvas.create_polygon(self.trailer_sides[0].x, self.trailer_sides[0].y,
#                                                       self.trailer_sides[1].x, self.trailer_sides[1].y,
#                                                       self.trailer_sides[2].x, self.trailer_sides[2].y,
#                                                       self.trailer_sides[3].x, self.trailer_sides[3].y,
#                                                       fill=const.BLUE,outline='black',width=1)

class Bus(Vehicle):
    def __init__(self, canvas, pos, crossroad, tags=[]):
        tags.append('Bus')
        super().__init__(canvas, pos, crossroad, tags)
        # SIDES
        self.sides = (
            Position(self.position.x-const.BUS_WIDTH/4,
                     self.position.y-const.BUS_HEIGHT/4),
            Position(self.position.x+const.BUS_WIDTH/4,
                     self.position.y-const.BUS_HEIGHT/4),
            Position(self.position.x+const.BUS_WIDTH/4,
                     self.position.y+const.BUS_HEIGHT/4),
            Position(self.position.x-const.BUS_WIDTH/4,
                     self.position.y+const.BUS_HEIGHT/4)
        )
        # POWER OF THE CAR
        self.power = const.BUS_ACCELERATION
        self.alignToLine()

    def draw(self):
        if not hasattr(self, 'graphic'):
            self.graphic = self.canvas.create_polygon(self.sides[0].x, self.sides[0].y,
                                                      self.sides[1].x, self.sides[1].y,
                                                      self.sides[2].x, self.sides[2].y,
                                                      self.sides[3].x, self.sides[3].y,
                                                      fill=const.BLUE,outline='black',width=1)