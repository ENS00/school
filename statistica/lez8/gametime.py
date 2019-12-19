import time
import const

class Gametime():
    def __init__(self,ratio):
        self.ratio=ratio
    def start(self):
        self.startT=time.time()
    # we could try/catch if start is not defined but i think it slows a lot the game
    def getTime(self):
        return (time.time()-self.startT)*self.ratio
    def getFormattedTime(self):
        gametime = (time.time()-self.startT)*self.ratio
        return time.strftime('%H:%M',time.gmtime(gametime))#'%H:%M:%S'