# Lorenzo Tomasello
# Exercise of the 8 queens
#python -m pip install --user numpy scipy
import numpy as np
import random

# creates new chessboard
def chessboard(dimX=8,dimY=8):
    board = []
    for i in range(dimX):
        for j in range(dimY):
            board.append({'x':i,'y':j})
    return board

# returns position of the queen
def placeQueen():
    global positions
    global chboard
    global wrongPos
    level=len(positions)
    chboard = [i for i in chboard if not i in wrongPos[level]]
    poss=len(chboard)
    if poss>0:
        print('Ho '+str(poss)+' possibilità')
        wrongPos[level+1]=[]
        rand = random.randrange(poss)
        point = chboard[rand]
        chboard=chessboardWithout(chboard,point)
        print('------------------ '+str(level+1))
        return point
    else:#level=7
        wrongPos[level-1].append(positions.pop())
        print('Ho esaurito le possibilità, torno indietro di un livello')
        print('------------------ '+str(level-1))
        chboard = chessboard()
        for p in positions:
            chboard=chessboardWithout(chboard,p)
        return placeQueen()

def drawChessboard(positions):
    board = np.zeros([8,8],dtype=str)
    x=range(len(board))
    y=range(len(board[0]))
    for i in x:
        for j in y:
            if True in [True for p in positions if p['x']==i and p['y']==j]:
                board[i][j]='Q'
            else:
                board[i][j]='_'
    printMatr(board)

# function to exclude a entire row, col and diagonals from a point given of a matrix
def chessboardWithout(mat,pos):
    global wrongPos
    global positions
    level=len(positions)+1
    matRet=[]
    for i in range(len(mat)):
        if mat[i]['x']!=pos['x']:#check row
            if mat[i]['y']!=pos['y']:#check col
                if (mat[i]['x']-mat[i]['y'])!=(pos['x']-pos['y']) and (mat[i]['x']+mat[i]['y'])!=(pos['x']+pos['y']):#check diag
                    matRet.append(mat[i])
    return matRet

# helper for matrix print
def opposite(bar):
    if bar=='/':
        return '\\'
    elif bar=='\\':
        return '/'
    elif bar=='(':
        return ')'
    else:
        return '|'

# it prints a matrix
def printMatr(mat):
    x=len(mat)
    y=len(mat[0])
    maxlen=len(str(mat[0][0]))
    for i in mat:
        for j in i:
            if maxlen<len(str(j)):
                maxlen=len(str(j))
    for i in range(x):
        for j in range(y):
            if (x==1):
                char='('
            elif (i==0):
                char='/'
            elif (i==x-1):
                char='\\'
            else:
                char='|'
            if j==0:
                print(char, end='')

            nspaces=maxlen-len(str(mat[i][j]))
            spaces=''
            for k in range(nspaces):
                spaces+=' '

            print(spaces,mat[i][j], end='')

            if j==y-1:
                print(' ',opposite(char))
            else:
                print(',', end='')

## START HERE
                
chboard = chessboard()
wrongPos = {0:[]}
positions = []
while len(positions)<8:
    positions.append(placeQueen())
print("Posizioni scelte: "+str(positions))
print("\n--------\n")
drawChessboard(positions)