import const
import math


class GraphicObject():
    def __init__(self, canvas):
        self.canvas = canvas

    def draw(self):
        raise Exception('Not yet implemented')

    def move(self, x, y):
        if hasattr(self, 'graphicitems'):
            [self.canvas.move(self.graphicitems[i], x, y)
             for i in self.graphicitems]
        if hasattr(self, 'graphic'):
            self.canvas.move(self.graphic, x, y)
        if hasattr(self, 'position'):
            self.position.move(x, y)
        if hasattr(self, 'sides'):
            for i in self.sides:
                i.move(x, y)

    def moveTo(self, x, y):
        if hasattr(self, 'graphicitems'):
            [self.canvas.moveTo(self.graphicitems[i], x, y)
             for i in self.graphicitems]
        if hasattr(self, 'graphic'):
            self.canvas.moveTo(self.graphic, x, y)
        if hasattr(self, 'position'):
            self.position.moveTo(x, y)
    
    def rotate(self,rad):
        if hasattr(self, 'graphic'):
            self.degrees += rad

            def _rot(x, y):
                #note: the rotation is done in the opposite fashion from for a right-handed coordinate system due to the left-handedness of computer coordinates
                x -= self.position.x
                y -= self.position.y
                _x = x * math.cos(rad) + y * math.sin(rad)
                _y = -x * math.sin(rad) + y * math.cos(rad)
                return _x + self.position.x, _y + self.position.y

            x,y=_rot(self.sides[0].x, self.sides[0].y)
            self.sides[0].moveTo(x,y)
            x,y=_rot(self.sides[1].x, self.sides[1].y)
            self.sides[1].moveTo(x,y)
            x,y=_rot(self.sides[2].x, self.sides[2].y)
            self.sides[2].moveTo(x,y)
            x,y=_rot(self.sides[3].x, self.sides[3].y)
            self.sides[3].moveTo(x,y)
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
        self.x += x
        self.y += y
    # this point is between two points?
    def between(self,pos1,pos2):
        if (self.x<=pos1.x and self.x>=pos2.x) or (self.x>=pos1.x and self.x<=pos2.x):
            if self.y<=pos1.y and self.y>=pos2.y:
                return True
            if self.y>=pos1.y and self.y<=pos2.y:
                return True
        return False
    def distance(self,pos):
        return math.sqrt(math.pow(self.x-pos.x,2)+math.pow(self.y-pos.y,2))
    # starting from pos1, where i am going if i want to arrive in pos2?
    @staticmethod
    def getDirection(pos1,pos2):
        rad=math.atan2(pos2.y-pos1.y,pos2.x-pos1.x)
        ret=[]
        if rad>-math.pi/2+0.001 and rad<math.pi/2-0.001:
            ret.append('right')
        if (rad>math.pi/2+0.001 and rad<math.pi+0.001) or (rad>-math.pi-0.001 and rad<-math.pi/2-0.001):
            ret.append('left')
        if rad>0.001 and rad<math.pi-0.001:
            ret.append('down')
        if rad>-math.pi+0.001 and rad<-0.001:
            ret.append('up')
        return ret


class TrafficLight(GraphicObject):
    def __init__(self, canvas, posred, posgreen, state=const.RED):
        super().__init__(canvas)
        self.state = state
        self.posred = posred
        self.posgreen = posgreen
        self.posyellow = Position((posgreen.x+posred.x)/2, (posgreen.y+posred.y)/2)
        if posgreen.x == posred.x:
            self.orientation = const.HORIZONTAL
        else:
            self.orientation = const.VERTICAL

    def changeState(self):
        if self.state == const.RED:
            self.state = const.GREEN
        elif self.state == const.YELLOW:
            self.state = const.RED
        elif self.state == const.GREEN:
            self.state = const.YELLOW

    def turnOn(self):
        pass

    def turnOff(self):
        pass

    def draw(self):
        if not (hasattr(self, 'redLight') or hasattr(self, 'yellowLight') or hasattr(self, 'greenLight')):
            self.redLight = self.canvas.create_oval(
                self.posred.x, self.posred.y, self.posred.x+20, self.posred.y+20, fill=const.RED_OFF)
            self.yellowLight = self.canvas.create_oval(
                self.posyellow.x, self.posyellow.y, self.posyellow.x+20, self.posyellow.y+20, fill=const.YELLOW_OFF)
            self.greenLight = self.canvas.create_oval(
                self.posgreen.x, self.posgreen.y, self.posgreen.x+20, self.posgreen.y+20, fill=const.GREEN_OFF)
            self.graphicitems = (
                self.redLight, self.yellowLight, self.greenLight)
        if self.state == const.RED:
            self.canvas.itemconfigure(self.redLight, fill=const.RED_ON)
            self.canvas.itemconfigure(self.yellowLight, fill=const.YELLOW_OFF)
            self.canvas.itemconfigure(self.greenLight, fill=const.GREEN_OFF)
        if self.state == const.YELLOW:
            self.canvas.itemconfigure(self.redLight, fill=const.RED_OFF)
            self.canvas.itemconfigure(self.yellowLight, fill=const.YELLOW_ON)
            self.canvas.itemconfigure(self.greenLight, fill=const.GREEN_OFF)
        if self.state == const.GREEN:
            self.canvas.itemconfigure(self.redLight, fill=const.RED_OFF)
            self.canvas.itemconfigure(self.yellowLight, fill=const.YELLOW_OFF)
            self.canvas.itemconfigure(self.greenLight, fill=const.GREEN_ON)


class RoadObject(GraphicObject):
    def __init__(self, canvas):
        super().__init__(canvas)

    def isA(self, prop):
        if prop in self.tags:
            return True
        return False


class Road(RoadObject):
    def __init__(self, canvas, pstart, pstop, dim, lineW=16, lineS=6, tags=[]):
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
                    stopline = self.lineW
                else:
                    road_lines = range(round(self.pstop.x),
                                       round(self.pstart.x), step)
                    stopline = -self.lineW
                for posx in road_lines:
                    self.graphicitems.append(self.canvas.create_rectangle(posx, self.pstart.y-self.dim/16,
                                                                          posx+self.lineW, self.pstart.y+self.dim/16,
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
                    stopline = self.lineW
                else:
                    road_lines = range(round(self.pstop.y),
                                       round(self.pstart.y), step)
                    stopline = -self.lineW
                for posy in road_lines:
                    self.graphicitems.append(self.canvas.create_rectangle(self.pstart.x-self.dim/16, posy,
                                                                          self.pstart.x+self.dim/16, posy+self.lineW,
                                                                          fill=const.WHITE, width=0))
                if super().isA('entry'):
                    self.graphicitems.append(self.canvas.create_rectangle(self.pstart.x-self.dim/2, self.pstop.y,
                                                                          self.pstart.x+self.dim/2, self.pstop.y-stopline,
                                                                          fill=const.WHITE, width=0))


class Lane(Road):
    # pstart and pstop centered
    def __init__(self, canvas, pstart, pstop, tLight=None, dim=const.CAR_HEIGHT*1.5):
        tags = Position.getDirection(pstart,pstop)
        if tLight is None or type(tLight) is TrafficLight:
            if tLight:
                self.tLight=tLight
                tags.extend(['entry'])
                super().__init__(canvas, pstart, pstop, dim, tags=tags)
                if self.orientation == const.HORIZONTAL:
                    # spawn points are two, left (you can turn left or go straight) and right side (you can turn right or go straight)
                    self.spawnPoints=(
                        Position(pstart.x,pstart.y+2-const.CAR_HEIGHT/2),
                        Position(pstart.x,pstart.y-2+const.CAR_HEIGHT/2)
                    )
                    # end lane points are the first stage before steer respectively
                    self.endLanePoints=(
                        Position(pstop.x,pstop.y+2-const.CAR_HEIGHT/2),
                        Position(pstop.x,pstop.y-2+const.CAR_HEIGHT/2)
                    )
                else:
                    self.spawnPoints=(
                        Position(pstart.x+2-const.CAR_HEIGHT/2,pstart.y),
                        Position(pstart.x-2+const.CAR_HEIGHT/2,pstart.y)
                    )
                    self.endLanePoints=(
                        Position(pstop.x+2-const.CAR_HEIGHT/2,pstop.y),
                        Position(pstop.x-2+const.CAR_HEIGHT/2,pstop.y)
                    )
            else:
                tags.extend(['exit'])
                super().__init__(canvas, pstart, pstop, dim, tags=tags)
                if self.orientation == const.HORIZONTAL:
                    # direction points are two, left (for cars that chose to turn right or go straight)
                    # and right side (for cars that chose to turn left or go straight)
                    self.directionPoints=(
                        Position(pstart.x,pstart.y+2-const.CAR_HEIGHT/2),
                        Position(pstart.x,pstart.y-2+const.CAR_HEIGHT/2)
                    )
                    # finally the car arrives at its destination
                    self.destinationPoints=(
                        Position(pstop.x,pstop.y+2-const.CAR_HEIGHT/2),
                        Position(pstop.x,pstop.y-2+const.CAR_HEIGHT/2)
                    )
                else:
                    self.directionPoints=(
                        Position(pstart.x+2-const.CAR_HEIGHT/2,pstart.y),
                        Position(pstart.x-2+const.CAR_HEIGHT/2,pstart.y)
                    )
                    self.destinationPoints=(
                        Position(pstop.x+2-const.CAR_HEIGHT/2,pstop.y),
                        Position(pstop.x-2+const.CAR_HEIGHT/2,pstop.y)
                    )
        else:
            raise Exception('invalid TrafficLight')

    def draw(self):
        if not (hasattr(self, 'graphic') or hasattr(self, 'graphicitems')):
            super().draw()


class Crossroad(RoadObject):
    def __init__(self, canvas, lanes):
        super().__init__(canvas)
        self.entries = [i for i in lanes if i.isA('entry')]
        self.exits = [i for i in lanes if i.isA('exit')]
        self.spawnPoints = [i.spawnPoints for i in self.entries]
        self.endLanePoints = [i.endLanePoints for i in self.entries]
        self.directionPoints = [i.directionPoints for i in self.exits]
        self.destinationPoints = [i.destinationPoints for i in self.exits]
        # assuming all lanes have equal dimensions
        self.dim = self.entries[0].dim
        minpstop = Position(2000, 2000)
        maxpstop = Position(0, 0)
        for i in self.exits:
            i.crossroad=self
        for i in self.entries:
            i.crossroad=self
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
    def getLaneFromPos(self,pos):
        for i in self.entries:
            if pos.between(i.spawnPoints[0],i.endLanePoints[0]):
                return i,0
            if pos.between(i.spawnPoints[1],i.endLanePoints[1]):
                return i,1
        for i in self.exits:
            if pos.between(i.directionPoints[0],i.destinationPoints[0]):
                return i,0
            if pos.between(i.directionPoints[1],i.destinationPoints[1]):
                return i,1
        # this point is not in a lane
        return None

class Car(RoadObject):
    def __init__(self, canvas, pos, tags=[]):
        super().__init__(canvas)
        self.position = pos
        self.tags = tags
        self.velocity = 50
        self.degrees = round(math.pi/2,6)
        self.steerDeg = 0
        # SIDES
        self.sides = (
            Position(self.position.x-const.CAR_WIDTH/4,self.position.y-const.CAR_HEIGHT/4),
            Position(self.position.x+const.CAR_WIDTH/4,self.position.y-const.CAR_HEIGHT/4),
            Position(self.position.x+const.CAR_WIDTH/4,self.position.y+const.CAR_HEIGHT/4),
            Position(self.position.x-const.CAR_WIDTH/4,self.position.y+const.CAR_HEIGHT/4)
        )

    def draw(self):
        if not hasattr(self, 'graphic'):
            self.graphic = self.canvas.create_polygon(self.sides[0].x, self.sides[0].y,
                                                        self.sides[1].x, self.sides[1].y,
                                                        self.sides[2].x, self.sides[2].y,
                                                        self.sides[3].x, self.sides[3].y,
                                                        fill=const.RED_ON, width=0)

    def update(self):
        if self.velocity > 0:
            self.velocity -= 0.1+math.fabs(self.steerDeg/10)
        else:
            self.velocity = 0
        self.rotate(-self.steerDeg*math.pi*self.velocity/6000)
        calc_x = round(math.sin(self.degrees)*self.velocity/40, 6)
        calc_y = round(math.cos(self.degrees)*self.velocity/40, 6)
        self.move(calc_x, calc_y)
        if self.position.x>=const.W_WIDTH and self.position.y>=const.W_HEIGHT:
            # destroy object
            self.canvas.delete(self.graphic)
            del self
    
    def steer(self,pow=0.5):
        self.steerDeg=pow

    def throttle(self,pow=0.5):
        if self.velocity < 90:
            self.velocity += 0.5*pow

    def brake(self,pow=0.5):
        if self.velocity < 90:
            self.velocity -= 2*pow
    # we tell to the car where to go and we set a step by step guide to get there
    def setObjective(self,lane):
        self.waypoints=[]
        if not lane.isA('exit'):
            raise Exception('Lane selected is not an exit')
        self.crossroad=lane.crossroad
        currentLane,rightS = self.crossroad.getLaneFromPos(self.position)
        if not currentLane.isA('entry'):
            raise Exception('Cannot set objective when the car is already leaving')
        if ((currentLane.isA('right') and lane.isA('left')) or
            (currentLane.isA('up') and lane.isA('down')) or
            (currentLane.isA('left') and lane.isA('right')) or
            (currentLane.isA('down') and lane.isA('up'))):
            raise Exception('Cannot set objective same road (you can only move right, forward or left)')
        desideredDirection=Position.getDirection(currentLane.spawnPoints[rightS],lane.destinationPoints[rightS])
        # we are on the wrong side
        if (((currentLane.isA('left') and lane.isA('down')) or
            (currentLane.isA('up') and lane.isA('left')) or
            (currentLane.isA('right') and lane.isA('up')) or
            (currentLane.isA('down') and lane.isA('right'))) and 
            rightS==0):
            rightS=1
        if (((currentLane.isA('left') and lane.isA('up')) or
            (currentLane.isA('up') and lane.isA('right')) or
            (currentLane.isA('right') and lane.isA('down')) or
            (currentLane.isA('down') and lane.isA('left'))) and 
            rightS==1):
            rightS=0
        self.waypoints.append(currentLane.endLanePoints[rightS])
        self.waypoints.append(lane.directionPoints[rightS])
        self.waypoints.append(lane.destinationPoints[rightS])
    # decide what to do...
    def drive(self):
        if not hasattr(self,'waypoints'):
            return
        if not hasattr(self,'status'):
            self.status=3-len(self.waypoints)
        if self.status==2:
            # exiting
            self.throttle()
            return
        if self.status==0:
            if self.position.between(self.waypoints[0],self.waypoints[1]):
                # we passed the traffic light
                self.status=1
            else:
                # we are about to face the traffic light
                if not hasattr(self,'myTrafficLight'):
                    currentLane,rightS = self.crossroad.getLaneFromPos(self.position)
                    self.myTrafficLight=currentLane.tLight
                if self.myTrafficLight.state==const.GREEN:
                    self.throttle()
                if self.myTrafficLight.state==const.YELLOW:
                    # we can pass in 3 seconds
                    dist=self.position.distance(self.waypoints[0])
                    print(self.velocity,dist)
                    # distance per sec
                    if self.velocity>dist:
                        self.throttle(1)
                    else:
                        self.brake()
                if self.myTrafficLight.state==const.RED:
                    self.brake()
        if self.status==1:
            #TODO: turn or go forward
            self.throttle()