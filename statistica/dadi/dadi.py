r=[1,2,3,4,5,6]
diz={}
for a in r:
    for b in r:
        for c in r:
            for d in r:
                s=a+b+c+d
                m=min(a,b,c,d)
                s-=m
                if not diz.get(s):
                    diz[s]=1
                else:
                    diz[s]+=1
print(diz)#({str(d)+":"+str(d/1296) for d in diz.values()})