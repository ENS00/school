# Lorenzo Tomasello
# Exercise of the 8 queens with AI algorithm
import random
import statistics
import time
import libqueen

GOAL = 8
NUM_CHBOARD = 8
MUTATE_ODDS = 0.01
MUTATE_MIN = 0.5
MUTATE_MAX = 1.2
LITTER_SIZE = 6# num of children
GENERATION_LIMIT = 500

def getCombo():
    ret = [1,2,3,4,5,6,7,8]
    random.shuffle(ret)
    return ret

def fitness(el):
    val=0
    return val/GOAL

def recombination(father,mother):#get something from father and from the mother
    return []

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

    totfitness=0
    for el in pop:
        totfitness+=fitness(el)
    statistics.mean([fitness(el) for el in pop])
    print(pop)

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    duration = end_time - start_time
    print('\nRuntime for this program was {} seconds.'.format(duration))