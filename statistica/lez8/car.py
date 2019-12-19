import const
import objects

class Car(objects.RoadObject):
    def __init__(self, canvas, pos, tags=[]):
        super().__init__(canvas)
        self.position = pos
        self.tags = tags
        self.velocity = 50
        self.degrees = round(math.pi/2,6)
        self.steerDeg = 0
        # SIDES
        self.sides = (
            objects.Position(self.position.x-const.CAR_WIDTH/4,self.position.y-const.CAR_HEIGHT/4),
            objects.Position(self.position.x+const.CAR_WIDTH/4,self.position.y-const.CAR_HEIGHT/4),
            objects.Position(self.position.x+const.CAR_WIDTH/4,self.position.y+const.CAR_HEIGHT/4),
            objects.Position(self.position.x-const.CAR_WIDTH/4,self.position.y+const.CAR_HEIGHT/4)
        )

    def draw(self):
        if not hasattr(self, 'graphic'):
            self.graphic = self.canvas.create_polygon(self.sides[0].x, self.sides[0].y,
                                                        self.sides[1].x, self.sides[1].y,
                                                        self.sides[2].x, self.sides[2].y,
                                                        self.sides[3].x, self.sides[3].y,
                                                        fill=const.RED_ON, width=0)

    def update(self):
        self.rotate(-self.steerDeg*math.pi*self.velocity/6000)
        calc_x = round(math.sin(self.degrees)*self.velocity/40, 6)
        calc_y = round(math.cos(self.degrees)*self.velocity/40, 6)
        self.move(calc_x, calc_y)
        if self.velocity > 0:
            self.velocity -= 0.1+math.fabs(self.steerDeg/10)
        else:
            self.velocity = 0
        if self.position.x>=const.W_WIDTH and self.position.y>=const.W_HEIGHT:
            # destroy object
            self.canvas.delete(self.graphic)
            del self
    
    def steer(self,pow=0.5):
        self.steerDeg=pow

    def throttle(self,pow=0.5):
        if self.velocity < 90:
            self.velocity += 2*pow

    def brake(self,pow=0.5):
        if self.velocity < 90:
            self.velocity -= 8*pow
    # we tell to the car where to go and we set a step by step guide to get there
    def setObjective(self,lane):
        self.waypoints=[]
        if not lane.isA('exit'):
            raise Exception('Lane selected is not an exit')
        crossroad=lane.crossroad
        currentLane,rightS = crossroad.getLaneFromPos(self.position)
        if not currentLane.isA('entry'):
            raise Exception('Cannot set objective when the car is already leaving')
        if ((currentLane.isA('right') and lane.isA('left')) or
            (currentLane.isA('up') and lane.isA('down')) or
            (currentLane.isA('left') and lane.isA('right')) or
            (currentLane.isA('down') and lane.isA('up'))):
            raise Exception('Cannot set objective same road (you can only move right, forward or left)')
        desideredDirection=objects.Position.getDirection(currentLane.spawnPoints[rightS],lane.destinationPoints[rightS])
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
        if not hasattr(self,'status')
            self.status=3-len(self.waypoints)
        if self.status==2:
            # exiting
            self.throttle()
            return
        if self.status==0:
            if self.position.between(self.waypoints[0],self.waypoints[1]):
                # we passed the traffic light
                self.status=1
                break
            # we are about to face the traffic light
            if not hasattr(self,'myTrafficLight'):
                currentLane,rightS = crossroad.getLaneFromPos(self.position)
                self.myTrafficLight=currentLane.tLight
            if self.myTrafficLight.status==const.GREEN:
                self.throttle()
            if self.myTrafficLight.status==const.YELLOW:
                # we can pass in 3 seconds
                dist=self.position.distance(self.waypoints[0])
                print(self.velocity,dist)
                # distance per sec
                if self.velocity/300>dist:
                    self.throttle(1)
                else
                    self.brake()
            if self.myTrafficLight.status==const.RED:
                self.brake()
        if self.status==1:
            #TODO: turn or go forward
            self.throttle()