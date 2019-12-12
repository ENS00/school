import time
import const

class Gametime():
    def __init__(self,ratio):
        self.start=time.time()
        self.ratio=ratio
    def getTime(self):
        return (time.time()-self.start)*self.ratio
    def getFormattedTime(self):
        gametime = (time.time()-self.start)*self.ratio
        return time.strftime('%H:%M',time.gmtime(gametime))#'%H:%M:%S'