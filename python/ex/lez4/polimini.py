from tkinter import *

WIDTH=600
HEIGHT=400
SIZE=12
BGCOLOR='lightgreen'
npoly=None
ignoredpositions=[]

def getCombinations():
    # global npoly
    # mat = []
    # for i in range(npoly):
    #     row = []
    #     for j in range(npoly):
    #         row.append(False)
    #     mat.append(row)
    # # starting from 0,0
    # mat[0][0]=True
    # # I can add a mono near another existent
    # combination = mat.copy()
    global npoly
    global ignoredpositions

    allCombo=[]
    returnCombo=[]
    ignoredpositions={}
    ignoredpositions[0]=[]
    combination=[]
    combination=attachUnit([{'x':0,'y':0}],allCombo)

    while len(combination)>0:
        if not exists(combination,allCombo):
            returnCombo.append(combination)
        allCombo.append(combination)
        combination=[]
        combination=attachUnit([{'x':0,'y':0}],allCombo)

    allCombo.append(combination)
    if not exists(combination,allCombo):
        returnCombo.append(combination)

    return returnCombo

def attachUnit(positions,allCombo):
    global npoly
    global ignoredpositions
    currentLevel=len(positions)
    if currentLevel not in ignoredpositions:
        ignoredpositions[currentLevel]=[]
    if currentLevel<npoly:
        for p in reversed(positions):
            myPos={'x':p['x']+1,'y':p['y']}
            if (myPos not in positions) and (myPos not in ignoredpositions[currentLevel]) and (positions+[myPos] not in allCombo):
                positions.append(myPos)
                return attachUnit(positions,allCombo)
            else:
                myPos={'x':p['x'],'y':p['y']+1}
                if (myPos not in positions) and (myPos not in ignoredpositions[currentLevel]) and (positions+[myPos] not in allCombo):
                    positions.append(myPos)
                    return attachUnit(positions,allCombo)
        fakepos=positions.pop()
        currentLevel=len(positions)
        # if i'm setting to ignore position (0,0) we found all combinations
        if currentLevel==0:
            return []
        ignoredpositions[currentLevel].append(fakepos)
        return attachUnit(positions,allCombo)
    else:
        return positions

#it checks also for rotated poly
def exists(combo,array):
    rotated=combo.copy()
    for i in range(4):
        rotated=rotate(rotated)
        if {'x':0,'y':0} not in rotated:
            continue
        for el in array:
            matches=0
            for pos in rotated:
                if pos in el:
                    matches+=1
            if matches==len(rotated):
                return True

    return False

# sets positions of a rotated poly
def rotate(positions,deg=90):
    deg=deg%360-deg%90
    minx=0
    miny=0
    retpos=[]
    if deg==90:
        for p in range(len(positions)):
            retpos.append({'x':-positions[p]['y'],'y':positions[p]['x']})
            if minx>retpos[p]['x']:
                minx=retpos[p]['x']
            if miny>retpos[p]['y']:
                miny=retpos[p]['y']
        
    elif deg==180:
        for p in range(len(positions)):
            retpos.append({'x':-positions[p]['x'],'y':-positions[p]['y']})
            if minx>positions[p]['x']:
                minx=positions[p]['x']
            if miny>positions[p]['y']:
                miny=positions[p]['y']
        
    elif deg==270:
        for p in range(len(positions)):
            retpos.append({'x':positions[p]['y'],'y':-positions[p]['x']})
            if minx>positions[p]['x']:
                minx=positions[p]['x']
            if miny>positions[p]['y']:
                miny=positions[p]['y']
    else:
        return []
    # # translate it
    for p in retpos:
        p['x']-=minx
        p['y']-=miny
    return retpos

##graphics

class Square():
    def __init__(self,x,y,size,color):
        canvas.create_rectangle(x,y,x+size,y+size,fill=color,outline='black',tags=('square'))

class PolyArea():
    def __init__(self,canvas,x,y):
        self.canvas=canvas
        self.x=x
        self.y=y
        self.shape=canvas.create_rectangle(x,y,canvas.winfo_width()-10,canvas.winfo_height()-10,outline='black')

tk = Tk()
tk.title('Polimini')
canvas=Canvas(tk,width=WIDTH,height=HEIGHT,bg=BGCOLOR)
canvas.pack()
tk.update()
polyarea=PolyArea(canvas,200,10)
tk.update()

def calculatePolyomino():
    global polyarea
    global npoly
    global inputval
    npoly=inputval.get()
    if npoly>1:
        comboLen=npoly*SIZE
        spacex=0
        spacey=0
        c=0
        d=0
        canvas.delete('square')
        combinations=getCombinations()
        for squares in combinations:
            for el in squares:
                if polyarea.x + (c+1)*SIZE + spacex > WIDTH-40:
                    d+=1
                    c=0
                    spacey+=SIZE*3
                    spacex=0
                Square(polyarea.x+10 + el['x']*SIZE + c*SIZE+spacex, polyarea.y+10 + el['y']*SIZE + d*SIZE+spacey, SIZE, '#7A7')
            c+=npoly
            spacex+=SIZE

lbl=Label(tk,text='Scrivi un numero:')
lbl.place(x=10,y=10)
inputval=IntVar()
inputnumber=Entry(tk,width=5,textvariable=inputval)
inputnumber.place(x=120,y=10)
calculate=Button(tk,text='Calcola',command=calculatePolyomino)
calculate.place(x=50, y=40)

tk.mainloop()