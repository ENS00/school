# Lorenzo Tomasello v. 1.0.1
# multiplication of 2 matrices
def matrMult(matA,matB):
    matRet=[]
    xA=len(matA)
    xB=len(matB)
    yA=len(matA[0])
    yB=len(matB[0])
    # it's possible to multiply only if nCols of matrA are the same of nRows of matrB
    if xB==yA:
        for i in range(xA):
            row=[]
            matRet.append(row)
            for j in range(yB):
                val=0
                for k in range(xB):
                    val+=matA[i][k]*matB[k][j]
                row.append(val)
        return matRet
    return None

# transpose of a matrix
def matrTrasp(mat):
    matRet=[]
    x=range(len(mat))
    y=range(len(mat[0]))
    for i in x:
        row=[]
        matRet.append(row)
        for j in y:
            row.append(mat[j][i])
    return matRet

# determinant of a matrix
def matrDet(mat):
    x=len(mat)
    if x==len(mat[0]):
        # if x>1:
        if x>2:
            result=0
            for i in range(x):
                myMat = matrWithout(mat,i,0)
                result+=matrDet(myMat)*mat[i][0]*(1-i%2*2)
            return result
        elif x==2:
            return mat[0][0]*mat[1][1]-mat[0][1]*mat[1][0]
        elif x==1:
            return mat[0][0]
    return None

# function to exclude an entire row and col from a point given of a matrix
def matrWithout(mat,posx,posy):
    matRet=[]
    x=range(len(mat))
    y=range(len(mat[0]))
    for i in x:
        if i!=posx:
            row=[]
            matRet.append(row)
            for j in y:
                if j!=posy:
                    row.append(mat[i][j])
    return matRet

def matrCA(mat):
    matRet=[]
    x=len(mat)
    if x>1:
        y=len(mat[0])
        if y>1:
            for i in range(x):
                matRet.append([])
                for j in range(y):
                    sign=-1
                    if (i+j)%2==0:
                        sign=1
                    matRet[i].append(sign*matrDet(matrWithout(mat,i,j)))
            return matRet
    return None

# every number inside a matrix is divided by n
def matrDivN(mat,n):
    matRet=[]
    for i in mat:
        row=[]
        matRet.append(row)
        for j in i:
            row.append(j/n)
    return matRet

# returns the inverse of a matrix (at the moment it works only for 2x2)
def matrInv(mat):
    d=matrDet(mat)
    if d!=0:
        return matrDivN(matrCA(matrTrasp(mat)),d)

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

# test examples are commented

# matA=[[1,2],[3,4]]
# matB=[[1,1],[2,0]]
# matA=[[2,1],[0,1]]
# matB=[[3,1],[0,4]]

# matA=[[1,2,3,5],
#       [2,-7,8,0],
#       [6,9,1,-3]]
# matB=[[1,0],
#       [3,-6],
#       [5,2],
#       [7,-8]]
matA=[[1,2,3],[0,4,5],[1,0,6]]


# matC=matrMult(matA,matB)
# print('Da = '+str(matrDet(matA)))
# print('Db = '+str(matrDet(matB)))
# print('Dc = '+str(matrDet(matC)))
printMatr(matA)
# printMatr(matB)
# printMatr(matC)
inv=matrInv(matA)
printMatr(matrInv(matA))
printMatr(matrInv(inv))

# mat=[[1,2,1,1,6,2,5,8],
#      [2,1,3,1,2,6,0,-6],
#      [0,2,2,0,7,-4,-1,-3],
#      [1,2,0,0,-1,0,-1,-2],
#      [4,-1,2,2,0,-3,3,0],
#      [5,2,1,1,1,0,-8,-3],
#      [-2,2,6,1,5,1,-2,-2],
#      [7,1,0,-2,3,-4,-5,-6]]
# printMatr(mat)
# printMatr(matrInv(mat))
# print("D: "+str(matrDet(mat)))

# mat=[[4,3,2,2],[0,1,-3,3],[0,-1,3,3],[0,3,1,1]]
# printMatr(mat)
# print("D: "+str(matrDet(mat)))