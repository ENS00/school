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

    def moveTo(self, x, y):
        if hasattr(self, 'graphicitems'):
            [self.canvas.moveTo(self.graphicitems[i], x, y)
             for i in self.graphicitems]
        if hasattr(self, 'graphic'):
            self.canvas.moveTo(self.graphic, x, y)
        if hasattr(self, 'position'):
            self.position.moveTo(x, y)


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


class TrafficLight(GraphicObject):
    def __init__(self, canvas, posred, posgreen, state=const.RED):
        super().__init__(canvas)
        self.state = state
        self.posred = posred
        self.posgreen = posgreen
        self.posyellow = Position(
            (posgreen.x+posred.x)/2, (posgreen.y+posred.y)/2)
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
    def __init__(self, canvas, pstart, pstop, tLight=None, dim=36*1.5):  # const.CARDIM*1.5
        if tLight is None or type(tLight) is TrafficLight:
            if tLight:
                super().__init__(canvas, pstart, pstop, dim, tags=['entry'])
            else:
                super().__init__(canvas, pstart, pstop,
                                 dim, tags=['exit'])  # EXIT
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
        self.spawnPoints = [i.pstart for i in self.entries]
        self.crossPoints = [i.pstop for i in self.entries]
        self.turnPoints = [i.pstart for i in self.exits]
        self.destinationPoints = [i.pstop for i in self.exits]
        # assuming all lanes have equal dimensions
        self.dim = self.entries[0].dim
        minpstop = Position(2000, 2000)
        maxpstop = Position(0, 0)
        for i in self.entries:
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


class Car(RoadObject):
    def __init__(self, canvas, pos, tags=[]):
        super().__init__(canvas)
        self.position = pos
        self.tags = tags
        self.velocity = 50
        self.degrees = round(math.pi/2,6)

    def draw(self):
        if not hasattr(self, 'graphic'):
            self.graphic = self.canvas.create_rectangle(self.position.x-const.CAR_WIDTH/4, self.position.y-const.CAR_HEIGHT/4,
                                                        self.position.x+const.CAR_WIDTH/4, self.position.y+const.CAR_HEIGHT/4,
                                                        fill=const.RED_ON, width=0)

    def update(self):
        calc_x = round(math.sin(self.degrees)*self.velocity/40, 6)
        calc_y = round(math.cos(self.degrees)*self.velocity/40, 6)
        self.move(calc_x, calc_y)
        if self.velocity > 0:
            self.velocity -= 0.1
        else:
            self.velocity = 0

    def accelerate(self):
        if self.velocity < 90:
            self.velocity += 2

    def brake(self):
        if self.velocity < 90:
            self.velocity -= 8
