import const
import math


class GraphicObject():
    def __init__(self, canvas):
        self.canvas = canvas

    def draw(self):
        raise Exception('Not yet implemented')

    def move(self, x, y):
        if hasattr(self, 'graphicitems'):
            [self.canvas.move(self.graphicitems[i], round(x,const.FLOAT_PRECISION), round(y,const.FLOAT_PRECISION))
             for i in self.graphicitems]
        if hasattr(self, 'graphic'):
            self.canvas.move(self.graphic, round(x,const.FLOAT_PRECISION), round(y,const.FLOAT_PRECISION))
        if hasattr(self, 'position'):
            self.position.move(x, y)
        if hasattr(self, 'sides'):
            for i in self.sides:
                i.move(x, y)

    def moveTo(self, x, y):
        if hasattr(self, 'graphicitems'):
            [self.canvas.moveTo(self.graphicitems[i], round(x,const.FLOAT_PRECISION), round(y,const.FLOAT_PRECISION))
             for i in self.graphicitems]
        if hasattr(self, 'graphic'):
            self.canvas.moveTo(self.graphic, round(x,const.FLOAT_PRECISION), round(y,const.FLOAT_PRECISION))
        if hasattr(self, 'position'):
            self.position.moveTo(x, y)

    def rotate(self, rad):
        self.degrees = round(self.degrees+rad,const.FLOAT_PRECISION)
        if self.degrees > math.pi:
            self.degrees=round(self.degrees-math.pi*2,const.FLOAT_PRECISION)
        if self.degrees < -math.pi:
            self.degrees=round(self.degrees+math.pi*2,const.FLOAT_PRECISION)

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
        self.x = x
        self.y = y

    def move(self, x, y):
        self.x=round(self.x+x,const.FLOAT_PRECISION)
        self.y=round(self.y+y,const.FLOAT_PRECISION)
    # this point is between two points?

    def between(self, pos1, pos2):
        sensibility=2
        if (self.x <= pos1.x+sensibility and self.x >= pos2.x-sensibility) or (self.x >= pos1.x-sensibility and self.x <= pos2.x+sensibility):
            if self.y <= pos1.y+sensibility and self.y >= pos2.y-sensibility:
                return True
            if self.y >= pos1.y-sensibility and self.y <= pos2.y+sensibility:
                return True
        return False
    
    def near(self,pos,sensibility=2):
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

class Waypoint(Position):
    def __init__(self, x, y, velocity=0):
        # position of waypoint
        super().__init__(x,y)
        # target velocity
        self.velocity=velocity

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
                    road_lines = range(round(self.pstart.y),round(self.pstop.y), step)
                    stopline = self.lineS+2
                else:
                    road_lines = range(round(self.pstop.y),round(self.pstart.y), step)
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
   
    def createTrafficLight(self,status=const.TL_RED):
        self.tags.remove('exit')
        self.tags.append('entry')
        self.tLight = None
        # create the tl near the right side of the road
        if self.isA('down'):
            self.tLight = TrafficLight(self.canvas,
                                        Position(self.endLanePoints[0].x-const.TL_DIST_X, self.endLanePoints[0].y-const.TL_DIST_Y),
                                        const.DOWN,
                                        status)
        elif self.isA('up'):
            self.tLight = TrafficLight(self.canvas,
                                        Position(self.endLanePoints[0].x+const.TL_DIST_X, self.endLanePoints[0].y+const.TL_DIST_Y),
                                        const.UP,
                                        status)
        elif self.isA('left'):
            self.tLight = TrafficLight(self.canvas,
                                        Position(self.endLanePoints[0].x+const.TL_DIST_Y, self.endLanePoints[0].y-const.TL_DIST_X),
                                        const.LEFT,
                                        status)
        elif self.isA('right'):
            self.tLight = TrafficLight(self.canvas,
                                        Position(self.endLanePoints[0].x-const.TL_DIST_Y, self.endLanePoints[0].y+const.TL_DIST_X),
                                        const.RIGHT,
                                        status)
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


class Car(RoadObject):
    def __init__(self, canvas, pos, tags=[]):
        super().__init__(canvas)
        self.position = pos
        self.tags = tags
        self.velocity = 50
        self.degrees = 0
        self.steerDeg = 0
        self.acceleration=0
        self.deceleration=0
        self.sensibility=1
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
        if self.velocity < const.CAR_MAX_SPEED:
            self.velocity += self.acceleration
        if self.velocity > 0:
            self.velocity -= self.deceleration*4
        self.acceleration=0
        self.deceleration=0
        if self.velocity > 0:
            self.velocity = round(self.velocity-0.004*self.velocity-math.fabs(self.steerDeg/10),const.FLOAT_PRECISION)
        if self.velocity < 0:
            self.velocity = 0
        self.rotate(self.steerDeg*self.velocity/(self.velocity*self.velocity+const.CAR_MAX_SPEED)*1.8)
        #self.rotate(self.steerDeg*math.pi*self.velocity/6000)
        calc_x = round(math.cos(self.degrees)*self.velocity/6*const.CAR_POWER,const.FLOAT_PRECISION)
        calc_y = round(math.sin(self.degrees)*self.velocity/6*const.CAR_POWER,const.FLOAT_PRECISION)
        self.move(calc_x, calc_y)
        #print(self.velocity)

    def steer(self, pow=const.CAR_POWER):
        if pow<-1:
            pow=-1
        if pow>1:
            pow=1
        self.steerDeg = pow

    def accelerate(self, pow=const.CAR_POWER):
        if pow<0:
            pow=0
        if pow>1:
            pow=1
        self.acceleration=pow

    def brake(self, pow=const.CAR_POWER):
        if pow<0:
            pow=0
        if pow>1:
            pow=1
        self.deceleration=pow
    # we tell to the car where to go and we set a step by step guide to get there

    def setObjective(self, lane):
        self.waypoints = []
        if not lane.isA('exit'):
            raise Exception('Lane selected is not an exit')
        self.crossroad = lane.crossroad
        currentLane, rightS = self.crossroad.getLaneFromPos(self.position)
        if not currentLane:
            raise Exception('This object is not in a lane')
        if not currentLane.isA('entry'):
            raise Exception('Cannot set objective when the car is already leaving')
        if ((currentLane.isA('right') and lane.isA('left')) or
            (currentLane.isA('up') and lane.isA('down')) or
            (currentLane.isA('left') and lane.isA('right')) or
                (currentLane.isA('down') and lane.isA('up'))):
            raise Exception('Cannot set objective same road (you can only move right, forward or left)')
        desideredDirection = Position.getDirection(currentLane.startLanePoints[rightS], lane.endLanePoints[rightS])
        # find if we want to turn left or right or go forward
        # then think if we need extra waypoints
        # we are on the wrong side
        if (((currentLane.isA('left') and lane.isA('down')) or
             (currentLane.isA('up') and lane.isA('left')) or
             (currentLane.isA('right') and lane.isA('up')) or
             (currentLane.isA('down') and lane.isA('right'))) and
                rightS == 0):
            rightS = 1
            self.waypoints.append(Waypoint(currentLane.endLanePoints[rightS].x/2,currentLane.endLanePoints[rightS].y,20))
        if (((currentLane.isA('left') and lane.isA('up')) or
             (currentLane.isA('up') and lane.isA('right')) or
             (currentLane.isA('right') and lane.isA('down')) or
             (currentLane.isA('down') and lane.isA('left'))) and
                rightS == 1):
            rightS = 0
            self.waypoints.append(Waypoint(currentLane.endLanePoints[rightS].x/2,currentLane.endLanePoints[rightS].y,20))

        self.waypoints.append(Waypoint(currentLane.endLanePoints[rightS].x,currentLane.endLanePoints[rightS].y,20))
        self.waypoints.append(Waypoint(lane.startLanePoints[rightS].x,lane.startLanePoints[rightS].y,10))
        self.waypoints.append(Waypoint(lane.endLanePoints[rightS].x,lane.endLanePoints[rightS].y,const.CAR_MAX_SPEED))

        # self.canvas.create_oval(
        #         currentLane.endLanePoints[rightS].x-45,currentLane.endLanePoints[rightS].y-5,
        #         currentLane.endLanePoints[rightS].x-35,currentLane.endLanePoints[rightS].y+5, fill=const.RED_OFF)
        # self.canvas.create_oval(
        #         lane.startLanePoints[rightS].x-5,lane.startLanePoints[rightS].y-5,
        #         lane.startLanePoints[rightS].x+5,lane.startLanePoints[rightS].y+5, fill=const.RED_OFF)
    # predict where it will be in t time

    def predict(self, t=1, wp=None):
        t=int(t*100)
        velocity = self.velocity
        degrees = self.degrees

        def p():
            nonlocal degrees
            nonlocal velocity
            if velocity < const.CAR_MAX_SPEED:
                velocity += self.acceleration
            if velocity > 0:
                velocity -= 4*self.deceleration
            if velocity > 0:
                velocity = round(self.velocity-0.004*self.velocity-math.fabs(self.steerDeg/10),const.FLOAT_PRECISION)
            if velocity < 0:
                velocity = 0
            degrees = round(degrees-self.steerDeg*math.pi*velocity/6000,const.FLOAT_PRECISION)
            calc_x = round(math.cos(degrees)*velocity/40, const.FLOAT_PRECISION)
            calc_y = round(math.sin(degrees)*velocity/40, const.FLOAT_PRECISION)
            return calc_x, calc_y

        retx = 0
        rety = 0
        myp=Position(self.position.x,self.position.y)
        if not wp:
            for i in range(1,t+1):
                x, y = p()
                myp.move(x,y)
        count=0
        while wp and myp.between(self.position,wp) and velocity>0 and count<200: 
            x, y = p()
            myp.move(x,y)
            count+=1
        return Waypoint(myp.x,myp.y,velocity)
    # decide what to do...

    def drive(self):
        if not hasattr(self, 'waypoints') or len(self.waypoints)<1:
            return
        if self.sensibility>1:
            self.sensibility=1
        if self.position.near(self.waypoints[0],4):
            # we passed the target
            self.waypoints.pop(0)
            if len(self.waypoints)<1:
                return

        futureWaypoint=self.predict(wp=self.waypoints[0])
        print(self.waypoints[0],self.position)
        rad = round(math.atan2(self.waypoints[0].y-self.position.y, self.waypoints[0].x-self.position.x), const.FLOAT_PRECISION)
        print(self.steerDeg,self.degrees,rad)
        left=self.degrees-rad
        if left<0:
            left=round(left+math.pi*2,const.FLOAT_PRECISION)
        right=rad-self.degrees# migliorabile?
        if right<0:
            right=round(right+math.pi*2,const.FLOAT_PRECISION)
        if right<left:
            self.steer(right)
        else:
            self.steer(-left)
        print(right,left)

        if self.waypoints[0].velocity>self.velocity:
            self.accelerate()
        else:
            if futureWaypoint.between(self.position,self.waypoints[0]):
                self.accelerate()
            else:
                self.brake(self.sensibility)
                futureWaypoint=self.predict(wp=self.waypoints[0])
                if futureWaypoint.between(self.position,self.waypoints[0]):
                    self.sensibility/=Position.distance(futureWaypoint,self.waypoints[0])
                    self.brake(self.sensibility)
                else:
                    self.sensibility*=Position.distance(futureWaypoint,self.waypoints[0])
                    self.brake(self.sensibility)
            
        # think how turn
