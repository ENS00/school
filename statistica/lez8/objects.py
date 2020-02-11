import const
import math
import copy
from random import randint


class GameObject():
    def __init__(self,game):
        self.id = game.idassigner.getNewID()
        self.game = game

    def draw(self):
        raise Exception('Not yet implemented')

    def move(self, x, y):
        self.game.graphic_lib.move(self, round(x, const.FLOAT_PRECISION), round(y, const.FLOAT_PRECISION))
        if hasattr(self, 'position'):
            self.position.move(x, y)
        if hasattr(self, 'sides'):
            for i in self.sides:
                i.move(x, y)

    def moveTo(self, x, y):
        self.game.graphic_lib.moveTo(self, round(x, const.FLOAT_PRECISION), round(y, const.FLOAT_PRECISION))
        if hasattr(self, 'position'):
            self.position.moveTo(x, y)

    def rotate(self, rad):
        self.degrees = self.degrees+rad
        if self.degrees > math.pi:
            self.degrees = self.degrees-math.pi*2
        if self.degrees < -math.pi:
            self.degrees = self.degrees+math.pi*2

        const.ROTATE(self.sides[0], self.position, rad)
        const.ROTATE(self.sides[1], self.position, rad)
        const.ROTATE(self.sides[2], self.position, rad)
        const.ROTATE(self.sides[3], self.position, rad)
        self.game.graphic_lib.setCoords(self, (self.sides[0].x, self.sides[0].y,
                                                self.sides[1].x, self.sides[1].y,
                                                self.sides[2].x, self.sides[2].y,
                                                self.sides[3].x, self.sides[3].y))


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


class TrafficLight(GameObject):
    def __init__(self, posred, direction=const.DOWN, state=const.TL_RED, on=False):
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

    def draw(self,graphic_lib):
        if not (hasattr(self, 'redLight') or hasattr(self, 'yellowLight') or hasattr(self, 'greenLight')):
            self.redLight = graphic_lib.drawCircle(self.posred.x, self.posred.y, const.TL_LIGHT_SIZE, fill=const.RED_OFF)
            self.yellowLight = graphic_lib.drawCircle(self.posyellow.x, self.posyellow.y, const.TL_LIGHT_SIZE, fill=const.YELLOW_OFF)
            self.greenLight = graphic_lib.drawCircle(self.posgreen.x, self.posgreen.y, const.TL_LIGHT_SIZE, fill=const.GREEN_OFF)
            self.graphicitems = (self.redLight, self.yellowLight, self.greenLight)
        if self.state == const.TL_RED:
            graphic_lib.changeColor(self.redLight, const.RED_ON)
            graphic_lib.changeColor(self.yellowLight, const.YELLOW_OFF)
            graphic_lib.changeColor(self.greenLight, const.GREEN_OFF)
        elif self.state == const.TL_YELLOW:
            graphic_lib.changeColor(self.redLight, const.RED_OFF)
            graphic_lib.changeColor(self.yellowLight, const.YELLOW_ON)
            graphic_lib.changeColor(self.greenLight, const.GREEN_OFF)
        elif self.state == const.TL_GREEN:
            graphic_lib.changeColor(self.redLight, const.RED_OFF)
            graphic_lib.changeColor(self.yellowLight, const.YELLOW_OFF)
            graphic_lib.changeColor(self.greenLight, const.GREEN_ON)
        elif self.state == const.TL_OFF:
            graphic_lib.changeColor(self.redLight, const.RED_OFF)
            graphic_lib.changeColor(self.yellowLight, const.YELLOW_OFF)
            graphic_lib.changeColor(self.greenLight, const.GREEN_OFF)


class RoadObject(GameObject):
    def __init__(self, game):
        super().__init__(game)

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
    # now you can instantiate only double direction road
    def __init__(self, pstart, pstop, dim=const.ROAD_LINE_THICKNESS, lineW=const.ROAD_LINE_WIDTH, lineS=const.ROAD_LINE_SIZE):
        self.pstart = pstart
        self.pstop = pstop
        self.dim = dim
        self.lineW = lineW
        self.lineS = lineS
        direction = Position.getDirection(pstart, pstop)

        self.pEntryStart = self.pstart.clonePosition()
        self.pEntryStop = self.pstop.clonePosition()
        self.pExitStop = self.pstart.clonePosition()
        self.pExitStart = self.pstop.clonePosition()
        if 'left' in direction:
            self.pEntryStart.move(0,-dim/2)
            self.pEntryStop.move(0,-dim/2)
            self.pExitStart.move(0,dim/2)
            self.pExitStop.move(0,dim/2)
        elif 'right' in direction:
            self.pEntryStart.move(0,dim/2)
            self.pEntryStop.move(0,dim/2)
            self.pExitStart.move(0,-dim/2)
            self.pExitStop.move(0,-dim/2)
        elif 'up' in direction:
            self.pEntryStart.move(dim/2,0)
            self.pEntryStop.move(dim/2,0)
            self.pExitStart.move(-dim/2,0)
            self.pExitStop.move(-dim/2,0)
        else:
            self.pEntryStart.move(-dim/2,0)
            self.pEntryStop.move(-dim/2,0)
            self.pExitStart.move(dim/2,0)
            self.pExitStop.move(dim/2,0)

        self.entry = Lane(self.pEntryStart,self.pEntryStop,self.dim,self.lineS,self.lineW,tags=['entry'])
        self.exit = Lane(self.pExitStart,self.pExitStop,self.dim,self.lineS,self.lineW,tags=['exit'])

    def draw(self, graphic_lib):
        if not hasattr(self.entry, 'graphicitems'):
            self.entry.draw(graphic_lib)
        if not hasattr(self.exit, 'graphicitems'):
            self.exit.draw(graphic_lib)


class Lane(RoadObject):
    def __init__(self, pstart, pstop, dim, lineS, lineW, tLight=None, tags=[]):
        self.pstart = pstart
        self.pstop = pstop
        self.dim = dim
        self.lineS = lineS
        self.lineW = lineW
        self.tags = Position.getDirection(pstart, pstop)
        self.tags.extend(tags)

        self.defineLanePoints()

    def getSpawnPoints(self):
        if self.isA('left'):
            return (
                Position(self.startLanePoints[0].x+const.BUS_WIDTH, self.startLanePoints[0].y),
                Position(self.startLanePoints[1].x+const.BUS_WIDTH, self.startLanePoints[1].y)
            )
        elif self.isA('right'):
            return (
                Position(self.startLanePoints[0].x-const.BUS_WIDTH, self.startLanePoints[0].y),
                Position(self.startLanePoints[1].x-const.BUS_WIDTH, self.startLanePoints[1].y)
            )
        elif self.isA('up'):
            return (
                Position(self.startLanePoints[0].x, self.startLanePoints[0].y+const.BUS_WIDTH),
                Position(self.startLanePoints[1].x, self.startLanePoints[1].y+const.BUS_WIDTH)
            )
        else:
            return (
                Position(self.startLanePoints[0].x, self.startLanePoints[0].y-const.BUS_WIDTH),
                Position(self.startLanePoints[1].x, self.startLanePoints[1].y-const.BUS_WIDTH)
            )
    def defineLanePoints(self):
        if self.isA('left'):
            self.startLanePoints = (
                Position(self.pstart.x, self.pstart.y+2-const.CAR_HEIGHT/2),
                Position(self.pstart.x, self.pstart.y-2+const.CAR_HEIGHT/2)
            )
            self.endLanePoints = (
                Position(self.pstop.x, self.pstop.y+2-const.CAR_HEIGHT/2),
                Position(self.pstop.x, self.pstop.y-2+const.CAR_HEIGHT/2)
            )
        elif self.isA('right'):
            self.startLanePoints = (
                Position(self.pstart.x, self.pstart.y-2+const.CAR_HEIGHT/2),
                Position(self.pstart.x, self.pstart.y+2-const.CAR_HEIGHT/2)
            )
            self.endLanePoints = (
                Position(self.pstop.x, self.pstop.y-2+const.CAR_HEIGHT/2),
                Position(self.pstop.x, self.pstop.y+2-const.CAR_HEIGHT/2)
            )
        elif self.isA('up'):
            self.startLanePoints = (
                Position(self.pstart.x-2+const.CAR_HEIGHT/2, self.pstart.y),
                Position(self.pstart.x+2-const.CAR_HEIGHT/2, self.pstart.y)
            )
            self.endLanePoints = (
                Position(self.pstop.x-2+const.CAR_HEIGHT/2, self.pstop.y),
                Position(self.pstop.x+2-const.CAR_HEIGHT/2, self.pstop.y)
            )
        else:
            self.startLanePoints = (
                Position(self.pstart.x+2-const.CAR_HEIGHT/2, self.pstart.y),
                Position(self.pstart.x-2+const.CAR_HEIGHT/2, self.pstart.y)
            )
            self.endLanePoints = (
                Position(self.pstop.x+2-const.CAR_HEIGHT/2, self.pstop.y),
                Position(self.pstop.x-2+const.CAR_HEIGHT/2, self.pstop.y)
            )

    def draw(self, graphic_lib):
        if not hasattr(self, 'graphicitems'):
            if self.isA('left') or self.isA('right'):
                # draw road
                self.graphicitems = [graphic_lib.drawRect(self.pstart.x, self.pstart.y-self.dim/2,
                                                    self.pstop.x, self.pstart.y+self.dim/2,
                                                    fill=const.COLOR_ROAD, border=0)]
                # draw border lines
                self.graphicitems.append(graphic_lib.drawRect(self.pstart.x, self.pstart.y-self.dim/2+const.PROPORTION/4,
                                                        self.pstop.x, self.pstart.y-self.dim/2-const.PROPORTION/4,
                                                        fill=const.WHITE, border=0))
                self.graphicitems.append(graphic_lib.drawRect(self.pstart.x, self.pstart.y+self.dim/2+const.PROPORTION/4,
                                                        self.pstop.x, self.pstart.y+self.dim/2-const.PROPORTION/4,
                                                        fill=const.WHITE, border=0))
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
                    self.graphicitems.append(graphic_lib.drawRect(posx, self.pstart.y-self.dim/24,
                                                            posx+self.lineW, self.pstart.y+self.dim/24,
                                                            fill=const.WHITE, border=0))
                # draw stop line
                if self.isA('entry'):
                    self.graphicitems.append(graphic_lib.drawRect(self.pstop.x, self.pstart.y-self.dim/2,
                                                            self.pstop.x-stopline, self.pstart.y+self.dim/2,
                                                            fill=const.WHITE, border=0))
            else:
                self.graphicitems = [graphic_lib.drawRect(self.pstart.x-self.dim/2, self.pstart.y,
                                                        self.pstart.x+self.dim/2, self.pstop.y,
                                                        fill=const.COLOR_ROAD, border=0)]
                # draw border lines
                self.graphicitems.append(graphic_lib.drawRect(self.pstart.x-self.dim/2+const.PROPORTION/4, self.pstart.y,
                                                        self.pstart.x-self.dim/2-const.PROPORTION/4, self.pstop.y,
                                                        fill=const.WHITE, border=0))
                self.graphicitems.append(graphic_lib.drawRect(self.pstart.x+self.dim/2+const.PROPORTION/4, self.pstart.y,
                                                        self.pstart.x+self.dim/2-const.PROPORTION/4, self.pstop.y,
                                                        fill=const.WHITE, border=0))
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
                    self.graphicitems.append(graphic_lib.drawRect(self.pstart.x-self.dim/24, posy,
                                                            self.pstart.x+self.dim/24, posy+self.lineW,
                                                            fill=const.WHITE, border=0))
                # draw stop line
                if self.isA('entry'):
                    self.graphicitems.append(graphic_lib.drawRect(self.pstart.x-self.dim/2, self.pstop.y,
                                                            self.pstart.x+self.dim/2, self.pstop.y-stopline,
                                                            fill=const.WHITE, border=0))

    def createTrafficLight(self, status=const.TL_RED):
        if hasattr(self,'tLight'):
            self.removeTrafficLight()

        # self.tags.remove('exit')
        # self.tags.append('entry')
        if(self.isA('entry')):
            self.tLight = None
            # create the tl near the right side of the road
            if self.isA('down'):
                self.tLight = TrafficLight(Position(self.endLanePoints[0].x-const.TL_DIST_X, self.endLanePoints[0].y-const.TL_DIST_Y),
                                        const.DOWN,status)
            elif self.isA('up'):
                self.tLight = TrafficLight(Position(self.endLanePoints[0].x+const.TL_DIST_X, self.endLanePoints[0].y+const.TL_DIST_Y),
                                        const.UP,status)
            elif self.isA('left'):
                self.tLight = TrafficLight(Position(self.endLanePoints[0].x+const.TL_DIST_Y, self.endLanePoints[0].y-const.TL_DIST_X),
                                        const.LEFT,status)
            elif self.isA('right'):
                self.tLight = TrafficLight(Position(self.endLanePoints[0].x-const.TL_DIST_Y, self.endLanePoints[0].y+const.TL_DIST_X),
                                        const.RIGHT,status)
            return self.tLight
        
        raise Exception('Please be sure to tell to an "entry" road to create traffic light')

    def removeTrafficLight(self):
        self.tags.remove('entry')
        self.tags.append('exit')
        del self.tLight

    # do not clone me
    def __deepcopy__(self,memo=None):
        return self


class Crossroad(RoadObject):
    def __init__(self, roads):
        self.entries = [i.entry for i in roads]
        self.exits = [i.exit for i in roads]
        # assuming all lanes have equal dimensions
        self.dim = self.entries[0].dim
        minpstop = Position(20000, 20000)
        maxpstop = Position(0, 0)
        for i in self.exits:
            if i.isA('left'):
                i.pstart.move(-i.dim,0)
            elif i.isA('right'):
                i.pstart.move(i.dim,0)
            elif i.isA('up'):
                i.pstart.move(0,-i.dim)
            else:
                i.pstart.move(0,i.dim)
            # refresh start/end lane positions
            i.defineLanePoints()
            i.crossroad = self
        for i in self.entries:
            if i.isA('left'):
                i.pstop.move(i.dim,0)
            elif i.isA('right'):
                i.pstop.move(-i.dim,0)
            elif i.isA('up'):
                i.pstop.move(0,i.dim)
            else:
                i.pstop.move(0,-i.dim)
            # refresh start/end lane positions
            i.defineLanePoints()
            i.crossroad = self
            if i.pstop.x < minpstop.x:
                minpstop.x = i.pstop.x
            if i.pstop.y < minpstop.y:
                minpstop.y = i.pstop.y
            if i.pstop.x > maxpstop.x:
                maxpstop.x = i.pstop.x
            if i.pstop.y > maxpstop.y:
                maxpstop.y = i.pstop.y
            # create its own traffic light
            if i.isA('up') or i.isA('down'):
                i.createTrafficLight(const.TL_RED)
            else:
                i.createTrafficLight(const.TL_GREEN)
        self.points = (Position(minpstop.x, minpstop.y), Position(maxpstop.x, minpstop.y),
                       Position(minpstop.x, maxpstop.y), Position(maxpstop.x, maxpstop.y))

    def draw(self,graphic_lib):
        if not hasattr(self, 'graphic'):
            self.graphic = graphic_lib.drawRect(self.points[0].x, self.points[0].y,
                                                self.points[3].x, self.points[3].y,
                                                fill=const.COLOR_ROAD, border=0)
        for i in self.exits:
            i.draw(graphic_lib)
        for i in self.entries:
            i.draw(graphic_lib)
            i.tLight.draw(graphic_lib)

    def updateTLights(self):
        for i in self.entries:
            i.tLight.update()

    def turnOnTLights(self,turnOn=True):
        if turnOn:
            for i in self.entries:
                i.tLight.turnOn()
        else:
            for i in self.entries:
                i.tLight.turnOff()
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
    
    def randomEntry(self):
        return self.entries[randint(0,3)]

    def getOppositeLanes(self,vehicle,direction=const.FORWARD):
        road = vehicle.spawnLine#TODO!!!!
        if direction==const.RIGHT:
            if road.isA('up'):
                return [lane for lane in self.exits if lane.isA('right')]
            elif road.isA('down'):
                return [lane for lane in self.exits if lane.isA('left')]
            elif road.isA('left'):
                return [lane for lane in self.exits if lane.isA('up')]
            else:
                return [lane for lane in self.exits if lane.isA('down')]
        elif direction==const.LEFT:
            if road.isA('up'):
                return [lane for lane in self.exits if lane.isA('left')]
            elif road.isA('down'):
                return [lane for lane in self.exits if lane.isA('right')]
            elif road.isA('left'):
                return [lane for lane in self.exits if lane.isA('down')]
            else:
                return [lane for lane in self.exits if lane.isA('up')]
        else:
            if road.isA('up'):
                return [lane for lane in self.exits if lane.isA('up')]
            elif road.isA('down'):
                return [lane for lane in self.exits if lane.isA('down')]
            elif road.isA('left'):
                return [lane for lane in self.exits if lane.isA('left')]
            else:
                return [lane for lane in self.exits if lane.isA('right')]
    
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

    # do not clone me
    def __deepcopy__(self,memo=None):
        return self
        


class Vehicle(RoadObject):
    def __init__(self, game, crossroad, line, side, tags=[]):
        super().__init__(game)
        self.position = line.getSpawnPoints()[side]
        self.tags = tags
        self.velocity = const.VEHICLE_SPAWN_SPEED
        self.degrees = 0
        self.steerDeg = 0
        self.acceleration = 0
        self.deceleration = 0
        self.sensibility = 1
        self.crossroad = crossroad
        self.spawnLine = line
        self.spawnSide = side
        self.arrived = False

    def clone(self):
        return copy.deepcopy(self)

    def draw(self):
        # not implemented in father class
        pass

    def alignToLine(self):
        if self.spawnLine.isA('up'):
            self.rotate(-math.pi/2)
            self.spawnDirection = const.UP
        elif self.spawnLine.isA('down'):
            self.rotate(math.pi/2)
            self.spawnDirection = const.DOWN
        elif self.spawnLine.isA('left'):
            self.rotate(math.pi)
            self.spawnDirection = const.LEFT
        else:
            self.spawnDirection = const.RIGHT

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
            currentLane = self.spawnLine
            rightS = self.spawnSide
            if currentLane == None or rightS == None:
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
        #     self.game.graphic_lib.drawCircle(
        #             i.x,i.y,5, fill=const.RED_OFF)
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
                # TODO check right sides!!
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
                self.arrived = True
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
                if currentLane.isA('up'):#IDEA!! +self.sides[0].y-self.position.y
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
    def __init__(self, game, crossroad, line, side=randint(0,1), tags=[]):
        tags.append('Car')
        super().__init__(game, crossroad, line, side, tags=tags)
        # SIDES
        self.sides = (
            Position(self.position.x+const.CAR_WIDTH/4,
                     self.position.y-const.CAR_HEIGHT/4),
            Position(self.position.x+const.CAR_WIDTH/4,
                     self.position.y+const.CAR_HEIGHT/4),
            Position(self.position.x-const.CAR_WIDTH/4,
                     self.position.y+const.CAR_HEIGHT/4),
            Position(self.position.x-const.CAR_WIDTH/4,
                     self.position.y-const.CAR_HEIGHT/4)
        )
        # POWER OF THE CAR
        self.power = const.CAR_ACCELERATION
        self.alignToLine()

    def draw(self,graphic_lib):
        if not hasattr(self, 'graphic'):
            self.graphic = graphic_lib.drawRect(self.sides[0].x, self.sides[0].y,
                                                self.sides[2].x, self.sides[2].y,
                                                fill=const.RANDOM_COLOR(),outline='black',border=1)
                                                      
class Bus(Vehicle):
    def __init__(self, game, crossroad, line, side=randint(0,1), tags=[]):
        tags.append('Bus')
        super().__init__(game, crossroad, line, side, tags=tags)
        # SIDES
        self.sides = (
            Position(self.position.x+const.BUS_WIDTH/4,
                     self.position.y-const.BUS_HEIGHT/4),
            Position(self.position.x+const.BUS_WIDTH/4,
                     self.position.y+const.BUS_HEIGHT/4),
            Position(self.position.x-const.BUS_WIDTH/4,
                     self.position.y+const.BUS_HEIGHT/4),
            Position(self.position.x-const.BUS_WIDTH/4,
                     self.position.y-const.BUS_HEIGHT/4)
        )
        # POWER OF THE CAR
        self.power = const.BUS_ACCELERATION
        self.alignToLine()

    def draw(self,graphic_lib):
        if not hasattr(self, 'graphic'):
            self.graphic = graphic_lib.drawRect(self.sides[0].x, self.sides[0].y,
                                                self.sides[2].x, self.sides[2].y,
                                                fill=const.RANDOM_COLOR(),outline='black',border=1)