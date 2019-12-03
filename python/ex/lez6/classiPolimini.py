from tkinter import (Tk,Canvas,Label,Button)
from operator import attrgetter

WIDTH=600
HEIGHT=400
BGCOLOR='lightgreen'
button=None
lblid=None
lblclass=None

#rules are adiacent free sides for every square

def sortFunction(a,b):
    if a.y>b.y:
        return b
    if a.y<b.y:
        return a
    if a.x>b.y:
        return b
    return a

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
        ret='{'
        for i in self.values:
            ret+=str(i)+', '
        ret=ret[:-2]+'}'
        return ret
    def __repr__(self):
        return 'Rule('+str(self.values)+')'

    def clone(self):
        return Rule(self.positions)
    
    def getDimension(self):
        return len(self.values)
    
    @staticmethod
    def orderPositions(positions):
        positions=list(positions)
        positions.sort(key=attrgetter('x'))
        positions.sort(key=attrgetter('y'))
        return positions

    #inverse algorithm to find all positions starting from rules
    @staticmethod
    def getPositions(values):
        values=list(values)
        currentvalues=[]
        start=Position(0,0)
        # positions=[]
        # newvalues=list()
        # [newvalues.append(None) for i in range(len(values))]
        # lastvalue=None
        level={0:{'values':0,'currentvalues':0,'lasttry':0}}
        backupvalues={}
        deep=0
        while len(values)>0:
            level[deep+1]={'values':0,'currentvalues':0,'lasttry':0}
            found=False
            backupvalues[deep]=list(values)
            for i in range(level[deep]['values'],len(values)):
                currentvalue=values[i]
                if deep==0:
                    level[deep]['values']+=1
                    currentvalues.append({
                        'position':start,
                        'value':currentvalue
                    })
                    found=True
                    break
                else:
                    for j in range(level[deep]['currentvalues'],len(currentvalues)):
                        #print('Trying merge '+str(values[i])+' and '+str(currentvalues[j]['value']))
                        #trying to attach to the up
                        if 2 not in values[i] and 0 not in currentvalues[j]['value'] and level[deep]['lasttry']<1:
                            pos=Position(currentvalues[j]['position'].x,currentvalues[j]['position'].y)
                            pos.move(0,-1)
                            if not pos.inArray(currentvalues):
                                currentvalues.append({
                                    'position':pos,
                                    'value':values[i]
                                })
                                level[deep]['lasttry']=1
                                found=True
                        #trying to attach to the right
                        elif 3 not in values[i] and 1 not in currentvalues[j]['value'] and level[deep]['lasttry']<2:
                            pos=Position(currentvalues[j]['position'].x,currentvalues[j]['position'].y)
                            pos.move(1,0)
                            if not pos.inArray(currentvalues):
                                currentvalues.append({
                                    'position':pos,
                                    'value':values[i]
                                })
                                level[deep]['lasttry']=2
                                found=True
                        #trying to attach to the down
                        elif 0 not in values[i] and 2 not in currentvalues[j]['value'] and level[deep]['lasttry']<3:
                            pos=Position(currentvalues[j]['position'].x,currentvalues[j]['position'].y)
                            pos.move(0,1)
                            if not pos.inArray(currentvalues):
                                currentvalues.append({
                                    'position':pos,
                                    'value':values[i]
                                })
                                level[deep]['lasttry']=3
                                found=True
                        #trying to attach to the left
                        elif 1 not in values[i] and 3 not in currentvalues[j]['value'] and level[deep]['lasttry']<4:
                            pos=Position(currentvalues[j]['position'].x,currentvalues[j]['position'].y)
                            pos.move(-1,0)
                            if not pos.inArray(currentvalues):
                                currentvalues.append({
                                    'position':pos,
                                    'value':values[i]
                                })
                                level[deep]['lasttry']=4
                                found=True
                        else:
                            level[deep]['currentvalues']+=1
                            level[deep]['lasttry']=0
                        if found:
                            break
                    if found:
                        break
                level[deep]['values']+=1
                level[deep]['currentvalues']=0
            if not found:
                #it's impossible to attach this at the moment, let's remove the last one and retry
                if len(currentvalues)<1:
                    raise Exception('Cannot create a Polyomino with this rule')
                currentvalues.pop()
                deep-=1
                values=backupvalues[deep]
            else:
                values.remove(currentvalue)
                deep+=1
            # print()
            # print(level)
            # print('Possibilities: '+str(values))
            # print('Current choose: '+str(currentvalues))
            # print()
        minX=900
        minY=900
        for el in currentvalues:
            if el['position'].x<minX:
                minX=el['position'].x
            if el['position'].y<minY:
                minY=el['position'].y
        positions=[]
        for el in currentvalues:
            el['position'].move(-minX,-minY)
            positions.append(el['position'])
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
            if i['position'].x==self.x and i['position'].y==self.y:
                return True
        return False

class Rect(Position):
    def __init__(self,position,father,conditions=None,size=26,color='#7A7'):
        self.father=father
        self.size=size
        self.color=color
        super().__init__(position.x*self.size+father.x,position.y*self.size+father.y)
    def draw(self):
        canvas.create_rectangle(self.x,self.y,self.x+self.size,self.y+self.size,fill=self.color,outline='black',tags=('square'))


class Polyomino():
    #define a unique polyomino using a unique rule
    def __init__(self,uniquerule,x=0,y=0):
        self.x=x
        self.y=y
        self.dim=uniquerule.getDimension()
        self.uniquerule=uniquerule
        self.positions=Rule.getPositions(self.uniquerule.values)
        self.positions=Rule.orderPositions(self.positions)
        self.elements=[]
        for i in self.positions:
            self.elements.append(Rect(i,self))
    def draw(self):
        global lblclass
        global lblid
        for i in self.elements:
            i.draw()
        lblclass=Label(tk,text="Classe: "+str(self.getClass()))
        lblclass.place(x=300,y=160)
        lblid=Label(tk,text="Id: "+str(self.uniquerule))
        lblid.place(x=300,y=200)
    def getClass(self):
        myclass=0
        for i in self.positions:
            if True in [True for j in self.positions if j.y==i.y and j.x==i.x+1]:
                    myclass+=1
            if True in [True for j in self.positions if j.y==i.y+1 and j.x==i.x]:
                    myclass+=1
        return myclass

    #for print() function
    def __str__(self):
        return 'Polyomino('+str(self.elements)+')'
    def __repr__(self):
        return 'Polyomino('+str(self.elements)+')'

    @staticmethod
    def fromPositionArray(array,x=0,y=0):
        myRule=Rule(array)
        return Polyomino(myRule,x,y)



lvl5=[[
        Position(0,-1),
        Position(-1,0),
        Position(-1,-2),
        Position(-1,-1),
        Position(-1,-3)
    ],[
        Position(0,-1),
        Position(0,0),
        Position(0,-2),
        Position(0,-4),
        Position(0,-3)
    ],[
        Position(1,0),
        Position(2,0),
        Position(2,1),
        Position(0,1),
        Position(1,1)
    ]
]

def PolyArea(canvas,x,y):
    canvas.create_rectangle(x,y,canvas.winfo_width()-10,canvas.winfo_height()-10,outline='black')

def drawNext(id):
    global button
    global lblid
    global lblclass
    if id>=len(lvl5):
        id=0
    tk.update()
    polyarea=PolyArea(canvas,10,10)
    canvas.delete('square')
    if button:
        button.destroy()
    if lblid:
        lblid.destroy()
    if lblclass:
        lblclass.destroy()
    button=Button(tk,text='Successivo',command=lambda:drawNext(id+1))
    button.place(x=300, y=50)
    tk.update()
    polyomino=Polyomino.fromPositionArray(lvl5[id],140,140)
    polyomino.draw()


tk = Tk()
tk.title('Polimini')
canvas=Canvas(tk,width=WIDTH,height=HEIGHT,bg=BGCOLOR)
canvas.pack()
drawNext(0)

tk.mainloop()