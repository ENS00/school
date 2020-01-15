import const
import math


class GraphicObject():
    def __init__(self, canvas):
        self.canvas = canvas
        self.id = canvas.idassigner.getNewID()

    def draw(self):
        raise Exception('Not yet implemented')

    def move(self, x, y):
        if hasattr(self, 'graphicitems'):
            [self.canvas.move(self.graphicitems[i], round(x, const.FLOAT_PRECISION), round(y, const.FLOAT_PRECISION))
             for i in self.graphicitems]
        if hasattr(self, 'graphic'):
            self.canvas.move(self.graphic, round(x, const.FLOAT_PRECISION), round(y, const.FLOAT_PRECISION))
        if hasattr(self, 'position'):
            self.position.move(x, y)
        if hasattr(self, 'sides'):
            for i in self.sides:
                i.move(x, y)

    def moveTo(self, x, y):
        if hasattr(self, 'graphicitems'):
            [self.canvas.moveTo(self.graphicitems[i], round(x, const.FLOAT_PRECISION), round(y, const.FLOAT_PRECISION))
             for i in self.graphicitems]
        if hasattr(self, 'graphic'):
            self.canvas.moveTo(self.graphic, round(x, const.FLOAT_PRECISION), round(y, const.FLOAT_PRECISION))
        if hasattr(self, 'position'):
            self.position.moveTo(x, y)

    def rotate(self, rad):
        self.degrees = round(self.degrees+rad, const.FLOAT_PRECISION)
        if self.degrees > math.pi:
            self.degrees = round(self.degrees-math.pi*2, const.FLOAT_PRECISION)
        if self.degrees < -math.pi:
            self.degrees = round(self.degrees+math.pi*2, const.FLOAT_PRECISION)

        def _rot(x, y):
            # note: the rotation is done in the opposite fashion from for a right-handed coordinate system due to the left-handedness of computer coordinates
            x -= self.position.x
            y -= self.position.y
            _x = x * math.cos(-rad) + y * math.sin(-rad)
            _y = -x * math.sin(-rad) + y * math.cos(-rad)
            return _x + self.position.x, _y + self.position.y

        x, y = _rot(self.sides[0].x, self.sides[0].y)
        self.sides[0].moveTo(x, y)
        x, y = _rot(self.sides[1].x, self.sides[1].y)
        self.sides[1].moveTo(x, y)
        x, y = _rot(self.sides[2].x, self.sides[2].y)
        self.sides[2].moveTo(x, y)
        x, y = _rot(self.sides[3].x, self.sides[3].y)
        self.sides[3].moveTo(x, y)
        if hasattr(self, 'graphic'):
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
        self.x = round(self.x+x, const.FLOAT_PRECISION)
        self.y = round(self.y+y, const.FLOAT_PRECISION)
    # this point is between two points?

    def between(self, pos1, pos2, sensibility=2):
        projectionPoint = self.projection(pos1,pos2)
        if (projectionPoint.x <= pos1.x+sensibility and projectionPoint.x >= pos2.x-sensibility) or (projectionPoint.x >= pos1.x-sensibility and projectionPoint.x <= pos2.x+sensibility):
            if projectionPoint.y <= pos1.y+sensibility and projectionPoint.y >= pos2.y-sensibility:
                return True
            if projectionPoint.y >= pos1.y-sensibility and projectionPoint.y <= pos2.y+sensibility:
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

    def near(self, pos, sensibility=2):
        if self.x <= pos.x+sensibility and self.x >= pos.x-sensibility and self.y <= pos.y+sensibility and self.y >= pos.y-sensibility:
            return True
        return False

    def distance(self, pos):
        return math.sqrt(math.pow(self.x-pos.x, 2)+math.pow(self.y-pos.y, 2))
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
        return self.x==pos.x and self.y==pos.y

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
                # draw white lines
                step = self.lineS+self.lineW
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
                step = self.lineS+self.lineW
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
                if super().isA('entry'):
                    self.graphicitems.append(self.canvas.create_rectangle(self.pstart.x-self.dim/2, self.pstop.y,
                                                                          self.pstart.x+self.dim/2, self.pstop.y-stopline,
                                                                          fill=const.WHITE, width=0))


class Lane(Road):
    # pstart and pstop centered
    def __init__(self, canvas, pstart, pstop, tLight=None, dim=const.CAR_HEIGHT*1.5):
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

    def getLaneFromPos(self, pos):
        for i in self.entries:
            if pos.between(i.startLanePoints[0], i.endLanePoints[0]):
                return i, 0
            if pos.between(i.startLanePoints[1], i.endLanePoints[1]):
                return i, 1
        for i in self.exits:
            if pos.between(i.startLanePoints[0], i.endLanePoints[0]):
                return i, 0
            if pos.between(i.startLanePoints[1], i.endLanePoints[1]):
                return i, 1
        # this point is not in a lane
        return None, None
    
    def hasPrecedence(self,pos1,pos2):
        lanePos1,laneN1 = self.getLaneFromPos(pos1)
        lanePos2,laneN2 = self.getLaneFromPos(pos2)
        if lanePos1 and lanePos2:
            if(lanePos1.isA('up') and lanePos2.isA('right')):
                return True
            if(lanePos1.isA('left') and lanePos2.isA('up')):
                return True
            if(lanePos1.isA('down') and lanePos2.isA('left')):
                return True
            if(lanePos1.isA('right') and lanePos2.isA('down')):
                return True
        return False

class Car(RoadObject):
    def __init__(self, canvas, pos, tags=[]):
        super().__init__(canvas)
        self.position = pos.clonePosition()
        self.tags = tags
        self.velocity = 50
        self.degrees = 0
        self.steerDeg = 0
        self.acceleration = 0
        self.deceleration = 0
        self.sensibility = 1
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

    def draw(self):
        if not hasattr(self, 'graphic'):
            self.graphic = self.canvas.create_polygon(self.sides[0].x, self.sides[0].y,
                                                      self.sides[1].x, self.sides[1].y,
                                                      self.sides[2].x, self.sides[2].y,
                                                      self.sides[3].x, self.sides[3].y,
                                                      fill=const.RED_ON, width=0)

    def update(self):
        self.velocity += self.acceleration*249/1200
        if self.velocity > 0:
            self.velocity -= self.deceleration/1.5
        self.acceleration = 0
        self.deceleration = 0
        if self.velocity > 0:
            self.velocity = round(self.velocity-0.0006*self.velocity - math.fabs(self.steerDeg/10), const.FLOAT_PRECISION)
        if self.velocity < 0:
            self.velocity = 0
        self.rotate(self.steerDeg*self.velocity / (self.velocity*self.velocity*1.2+const.CAR_MAX_SPEED))
        calc_x = round(math.cos(self.degrees)*self.velocity / 6*const.CAR_POWER, const.FLOAT_PRECISION)
        calc_y = round(math.sin(self.degrees)*self.velocity / 6*const.CAR_POWER, const.FLOAT_PRECISION)
        self.move(calc_x, calc_y)

    def steer(self, pow=const.CAR_POWER):
        if pow < -1:
            pow = -1
        if pow > 1:
            pow = 1
        self.steerDeg = round(pow,const.FLOAT_PRECISION)

    def accelerate(self, pow=const.CAR_POWER):
        if pow < 0:
            pow = 0
        if pow > 1:
            pow = 1
        self.acceleration = pow*pow
        self.deceleration = 0

    def brake(self, pow=const.CAR_POWER):
        if pow < 0:
            pow = 0
        if pow > 1:
            pow = 1
        self.deceleration = pow*pow
        self.acceleration = 0
    # we tell to the car where to go and we set a step by step guide to get there

    def setObjective(self, lane):
        self.waypoints = []
        if not lane.isA('exit'):
            raise Exception('Lane selected is not an exit')
        self.crossroad = lane.crossroad
        currentLane, rightS = self.crossroad.getLaneFromPos(self.position)
        # straight the car with the lane
        if currentLane.isA('up'):
            self.rotate(-math.pi/2)
        elif currentLane.isA('down'):
            self.rotate(math.pi/2)
        elif currentLane.isA('left'):
            self.rotate(math.pi)
        if not currentLane:
            raise Exception('This object is not in a lane')
        if not currentLane.isA('entry'):
            raise Exception('Cannot set objective when the car is already leaving')
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
                self.waypoints.append(Waypoint(currentLane.endLanePoints[rightS].x/2, currentLane.endLanePoints[rightS].y, self.velocity))
            # end of current line
            self.waypoints.append(Waypoint(currentLane.endLanePoints[rightS].x+50, currentLane.endLanePoints[rightS].y, 10))
            # start of new line
            self.waypoints.append(Waypoint(lane.startLanePoints[rightS].x, lane.startLanePoints[rightS].y, 20))
        elif (currentLane.isA('left') and lane.isA('up')) or (currentLane.isA('up') and lane.isA('right')) or (currentLane.isA('right') and lane.isA('down')) or (currentLane.isA('down') and lane.isA('left')):
            self.objectiveDirection = const.RIGHT
            if(rightS == 1):
                # we are on the wrong side
                rightS = 0
                self.waypoints.append(Waypoint(currentLane.endLanePoints[rightS].x/2, currentLane.endLanePoints[rightS].y, self.velocity))
            # end of current line
            self.waypoints.append(Waypoint(currentLane.endLanePoints[rightS].x, currentLane.endLanePoints[rightS].y, 10))
            # start of new line
            self.waypoints.append(Waypoint(lane.startLanePoints[rightS].x, lane.startLanePoints[rightS].y, 20))
        else:
            # exit is on the other line
            if(rightS == 1):
                rightS = 0
            else:
                rightS = 1
            self.objectiveDirection = const.FORWARD

        # exit of new line
        self.waypoints.append(Waypoint(lane.endLanePoints[rightS].x, lane.endLanePoints[rightS].y, const.CAR_MAX_SPEED))

        # self.canvas.create_oval(
        #         currentLane.endLanePoints[rightS].x-45,currentLane.endLanePoints[rightS].y-5,
        #         currentLane.endLanePoints[rightS].x-35,currentLane.endLanePoints[rightS].y+5, fill=const.RED_OFF)
        # self.canvas.create_oval(
        #         lane.startLanePoints[rightS].x-5,lane.startLanePoints[rightS].y-5,
        #         lane.startLanePoints[rightS].x+5,lane.startLanePoints[rightS].y+5, fill=const.RED_OFF)
        # self.canvas.create_oval(
        #         357.00899-5,348.55417-5,
        #         357.00899+5,348.55417+5, fill=const.RED_OFF)
    # predict where it will be in t time

    def predict(self, t=0, objective=None):
        if not t and not objective:
            t=1
        # t = int(t*100)
        velocity = self.velocity
        degrees = self.degrees

        calc_x = 0
        calc_y = 0
        myp = self.position.clonePosition()
        if not objective:
            for i in range(1, t+1):
                velocity += self.acceleration*249/1200
                if velocity > 0:
                    velocity -= self.deceleration/1.5
                if velocity > 0:
                    velocity = round(self.velocity-0.0006*self.velocity -
                                    math.fabs(self.steerDeg/10), const.FLOAT_PRECISION)
                if velocity < 0:
                    velocity = 0
                degrees += round(self.steerDeg*velocity / (velocity*velocity*1.2+const.CAR_MAX_SPEED), const.FLOAT_PRECISION)
                calc_x += round(math.cos(degrees)*velocity / 6*const.CAR_POWER, const.FLOAT_PRECISION)
                calc_y += round(math.sin(degrees)*velocity / 6*const.CAR_POWER, const.FLOAT_PRECISION)
            myp.move(calc_x, calc_y)
        # predict a non-linear movement until it moves far away the desidered point
        else:
            last_distance = 100000
            count = 0
            while velocity > 0 and last_distance>=Position.distance(myp,objective):
                last_distance = Position.distance(myp,objective)
                velocity += self.acceleration*249/1200
                if velocity > 0:
                    velocity -= self.deceleration/1.5
                if velocity > 0:
                    velocity = round(self.velocity-0.0006*self.velocity -
                                    math.fabs(self.steerDeg/10), const.FLOAT_PRECISION)
                if velocity < 0:
                    velocity = 0
                degrees += round(self.steerDeg*velocity / (velocity*velocity*1.2+const.CAR_MAX_SPEED), const.FLOAT_PRECISION)
                calc_x += round(math.cos(degrees)*velocity / 6*const.CAR_POWER, const.FLOAT_PRECISION)
                calc_y += round(math.sin(degrees)*velocity / 6*const.CAR_POWER, const.FLOAT_PRECISION)
                myp.move(calc_x, calc_y)
                count += 1
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
    # decide what to do...

    def drive(self,allcars):
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
            self.steer(right)#+0.2
        else:
            self.steer(-left)#-0.2
        
        currentLane,laneN = self.crossroad.getLaneFromPos(self.position)
        objectiveLane,laneObjN = self.crossroad.getLaneFromPos(objective)
        if currentLane and currentLane.isA('entry') and currentLane.tLight.on:
            #we need to check tlight
            currentEndLane = currentLane.endLanePoints[laneN]
            objectiveEndLane = objectiveLane.endLanePoints[laneObjN]

            # print(futureWaypoint,objective,futureWaypoint.desidered)
            if currentLane.tLight.state==const.TL_RED and not currentEndLane.equals(objectiveEndLane):
                if currentLane.isA('up'):
                    objective=Waypoint(currentEndLane.x,currentEndLane.y+10,0)
                elif currentLane.isA('down'):
                    objective=Waypoint(currentEndLane.x,currentEndLane.y-10,0)
                elif currentLane.isA('left'):
                    objective=Waypoint(currentEndLane.x+10,currentEndLane.y,0)
                elif currentLane.isA('right'):
                    objective=Waypoint(currentEndLane.x-10,currentEndLane.y,0)

            if currentLane.tLight.state==const.TL_YELLOW and not currentEndLane.equals(objectiveEndLane):
                if currentLane.isA('up'):
                    objective1=Waypoint(currentEndLane.x,currentEndLane.y+10,0)
                elif currentLane.isA('down'):
                    objective1=Waypoint(currentEndLane.x,currentEndLane.y-10,0)
                elif currentLane.isA('left'):
                    objective1=Waypoint(currentEndLane.x+10,currentEndLane.y,0)
                elif currentLane.isA('right'):
                    objective1=Waypoint(currentEndLane.x-10,currentEndLane.y,0)
                # in n cycles I would had passed tlight
                canPassTL = self.predict(15,objective1).desidered
                if not canPassTL:
                    objective=objective1

        if (objective.velocity > futureWaypoint.velocity or Position.distance(self.position,objective)>self.velocity*20) and futureWaypoint.desidered:
            self.accelerate(self.sensibility)
            # print('OK! :) but slow',self.sensibility)
            futureWaypoint = self.predict(objective=objective)
            if objective.velocity > futureWaypoint.velocity:
                self.sensibility += 0.1
                self.accelerate(self.sensibility)
            else:
                self.sensibility = Position.distance(self.position,objective)/80
                self.accelerate(self.sensibility)
        elif not futureWaypoint.desidered and Position.distance(self.position,objective)<self.velocity*10:
            # print('i have to turn badly')
            self.sensibility = 0.8#40/Position.distance(self.position,objective)
            self.brake(self.sensibility)
        elif self.velocity>Position.distance(self.position,objective)/100 or objective.velocity < futureWaypoint.velocity:
            # print('i have to turn',self.sensibility)
            self.sensibility = 100/Position.distance(self.position,objective)
            self.brake(self.sensibility)
        
        # check for cars with more precedence
        for car in allcars:
            if car.position.distance(self.position)<300 and (self.crossroad.hasPrecedence(car.position,self.position) or (not self.crossroad.hasPrecedence(self.position,car.position) and car.id<self.id)):
                for i in range(int(car.position.distance(self.position)/10),40):
                    ### TO DO FUNCTION
                    myFuturePos = self.predict(i)
                    selfSide00 = Position(self.sides[0].x+myFuturePos.x-self.position.x,self.sides[0].y+myFuturePos.y-self.position.y)
                    selfSide01 = Position(self.sides[1].x+myFuturePos.x-self.position.x,self.sides[1].y+myFuturePos.y-self.position.y)
                    selfSide02 = Position(self.sides[2].x+myFuturePos.x-self.position.x,self.sides[2].y+myFuturePos.y-self.position.y)
                    selfSide03 = Position(self.sides[3].x+myFuturePos.x-self.position.x,self.sides[3].y+myFuturePos.y-self.position.y)
                    futurePosition = car.predict(i)
                    selfSide10 = Position(car.sides[0].x+futurePosition.x-car.position.x,car.sides[0].y+futurePosition.y-car.position.y)
                    selfSide11 = Position(car.sides[1].x+futurePosition.x-car.position.x,car.sides[1].y+futurePosition.y-car.position.y)
                    selfSide12 = Position(car.sides[2].x+futurePosition.x-car.position.x,car.sides[2].y+futurePosition.y-car.position.y)
                    ###
                    # print(futurePosition,futurePosition.projection(selfSide0,selfSide1),selfSide0,selfSide1)
                    # print(futurePosition,futurePosition.projection(selfSide1,selfSide2),selfSide1,selfSide2)
                    if (selfSide00.between(selfSide10,selfSide11,0) and selfSide00.between(selfSide11,selfSide12,0)) or (selfSide01.between(selfSide10,selfSide11,0) and selfSide01.between(selfSide11,selfSide12,0)) or (selfSide02.between(selfSide10,selfSide11,0) and selfSide02.between(selfSide11,selfSide12,0)) or (selfSide03.between(selfSide10,selfSide11,0) and selfSide03.between(selfSide11,selfSide12,0)):
                        self.brake(150/Position.distance(futurePosition,myFuturePos))
                        print('WARNING',self.id,self.deceleration)
                        break