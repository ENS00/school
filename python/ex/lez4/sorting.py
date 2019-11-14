def selectionSort(iterab):
    nelem = len(iterab)
    for k in range(nelem-2):
        m=k
        for j in range(k+1,nelem):
            if iterab[j]<iterab[m]:
                m=j
        iterab[m],iterab[k] = iterab[k],iterab[m]
        print(iterab)

def insertionSort(iterab):
    nelem = len(iterab)
    for i in range(1,nelem):
        for j in range(i):
            if iterab[j]>iterab[i]:
                el=iterab.pop(i)
                iterab.insert(j,el)
                print(iterab)
                break

def bubbleSort(iterab):
    nelem = len(iterab)
    for i in range(nelem):
        for j in range(1,nelem-i):
            if iterab[j]<iterab[j-1]:
                iterab[j],iterab[j-1] = iterab[j-1],iterab[j]
        print(iterab)

lista = [7,2,4,5,3,1]
print(lista)
bubbleSort(lista)