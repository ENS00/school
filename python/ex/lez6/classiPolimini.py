from tkinter import (Tk,Canvas)

WIDTH=600
HEIGHT=400
BGCOLOR='lightgreen'

#rules are adiacent free sides for every square

class Rule():
    def __init__(self,positions):
        #it contains A rects, B poly of dim = 2, C poly of dim = 3 ecc.
        self.values=list()
        self.positions=positions
        for i in positions:
            elRule=set()
            if True in [True for j in positions if j.y==i.y-1 and j.x==i.x]:
                elRule.add(0)
            if True in [True for j in positions if j.y==i.y and j.x==i.x+1]:
                elRule.add(1)
            if True in [True for j in positions if j.y==i.y+1 and j.x==i.x]:
                elRule.add(2)
            if True in [True for j in positions if j.y==i.y and j.x==i.x-1]:
                elRule.add(3)
            self.values.append(tuple({0,1,2,3}-elRule))

    #for print() function
    def __str__(self):
        return 'Rule('+str(self.values)+')'
    def __repr__(self):
        return 'Rule('+str(self.values)+')'

    def clone(self):
        return Rule(self.positions)
    
    def getDimension(self):
        return len(self.values)

    #inverse algorithm to find all positions starting from rules
    @staticmethod
    def getPositions(values):
        values=list(values)
        start=Position(0,0)
        lastvalue=None
        positions=[]
        remembervalues=[]
        count={0:0}
        backupvalues={}
        deep=0
        while len(values)>0:
            count[deep+1]=0
            found=False
            for i in range(count[deep],len(values)):
                count[deep]+=1
                backupvalues[deep]=list(values)
                currentvalue=values[i]
                if lastvalue:
                    #trying to attach to the up
                    if 0 not in lastvalue and 2 not in currentvalue:
                        newposition=Position(lastposition.x,lastposition.y)
                        newposition.move(0,-1)
                        if not newposition.inArray(positions):
                            lastposition=newposition
                            found=True
                            break
                    #trying to attach to the right
                    if 1 not in lastvalue and 3 not in currentvalue:
                        newposition=Position(lastposition.x,lastposition.y)
                        newposition.move(1,0)
                        if not newposition.inArray(positions):
                            lastposition=newposition
                            found=True
                            break
                    #trying to attach to the down
                    if 2 not in lastvalue and 0 not in currentvalue:
                        newposition=Position(lastposition.x,lastposition.y)
                        newposition.move(0,1)
                        if not newposition.inArray(positions):
                            lastposition=newposition
                            found=True
                            break
                    #trying to attach to the left
                    if 3 not in lastvalue and 1 not in currentvalue:
                        newposition=Position(lastposition.x,lastposition.y)
                        newposition.move(-1,0)
                        if not newposition.inArray(positions):
                            lastposition=newposition
                            found=True
                            break
                else:
                    lastposition=start
                    found=True
                    break
            if not found:
                #it's not possible to attach this at the moment, let's remove the last one and retry
                lastposition=positions.pop()
                lastvalue=remembervalues.pop()
                if len(positions)<1:
                    lastposition=None
                    lastvalue=None
                deep-=1
                values=backupvalues[deep]
            else:
                remembervalues.append(currentvalue)
                positions.append(lastposition)
                values.remove(currentvalue)
                lastvalue=currentvalue
                deep+=1
        minX=900
        minY=900
        for el in positions:
            if el.x<minX:
                minX=el.x
            if el.y<minY:
                minY=el.y
        for el in positions:
            el.move(-minX,-minY)
        return positions

    #return first occurrence if position respect rule
    def find(self,freeSides):
        possibilities=Rule.getPoss(freeSides,possibilities=set())
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
    #it's possible to implement here movement or transformation functions and then call them inside Rect class
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def move(self,x,y):
        self.x+=x
        self.y+=y

    #for print() function
    def __str__(self):
        return 'Position(x:'+str(self.x)+'; y:'+str(self.y)+')'
    def __repr__(self):
        return 'Position(x:'+str(self.x)+'; y:'+str(self.y)+')'
    
    def inArray(self,arrayPositions):
        for i in arrayPositions:
            if i.x==self.x and i.y==self.y:
                return True
        return False

class Rect(Position):
    def __init__(self,position,father,conditions=None,size=12,color='#7A7'):

        # self.rule=rule.clone()#TODO: implement a valid cloning function, this sucks!
        # self.rule.values=rule.values
        # if not conditions:
        #     #this rect will represent the first condition in a list of rules
        #     self.freeSides=self.rule.values.pop(0)
        # else:
        #     #this rect will represent the first condition that respects the rule
        #     self.freeSides=self.rule.find(conditions)
        #     self.rule.values.remove(self.freeSides)
        self.father=father
        self.size=size
        self.color=color
        super().__init__(position.x*self.size+father.x,position.y*self.size+father.y)
    def draw(self):
        canvas.create_rectangle(self.x,self.y,self.x+self.size,self.y+self.size,fill=self.color,outline='black',tags=('square'))
    # def getNext(self):
    #     return Rect(rule=self.rule,conditions=self.freeSides,size=self.size,color=self.color)


class Polyomino():
    #define a unique polyomino using a unique rule
    def __init__(self,uniquerule,x=0,y=0):
        self.x=x
        self.y=y
        self.dim=uniquerule.getDimension()
        self.uniquerule=uniquerule
        self.positions=Rule.getPositions(self.uniquerule.values)
        self.elements=[]
        for i in self.positions:
            self.elements.append(Rect(i,self))
    def draw(self):
        for i in self.elements:
            i.draw()

    #for print() function
    def __str__(self):
        return 'Polyomino('+str(self.elements)+')'
    def __repr__(self):
        return 'Polyomino('+str(self.elements)+')'
    

def PolyArea(canvas,x,y):
    canvas.create_rectangle(x,y,canvas.winfo_width()-10,canvas.winfo_height()-10,outline='black')


tk = Tk()
tk.title('Polimini')
canvas=Canvas(tk,width=WIDTH,height=HEIGHT,bg=BGCOLOR)
canvas.pack()
tk.update()
polyarea=PolyArea(canvas,10,10)
tk.update()

positionArray=[
    Position(1,0),
    Position(0,0),
    Position(-2,0),
    Position(-1,0)
]
myRule=Rule(positionArray)
print(myRule)
polyomino=Polyomino(myRule,20,20)
polyomino.draw()
print(polyomino)

tk.mainloop()