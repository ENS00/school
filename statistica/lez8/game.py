import graphic_lib
import const
import gametime
import objects
from random import randint

class IDassigner():
    def __init__(self):
        self.__idassign = 0
    
    def getNewID(self):
        self.__idassign += 1
        return self.__idassign

class TimePanel(objects.GameObject):
    def __init__(self, game, gametime):
        super().__init__(game)
        self.gametime = gametime
        self.position = objects.Position(const.W_WIDTH-const.W_WIDTH/20,const.W_HEIGHT/40)
        self.game = game
    
    def update(self):
        self.value = self.gametime.getFormattedTime()
        self.draw()
    def draw(self):
        if not hasattr(self, 'graphic'):
            self.graphic = self.game.graphic_lib.drawText(self.position.x,self.position.y,self.value, "Purisa", round(const.CAR_HEIGHT/2))
        self.game.graphic_lib.changeText(self.graphic,self.value)

class Game():
    def __init__(self):
        self.graphic_lib = graphic_lib.Graphic(const.W_TITLE,const.W_WIDTH,const.W_HEIGHT,const.W_BACKGROUND)
        self.idassigner = IDassigner()

        self.statusLights = None
        self.time = gametime.Gametime(const.TIME_SPEED)
        self.timepanel = TimePanel(self, self.time)

        self.vehicles = []
        self.removeObjects = []
        self.randomSpawn = randint(500,1100)# every x time spawn a vehicle
        self.spawnCount = 0

    def drawField(self):
        #self.graphic_lib.drawRect(0, 0, const.W_WIDTH, const.W_HEIGHT, fill=const.W_BACKGROUND)# self.canvas.winfo_width() # self.canvas.winfo_height()

        # ROADS
        self.road_north = objects.Road(objects.Position(const.W_WIDTH/2,0),
                                objects.Position(const.W_WIDTH/2,const.W_HEIGHT/2))
                                
        self.road_east = objects.Road(objects.Position(const.W_WIDTH,const.W_HEIGHT/2),
                                objects.Position(const.W_WIDTH/2,const.W_HEIGHT/2))

        self.road_south = objects.Road(objects.Position(const.W_WIDTH/2,const.W_HEIGHT),
                                objects.Position(const.W_WIDTH/2,const.W_HEIGHT/2))

        self.road_west = objects.Road(objects.Position(0,const.W_HEIGHT/2),
                                objects.Position(const.W_WIDTH/2,const.W_HEIGHT/2))
        
        # crossroad
        self.crossroad = objects.Crossroad([self.road_north,self.road_east,self.road_south,self.road_west])
        self.crossroad.turnOnTLights()

        # let's draw everything
        self.graphic_lib.draw(self.crossroad)

        newVehicle = self.spawnVehicle()
        self.vehicles.append(newVehicle)

    def updateField(self):
        self.graphic_lib.draw(self.crossroad)
        self.timepanel.update()
        for i in self.vehicles:
            i.update()

    def loop(self):
        currentTimeFromStart = int(self.time.getTime())

        # control all trafficlights
        if currentTimeFromStart//1200 % 10 != self.statusLights:
            self.statusLights = currentTimeFromStart//1200 % 10
            self.crossroad.updateTLights()

        if currentTimeFromStart > self.spawnCount+self.randomSpawn:
            self.spawnCount = currentTimeFromStart+self.randomSpawn
            self.randomSpawn = randint(400,1400)
            newVehicle = self.spawnVehicle()
            self.vehicles.append(newVehicle)

        # the vehicles are moving
        for i in self.vehicles:
            if i.arrived:
                print(i.sides)
                #TODO VERIFICARE PERCHE' NON FUNZIA AL BUS
                right_side_out = i.sides[0].x > const.W_WIDTH or i.sides[0].y > const.W_HEIGHT or i.sides[0].x < 0 or i.sides[0].y < 0
                left_side_out = i.sides[3].x > const.W_WIDTH or i.sides[3].y > const.W_HEIGHT or i.sides[3].x < 0 or i.sides[3].y < 0
                if left_side_out or right_side_out:
                    # destroy object
                    self.graphic_lib.delete(i.graphic)
                    self.removeObjects.append(i)
                else:
                    i.drive(self.vehicles)
            else:
                i.drive(self.vehicles)

        for i in self.removeObjects:
            print(i.id,'removed')
            self.vehicles.remove(i)

        self.removeObjects.clear()


        # necessary to upload object states
        self.updateField()
        # cicle
        self.graphic_lib.update(self.loop, 10)

    def spawnVehicle(self):
        if(randint(0,7)>5):
            newVehicle = objects.Bus(self,self.crossroad,self.crossroad.randomEntry())
        else:
            newVehicle = objects.Car(self,self.crossroad,self.crossroad.randomEntry())
        self.graphic_lib.draw(newVehicle)
        # for now we set that all cars do not turn
        newVehicle.setObjective(self.crossroad.getOppositeLanes(newVehicle)[0])
        return newVehicle