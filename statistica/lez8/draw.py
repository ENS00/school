import tkinter
import const
import objects
import gametime

class Game():
    def __init__(self):
        self.tk=tkinter.Tk()
        self.tk.title(const.W_TITLE)
        self.canvas=tkinter.Canvas(self.tk,width=const.W_WIDTH,height=const.W_HEIGHT,bg=const.W_BACKGROUND)
        self.canvas.pack()
        self.time=gametime.Gametime(const.TIME_SPEED)
    def drawField(self):
        self.canvas.create_rectangle(0,0,self.canvas.winfo_width(),self.canvas.winfo_height(),width=0)
        
        self.tlight_up=objects.TrafficLight(self.canvas,objects.Position(250,300),objects.Position(250,250))
        self.tlight_down=objects.TrafficLight(self.canvas,objects.Position(450,400),objects.Position(450,450))

        self.lane_up_entry = objects.Lane(self.canvas,objects.Position(const.W_WIDTH/2-36*0.75,0),
                                    objects.Position(const.W_WIDTH/2-36*0.75,const.W_HEIGHT/2-36*1.5),self.tlight_up)
        self.lane_up_entry.draw()
        self.lane_up_exit = objects.Lane(self.canvas,objects.Position(const.W_WIDTH/2+36*0.75,const.W_HEIGHT/2-36*1.5),
                                    objects.Position(const.W_WIDTH/2+36*0.75,0))
        self.lane_up_exit.draw()
        self.lane_left_entry=objects.Lane(self.canvas,objects.Position(const.W_WIDTH/2-36*1.5,const.W_HEIGHT/2-36*0.75),
                                    objects.Position(0,const.W_HEIGHT/2-36*0.75))
        self.lane_left_entry.draw()
        self.lane_left_exit=objects.Lane(self.canvas,objects.Position(0,const.W_HEIGHT/2+36*0.75),
                                    objects.Position(const.W_WIDTH/2-36*1.5,const.W_HEIGHT/2+36*0.75))
        self.lane_left_exit.draw()
        self.lane_down_entry = objects.Lane(self.canvas,objects.Position(const.W_WIDTH/2-36*0.75,const.W_HEIGHT),
                                    objects.Position(const.W_WIDTH/2-36*0.75,const.W_HEIGHT/2-36*1.5),self.tlight_down)
        self.lane_down_entry.draw()
        self.lane_down_exit = objects.Lane(self.canvas,objects.Position(const.W_WIDTH/2+36*0.75,const.W_HEIGHT/2-36*1.5),
                                    objects.Position(const.W_WIDTH/2+36*0.75,const.W_HEIGHT))
        self.lane_down_exit.draw()
        """
        self.lane_right_entry=objects.Lane(self.canvas,objects.Position(const.W_WIDTH/2-36*1.5,const.W_HEIGHT/2-36*0.75),
                                    objects.Position(const.W_WIDTH,const.W_HEIGHT/2-36*0.75))
        self.lane_right_entry.draw()
        self.lane_right_exit=objects.Lane(self.canvas,objects.Position(const.W_WIDTH,const.W_HEIGHT/2+36*0.75),
                                    objects.Position(const.W_WIDTH/2-36*1.5,const.W_HEIGHT/2+36*0.75))
        self.lane_right_exit.draw()
        """
    def updateField(self):
        self.tlight_up.draw()

    def loop(self):
        #print(gametime.gametime.getFormattedTime())
        #sum 10 every time to gametime???
        currentTimeFromStart=int(self.time.getTime())
        
        #control all trafficlights
        if currentTimeFromStart//60%10!=self.statusLights:
            self.statusLights=currentTimeFromStart//60%10
            if self.statusLights==9:#YELLOW
                self.tlight_up.changeState()
                self.tlight_down.changeState()
            if self.statusLights==0:#RED
                self.tlight_up.changeState()
                self.tlight_down.changeState()
            if self.statusLights==5:#GREEN
                self.tlight_up.changeState()
                self.tlight_down.changeState()
            
        
        #necessary to upload object states
        self.updateField()
        #cicle
        self.tk.after(10,self.loop)