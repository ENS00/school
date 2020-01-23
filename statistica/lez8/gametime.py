from time import time,strftime,gmtime
import const

class Gametime():
    def __init__(self,ratio):
        self.ratio=ratio/4
    def start(self):
        self.startT=time()
    # we could try/catch if start is not defined but i think it slows a lot the game
    def getTime(self):
        return (time()-self.startT)*self.ratio
    def getFormattedTime(self):
        gametime = (time()-self.startT)*self.ratio
        return strftime('%H:%M',gmtime(gametime))#'%H:%M:%S'