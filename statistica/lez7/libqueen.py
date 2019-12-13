def drawChessboard(positions,dimX=8,dimY=8):
    board = []
    for i in range(dimX):
        board.append([])
        for j in range(dimY):
            if {"x":i,"y":j} in positions:
                board[i].append('Q')
            else:
                board[i].append('_')
    printMatr(board)


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