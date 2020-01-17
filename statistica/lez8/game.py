import tkinter
import const
import objects
import gametime

class IDassigner():
    def __init__(self):
        self.__idassign = 0
    
    def getNewID(self):
        self.__idassign += 1
        return self.__idassign

class TimePanel(objects.GraphicObject):
    def __init__(self,canvas,gametime):
        super().__init__(canvas)
        self.gametime=gametime
        self.position=objects.Position(const.W_WIDTH-const.W_WIDTH/20,const.W_HEIGHT/40)
    
    def update(self):
        self.value=self.gametime.getFormattedTime()
        self.draw()
    def draw(self):
        if not hasattr(self, 'graphic'):
            self.graphic = self.canvas.create_text(self.position.x,self.position.y, font=("Purisa", round(const.CAR_HEIGHT/2)),text=self.value)
        self.canvas.itemconfigure(self.graphic,text=self.value)

class Game():
    def __init__(self):
        self.tk = tkinter.Tk()
        self.tk.title(const.W_TITLE)
        self.canvas = tkinter.Canvas(self.tk, width=const.W_WIDTH, height=const.W_HEIGHT, bg=const.W_BACKGROUND)
        self.canvas.pack()
        self.canvas.idassigner = IDassigner()

        self.statusLights=None
        self.time = gametime.Gametime(const.TIME_SPEED)
        self.timepanel=TimePanel(self.canvas,self.time)

        self.cars=[]
        self.removeObjects=[]

    def drawField(self):
        self.canvas.create_rectangle(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height(), width=0)

        #lanes
        self.lane_up_entry = objects.Lane(self.canvas, objects.Position(const.W_WIDTH/2-const.CAR_HEIGHT*0.75, 0),
                                          objects.Position(const.W_WIDTH/2-const.CAR_HEIGHT*0.75, const.W_HEIGHT/2-const.CAR_HEIGHT*1.5))
        
        self.lane_up_exit = objects.Lane(self.canvas, objects.Position(const.W_WIDTH/2+const.CAR_HEIGHT*0.75, const.W_HEIGHT/2-const.CAR_HEIGHT*1.5),
                                         objects.Position(const.W_WIDTH/2+const.CAR_HEIGHT*0.75, 0))
        
        self.lane_left_entry = objects.Lane(self.canvas, objects.Position(0, const.W_HEIGHT/2+const.CAR_HEIGHT*0.75),
                                           objects.Position(const.W_WIDTH/2-const.CAR_HEIGHT*1.5, const.W_HEIGHT/2+const.CAR_HEIGHT*0.75))
        
        self.lane_left_exit = objects.Lane(self.canvas, objects.Position(const.W_WIDTH/2-const.CAR_HEIGHT*1.5, const.W_HEIGHT/2-const.CAR_HEIGHT*0.75),
                                            objects.Position(0, const.W_HEIGHT/2-const.CAR_HEIGHT*0.75))
        
        self.lane_down_entry = objects.Lane(self.canvas, objects.Position(const.W_WIDTH/2+const.CAR_HEIGHT*0.75, const.W_HEIGHT),
                                            objects.Position(const.W_WIDTH/2+const.CAR_HEIGHT*0.75, const.W_HEIGHT/2+const.CAR_HEIGHT*1.5))
        
        self.lane_down_exit = objects.Lane(self.canvas, objects.Position(const.W_WIDTH/2-const.CAR_HEIGHT*0.75, const.W_HEIGHT/2+const.CAR_HEIGHT*1.5),
                                           objects.Position(const.W_WIDTH/2-const.CAR_HEIGHT*0.75, const.W_HEIGHT))
        
        self.lane_right_entry=objects.Lane(self.canvas, objects.Position(const.W_WIDTH,const.W_HEIGHT/2-const.CAR_HEIGHT*0.75),
                                    objects.Position(const.W_WIDTH/2+const.CAR_HEIGHT*1.5,const.W_HEIGHT/2-const.CAR_HEIGHT*0.75))
        
        self.lane_right_exit=objects.Lane(self.canvas, objects.Position(const.W_WIDTH/2+const.CAR_HEIGHT*1.5,const.W_HEIGHT/2+const.CAR_HEIGHT*0.75),
                                    objects.Position(const.W_WIDTH,const.W_HEIGHT/2+const.CAR_HEIGHT*0.75))

        # Traffic lights
        self.tlight_up=self.lane_up_entry.createTrafficLight(const.TL_RED)
        self.tlight_left=self.lane_left_entry.createTrafficLight(const.TL_GREEN)
        self.tlight_down=self.lane_down_entry.createTrafficLight(const.TL_RED)
        self.tlight_right=self.lane_right_entry.createTrafficLight(const.TL_GREEN)

        # crossroad
        self.crossroad=objects.Crossroad(self.canvas,(self.lane_up_entry,self.lane_up_exit,
                                        self.lane_left_entry,self.lane_left_exit,
                                        self.lane_down_entry,self.lane_down_exit,
                                        self.lane_right_entry,self.lane_right_exit))

        # turn on traffic lights
        self.tlight_up.turnOn()
        self.tlight_down.turnOn()
        self.tlight_left.turnOn()
        self.tlight_right.turnOn()

        # let's draw everything
        self.lane_up_entry.draw()
        self.lane_up_exit.draw()
        self.lane_left_entry.draw()
        self.lane_left_exit.draw()
        self.lane_down_entry.draw()
        self.lane_down_exit.draw()
        self.lane_right_entry.draw()
        self.lane_right_exit.draw()
        self.crossroad.draw()
        self.a=0##########################################################################################à
        self.spawnCar()

    def spawnCar(self):
        # newCar = objects.Car(self.canvas,self.crossroad.entries[0].startLanePoints[0])
        # self.cars.append(newCar)
        # newCar.draw()
        # newCar.setObjective(self.crossroad.exits[2])
        newCar = objects.Car(self.canvas,self.crossroad.entries[2].startLanePoints[1])
        self.cars.append(newCar)
        newCar.draw()
        newCar.setObjective(self.crossroad.exits[0])
        # newCar2 = objects.Car(self.canvas,self.crossroad.entries[3].startLanePoints[1])
        # self.cars.append(newCar2)
        # newCar2.draw()
        # newCar2.setObjective(self.crossroad.exits[1])

    def updateField(self):
        self.tlight_up.draw()
        self.tlight_down.draw()
        self.tlight_left.draw()
        self.tlight_right.draw()
        self.timepanel.update()
        for i in self.cars:
            i.update()

    def loop(self):
        currentTimeFromStart = int(self.time.getTime())

        # control all trafficlights
        if currentTimeFromStart//120 % 10 != self.statusLights:
            self.statusLights = currentTimeFromStart//120 % 10
            self.tlight_up.update()
            self.tlight_down.update()
            self.tlight_left.update()
            self.tlight_right.update()

        if currentTimeFromStart//200 % 10 != self.a:
            self.a = currentTimeFromStart//200 % 10
            self.spawnCar()

        # the cars are moving
        for i in self.cars:
            if i.position.x > const.W_WIDTH or i.position.y > const.W_HEIGHT or i.position.x < 0 or i.position.y < 0:
                # destroy object
                self.canvas.delete(i.graphic)
                self.removeObjects.append(i)
            else:
                i.drive(self.cars)

        for i in self.removeObjects:
            self.cars.remove(i)

        self.removeObjects.clear()


        # necessary to upload object states
        self.updateField()
        # cicle
        self.tk.after(10, self.loop)