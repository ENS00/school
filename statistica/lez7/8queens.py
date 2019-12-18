# Lorenzo Tomasello
# Exercise of the 8 queens with genetic algorithm
import random
import statistics
import time
import libqueen

GOAL = 28
NUM_CHBOARD = 8
MUTATION = 0.5
LITTER_SIZE = 6# num of children
GENERATION_LIMIT = 500

def getCombo():
    ret = [1,2,3,4,5,6,7,8]
    random.shuffle(ret)
    return ret

def validDiagonal(el1,pos1,el2,pos2):
    diff=pos1-pos2
    #from up left to down right
    if el1-el2+pos2-pos1 == 0:
        return False
    #from up right to down left
    if el1-el2+pos1-pos2 == 0:
        return False
    return True

def fitness(el):
    val=0
    for i in range(len(el)):
        for j in range(i+1,len(el)):
            if validDiagonal(el[i],i,el[j],j):
                val+=1
    return val/GOAL

def recombination(father,mother):#get something from father and from the mother
    start=random.randint(0,3)
    son=list(father)[start:start+4]
    for i in mother:
        if i not in son:
            son.append(i)
    return son

def breed(pop,litter_size):#sistemare!!
    npop=len(pop)
    pop1=pop[:npop//2]
    pop2=pop[npop//2:npop]
    children=[]
    for i in range(litter_size):
        children.append(recombination(pop1[random.randint(0,len(pop1)-1)],pop2[random.randint(0,len(pop2)-1)]))
    return children

def mutate(el):
    p1 = random.randint(0,7)
    p2 = random.randint(0,6)
    if p2>=p1:
        p2+=1
    el[p2],el[p1]=el[p1],el[p2]
    return el

def main():
    gen = 0
    pop=[]
    #populate
    for i in range(NUM_CHBOARD):
        pop.append(getCombo())
    pop.sort(key=fitness,reverse=True)
    everyfitness=[fitness(el) for el in pop]
    totfitness=statistics.mean(everyfitness)

    while totfitness<1 and gen<GENERATION_LIMIT:
        print('Generation: '+str(gen))
        gen+=1
        print(pop)
        print(totfitness)

        #get babies
        children=breed(pop,LITTER_SIZE)
        #use random special abilities
        for i in range(len(children)):
            if random.random()<MUTATION:
                children[i]=mutate(children[i])
        #add them to population
        pop.extend(children)
        #sort by fitness
        pop.sort(key=fitness,reverse=True)
        #kill idiots
        pop=pop[:8]

        everyfitness=[fitness(el) for el in pop]
        totfitness=statistics.mean(everyfitness)
    if totfitness==1:
        for i in pop:
            p=[]
            [p.append({"x":i.index(j),"y":j-1}) for j in i]
            libqueen.drawChessboard(p)

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    duration = end_time - start_time
    print('\nRuntime for this program was {} seconds.'.format(duration))