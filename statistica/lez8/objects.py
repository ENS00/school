import const
import draw


class Position():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, x, y):
        self.x = x
        self.y = y

    def forward(self, x, y):
        self.x += x
        self.y += y


class TrafficLight():
    def __init__(self, pos, state=const.RED):
        self.state = state
        self.pos = pos

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
        pass

class RoadObject():
    def isA(self,prop):
        if prop in self.tags:
            return True
        return False

class Road(RoadObject):
    def __init__(self,pstart,pstop,dim,lineW=16,lineS=6,tags=[]):
        self.pstart=pstart
        self.pstop=pstop
        self.dim=dim
        self.lineW=lineW
        self.lineS=lineS
        self.tags=tags
        if self.pstart.x != self.pstop.x:
            self.orientation = const.HORIZONTAL
        else:
            self.orientation = const.VERTICAL
    
    def draw(self):
        if self.orientation == const.HORIZONTAL:
            #draw road
            self.graphic=draw.canvas.create_rectangle(self.pstart.x, self.pstart.y-self.dim/2,
                                                      self.pstop.x, self.pstart.y+self.dim/2,
                                                      fill=const.COLOR_ROAD,width=0)
            #draw white lines
            if self.pstart.x<self.pstop.x:
                step=self.lineS+self.lineW
                road_lines = range(round(self.pstart.x),round(self.pstop.x-step),step)
            else:
                step=-self.lineS-self.lineW
                road_lines = range(round(self.pstart.x-self.lineW),round(self.pstop.x),step)
            for posx in road_lines:
                draw.canvas.create_rectangle(posx,self.pstart.y-self.dim/16,
                                            posx+self.lineW,self.pstart.y+self.dim/16,
                                            fill=const.WHITE,width=0)
            #draw stop line
            if super().isA('entry'):
                draw.canvas.create_rectangle(self.pstop.x,self.pstart.y-self.dim/2,
                                            self.pstop.x-step,self.pstart.y+self.dim/2,
                                            fill=const.WHITE,width=0)
        else:
            self.graphic=draw.canvas.create_rectangle(self.pstart.x-self.dim/2, self.pstart.y,
                                                      self.pstart.x+self.dim/2, self.pstop.y,
                                                      fill=const.COLOR_ROAD,width=0)
            if self.pstart.y<self.pstop.y:
                step=self.lineS+self.lineW
                road_lines = range(round(self.pstart.y),round(self.pstop.y-step),step)
            else:
                step=-self.lineS-self.lineW
                road_lines = range(round(self.pstart.y-self.lineW),round(self.pstop.y),step)
            for posy in road_lines:
                draw.canvas.create_rectangle(self.pstart.x-self.dim/16,posy,
                                            self.pstart.x+self.dim/16,posy+self.lineW,
                                            fill=const.WHITE,width=0)
            if super().isA('entry'):
                draw.canvas.create_rectangle(self.pstart.x-self.dim/2,self.pstop.y,
                                            self.pstart.x+self.dim/2,self.pstop.y-step,
                                            fill=const.WHITE,width=0)

class Lane(Road):
    # pstart and pstop centered
    def __init__(self, pstart, pstop, tLight=None, dim=36*1.5):#const.CARDIM*1.5
        if tLight is None or type(tLight) is TrafficLight:
            if tLight:
                super().__init__(pstart,pstop,dim,tags=['entry'])
            else:
                super().__init__(pstart,pstop,dim,tags=['entry'])#EXIT
            pass
        else:
            raise Exception('invalid TrafficLight')

    def draw(self):
        super().draw()


class Crossroad:
    def __init__(lanes):
        pass