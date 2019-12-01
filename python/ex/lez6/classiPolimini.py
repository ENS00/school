from tkinter import (Tk,Canvas)

WIDTH=600
HEIGHT=400
BGCOLOR='lightgreen'

class Rule():
    def __init__(self,elements):
        #it contains A rects, B poly of dim = 2, C poly of dim = 3 ecc.
        self.values=list()
        for i in elements:
            elRule=set()
            for j in elements:
                if j.y==i.y-1:
                    elRule.add(0)
                if j.x==i.x+1:
                    elRule.add(1)
                if j.y==i.y+1:
                    elRule.add(2)
                if j.x==i.x-1:
                    elRule.add(3)
            self.values.append(tuple({0,1,2,3}-elRule))

    #for print() function
    def __str__(self):
        return '\nRule('+str(self.values)+')'
    def __repr__(self):
        return 'Rule('+str(self.values)+')'
    
    def getDimension(self):
        return len(self.values)

    #return first occurrence if position respect rule
    def find(self,pos):
        print([pos,self])
        possibilities=Rule.getPoss(pos)
        for i in possibilities:
            if i in self.values:
                return i
        raise Exception('No occurrence')
    
    #it returns all type of rects with free positions
    @staticmethod
    def getPoss(pos,allposs=(0,1,2,3),possibilities=set()):
        if len(allposs)>1:
            #pos ex=[0,1]
            for i in pos:
                #remove only if present, otherwise skip because there is nothing to remove
                if i in allposs:
                    poss = tuple([j for j in allposs if i != j])# allposs without iterative pos (1st case (1,2,3), 2nd case (0,2,3))
                    if poss:#if is not a void tuple
                        possibilities.add(poss)
                        recursivePoss=Rule.getPoss(poss,poss)
                        possibilities|=recursivePoss#join other possibilities
        return possibilities

class Position():
    def __init__(self,x,y):
        self.x=x
        self.y=y

class Rect():
    def __init__(self,rule,position=None,size=12,color='#7A7'):
        self.x=0#edit
        self.y=0#edit

        if not position:
            self.freeSides=rule.values.pop(0)
        else:
            self.freeSides=rule.find(position)
            rule.values.remove(self.freeSides)
        self.rule=rule
        self.size=size
        self.color=color
    def draw(self,x=0,y=0):
        canvas.create_rectangle(self.x,self.y,self.x+self.size,self.y+self.size,fill=self.color,outline='black',tags=('square'))
    def getNext(self):
        return Rect(self.rule,position=self.freeSides,size=self.size,color=self.color)


class Polyomino():
    #define a unique polyomino using a unique rule
    def __init__(self,uniquerule,x=0,y=0):
        self.x=x
        self.y=y
        self.dim=uniquerule.getDimension()
        self.uniquerule=uniquerule
        self.elements=[]
        el=Rect(uniquerule)
        self.elements.append(el)
        nextEl=el.getNext()
        while nextEl!=None:
            self.elements.append(nextEl)
            nextEl=nextEl.getNext()

        print(self.elements)
    def draw():
        for i in self.components:
            i.draw(x,y)
    

def PolyArea(canvas,x,y):
    canvas.create_rectangle(x,y,canvas.winfo_width()-10,canvas.winfo_height()-10,outline='black')


tk = Tk()
tk.title('Polimini')
canvas=Canvas(tk,width=WIDTH,height=HEIGHT,bg=BGCOLOR)
canvas.pack()
tk.update()
polyarea=PolyArea(canvas,200,10)
tk.update()

positionArray=[
    Position(3,0),
    Position(1,0),
    Position(0,0),
    Position(2,0)
]
myRule=Rule(positionArray)#Rule([(0, 2, 3), (0, 2), (0, 2), (0, 1, 2)])
Polyomino(myRule)

tk.mainloop()