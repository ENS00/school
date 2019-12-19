import tkinter
import const
import objects
import gametime

class TimePanel(objects.GraphicObject):
    def __init__(self,canvas,gametime):
        super().__init__(canvas)
        self.gametime=gametime
        self.position=objects.Position(const.W_WIDTH-80,20)
        self.update()
    
    def update(self):
        self.value=self.gametime.getFormattedTime()
        self.draw()
    def draw(self):
        if not hasattr(self, 'graphic'):
            self.graphic = self.canvas.create_text(self.position.x,self.position.y, font=("Purisa", 26),text=self.value)
        self.canvas.itemconfigure(self.graphic,text=self.value)

class Game():
    def __init__(self):
        self.tk = tkinter.Tk()
        self.tk.title(const.W_TITLE)
        self.canvas = tkinter.Canvas(
            self.tk, width=const.W_WIDTH, height=const.W_HEIGHT, bg=const.W_BACKGROUND)
        self.canvas.pack()
        self.time = gametime.Gametime(const.TIME_SPEED)
        self.timepanel=TimePanel(self.canvas,self.time)

    def drawField(self):
        self.canvas.create_rectangle(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height(), width=0)

        #Traffic lights
        self.tlight_up = objects.TrafficLight(self.canvas, objects.Position(320, 320), objects.Position(320, 270))
        self.tlight_down = objects.TrafficLight(self.canvas, objects.Position(460, 460), objects.Position(460, 510))
        self.tlight_left = objects.TrafficLight(self.canvas, objects.Position(320, 460), objects.Position(270, 460))
        self.tlight_right = objects.TrafficLight(self.canvas, objects.Position(460, 320), objects.Position(510, 320))

        #lanes
        self.lane_up_entry = objects.Lane(self.canvas, objects.Position(const.W_WIDTH/2-36*0.75, 0),
                                          objects.Position(const.W_WIDTH/2-36*0.75, const.W_HEIGHT/2-36*1.5), self.tlight_up)
        self.lane_up_exit = objects.Lane(self.canvas, objects.Position(const.W_WIDTH/2+36*0.75, const.W_HEIGHT/2-36*1.5),
                                         objects.Position(const.W_WIDTH/2+36*0.75, 0))
        self.lane_left_entry = objects.Lane(self.canvas, objects.Position(0, const.W_HEIGHT/2+36*0.75),
                                           objects.Position(const.W_WIDTH/2-36*1.5, const.W_HEIGHT/2+36*0.75),self.tlight_left)
        self.lane_left_exit = objects.Lane(self.canvas, objects.Position(const.W_WIDTH/2-36*1.5, const.W_HEIGHT/2-36*0.75),
                                            objects.Position(0, const.W_HEIGHT/2-36*0.75))
        self.lane_down_entry = objects.Lane(self.canvas, objects.Position(const.W_WIDTH/2+36*0.75, const.W_HEIGHT),
                                            objects.Position(const.W_WIDTH/2+36*0.75, const.W_HEIGHT/2+36*1.5), self.tlight_down)
        self.lane_down_exit = objects.Lane(self.canvas, objects.Position(const.W_WIDTH/2-36*0.75, const.W_HEIGHT/2+36*1.5),
                                           objects.Position(const.W_WIDTH/2-36*0.75, const.W_HEIGHT))
        self.lane_right_entry=objects.Lane(self.canvas, objects.Position(const.W_WIDTH,const.W_HEIGHT/2-36*0.75),
                                    objects.Position(const.W_WIDTH/2+36*1.5,const.W_HEIGHT/2-36*0.75),self.tlight_right)
        self.lane_right_exit=objects.Lane(self.canvas, objects.Position(const.W_WIDTH/2+36*1.5,const.W_HEIGHT/2+36*0.75),
                                    objects.Position(const.W_WIDTH,const.W_HEIGHT/2+36*0.75))

        self.crossroad=objects.Crossroad(self.canvas,(self.lane_up_entry,self.lane_up_exit,
                                        self.lane_left_entry,self.lane_left_exit,
                                        self.lane_down_entry,self.lane_down_exit,
                                        self.lane_right_entry,self.lane_right_exit))


        #let's draw everything
        self.lane_up_entry.draw()
        self.lane_up_exit.draw()
        self.lane_left_entry.draw()
        self.lane_left_exit.draw()
        self.lane_down_entry.draw()
        self.lane_down_exit.draw()
        self.lane_right_entry.draw()
        self.lane_right_exit.draw()
        self.crossroad.draw()
        
        self.cars=[]
        self.cars.append(objects.Car(self.canvas,self.crossroad.spawnPoints[1][1]))#objects.Position(200,200)
        self.cars[0].draw()
        self.cars[0].setObjective(self.crossroad.exits[2])
        #self.cars[0].steer(1)

    def updateField(self):
        self.tlight_up.draw()
        self.tlight_down.draw()
        self.tlight_left.draw()
        self.tlight_right.draw()
        self.timepanel.update()
        self.cars[0].update()

    def loop(self):
        # print(gametime.gametime.getFormattedTime())
        # sum 10 every time to gametime???
        currentTimeFromStart = int(self.time.getTime())

        # control all trafficlights
        if currentTimeFromStart//120 % 10 != self.statusLights:
            self.statusLights = currentTimeFromStart//120 % 10
            if self.statusLights == 9:  # YELLOW
                self.tlight_up.changeState()
                self.tlight_down.changeState()
            if self.statusLights == 0:  # RED
                self.tlight_up.changeState()
                self.tlight_down.changeState()
            if self.statusLights == 1:  # GREEN
                self.tlight_left.changeState()
                self.tlight_right.changeState()
            if self.statusLights == 4:  # YELLOW
                self.tlight_left.changeState()
                self.tlight_right.changeState()
            if self.statusLights == 5:  # RED
                self.tlight_left.changeState()
                self.tlight_right.changeState()
            if self.statusLights == 6:  # GREEN
                self.tlight_up.changeState()
                self.tlight_down.changeState()

        # the cars are moving
        for i in self.cars:
            i.drive()
        # necessary to upload object states
        self.updateField()
        # cicle
        self.tk.after(10, self.loop)
