import tkinter
import copy

class Canvas(tkinter.Canvas):
    # do not clone me
    def __deepcopy__(self,memo=None):
        return self

class Graphic():
    def __init__(self, title, width, height, background_color):
        self.graphic = tkinter.Tk()
        self.graphic.title(title)
        self.canvas = Canvas(self.graphic, width=width, height=height, bg=background_color)
        self.canvas.pack()
        self.width = width
        self.height = height
        self.background_color = background_color
    
    def drawRect(self, x0, y0, x1, y1, fill=None, outline=None, border=0):
        return self.canvas.create_polygon(x0, y0, x1, y0, x1, y1, x0, y1, fill=fill, outline=outline, width=border)

    def drawCircle(self, x, y, r, fill):
        return self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=fill)

    def drawText(self, x, y, text, font, size):
        return self.canvas.create_text(x, y, font=(font, size), text=text)

    def move(self, obj, x, y):
        if hasattr(obj, 'graphicitems'):
            [self.canvas.move(obj.graphicitems[i], x, y) for i in obj.graphicitems]
        if hasattr(obj, 'graphic'):
            self.canvas.move(obj.graphic, x, y)

    def moveTo(self, obj, x, y):
        if hasattr(obj, 'graphicitems'):
            [self.canvas.moveTo(obj.graphicitems[i], x, y) for i in obj.graphicitems]
        if hasattr(obj, 'graphic'):
            self.canvas.moveTo(obj.graphic, x, y)

    def setCoords(self, obj, newCoords):
        if hasattr(obj, 'graphic'):
            self.canvas.coords(obj.graphic, newCoords[0], newCoords[1],
                                        newCoords[2], newCoords[3],
                                        newCoords[4], newCoords[5],
                                        newCoords[6], newCoords[7])

    def changeColor(self, canvasObj, color):
        self.canvas.itemconfigure(canvasObj, fill=color)

    def changeText(self, canvasObj, text):
        self.canvas.itemconfigure(canvasObj, text=text)
    # pass an object and call his draw function
    def draw(self,obj):
        if type(obj) is list:
            [el.draw(self) for el in obj]
        else:
            obj.draw(self)

    def delete(self,obj):
        self.canvas.delete(obj)

    def update(self, function, time):
        self.graphic.after(time, function)

    def mainloop(self):
        self.graphic.mainloop()