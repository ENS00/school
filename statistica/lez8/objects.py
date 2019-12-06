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

class Road():
    def __init__(self,pstart,pstop,dim,lineW=6,lineS=2):
        self.pstart=pstart
        self.pstop=pstop
        self.dim=dim
        self.lineW=lineW
        self.lineS=lineS
        if self.pstart.x != self.pstop.x:
            self.orientation = const.HORIZONTAL
        else:
            self.orientation = const.VERTICAL
    
    def draw(self):#TO FIX!!!!!!!!!!!!!!!
        if self.orientation == const.HORIZONTAL:
            self.graphic=draw.canvas.create_rectangle(self.pstart.x-self.dim/2, self.pstart.y-self.dim/2,
                                                      abs(self.pstart.x-self.pstop.x), self.dim,
                                                      fill=const.COLOR_ROAD)
            if self.pstart.x<self.pstop.x:
                step=self.lineS+self.lineW
            else:
                step=-self.lineS+self.lineW
            for posx in range(self.pstart.x,self.pstop.x-self.pstart.x,step):
                draw.canvas.create_rectangle(posx,self.pstart.y-self.dim/8,posx+self.lineW,self.dim/4,fill=const.WHITE)
        else:
            self.graphic=draw.canvas.create_rectangle(self.pstart.x-self.dim/2, self.pstart.y-self.dim/2,
                                                      self.dim, abs(self.pstart.y-self.pstop.y),
                                                      fill=const.COLOR_ROAD)
            if self.pstart.y<self.pstop.y:
                step=self.lineS+self.lineW
            else:
                step=-self.lineS+self.lineW
            for posy in range(self.pstart.y,self.pstop.y-self.pstart.y,step):
                draw.canvas.create_rectangle(self.pstart.x-self.dim/8,posy,self.dim/4,posy+self.lineW,fill=const.WHITE)
    
    def drawStopLine(self):
        pass

class Lane(Road):
    # pstart and pstop centered
    def __init__(self, pstart, pstop, tLight=None, dim=const.CARDIM*1.5):
        super().__init__(pstart,pstop,dim)
        if tLight is None or type(tLight) is TrafficLight:
            pass
        else:
            raise Exception('invalid TrafficLight')

    def draw(self):
        super().draw()


class Crossroad:
    def __init__(lanes):
        pass

lane=Lane(Position(200,200),Position(200,500))
lane.draw()
draw.tk.mainloop()