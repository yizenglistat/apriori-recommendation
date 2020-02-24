import sys

def main():
    buckets = []
    filename = sys.argv[1]
    minsupport = int(sys.argv[2])
    nbuckets = int(sys.argv[3])
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            buckets.append(line.strip().split())
    itemiddic, finalist1, finalfreq1 = size1freqset(minsupport,nbuckets,buckets)
    finalist2, finalfreq2 = size2freqset(minsupport,nbuckets,itemiddic,buckets,finalist1)
    finalist3, finalfreq3 = size3freqset(minsupport,nbuckets,itemiddic,buckets,finalist2)
    output(finalfreq1,finalfreq2,finalfreq3,filename='output.txt')
    
def size1freqset(minsupport,nbuckets,buckets):

    "Creating Candidate List of Size 1"
    candidatelist1=[]
    finalist1=[]
    finalfreq1={}

    for i in range(0, len(buckets)):
        for b in buckets[i]:
            candidatelist1.append(b)

    candidatelist1=sorted(set(candidatelist1))

    "Appending frequent items of size 1 to finallist1"
    lala=0
    for k in candidatelist1:
        for i in range(0, len(buckets)):
            for j in buckets[i]:
                if(k==j):
                    lala+=1
        if lala>=minsupport:
            finalist1.append(k)
            finalfreq1[(k,)]=lala
        lala=0

    itemiddic={}
    counter=1
    for c in candidatelist1:
        itemiddic[c]=counter
        counter+=1

    return itemiddic, finalist1, finalfreq1 

def size2freqset(minsupport,nbuckets,itemiddic,buckets,finalist1):

    k=3

    countofbuckets=[0]*nbuckets
    bitmap=[0]*nbuckets
    pairs=[]

    "PCY Pass 1"
    for i in range(0,len(buckets)):
        for x in range(0,len(buckets[i])-1):
            for y in range(x+1,len(buckets[i])):
                if(buckets[i][x]<buckets[i][y]):
                    countofbuckets[int(str(itemiddic[buckets[i][x]])+str(itemiddic[buckets[i][y]]))%nbuckets]+=1
                    if ([buckets[i][x],buckets[i][y]] not in pairs):
                        pairs.append(sorted([buckets[i][x],buckets[i][y]]))
                else:
                    countofbuckets[int(str(itemiddic[buckets[i][y]])+str(itemiddic[buckets[i][x]]))%nbuckets]+=1
                    if ([buckets[i][y],buckets[i][x]] not in pairs):
                        pairs.append(sorted([buckets[i][y],buckets[i][x]]))

    pairs=sorted(pairs)

    for x in range(0,len(countofbuckets)):
        if countofbuckets[x]>=minsupport:
            bitmap[x]=1
        else:
            bitmap[x]=0

    prunedpairs=[]

    "Checking condition 1 of PCY Pass 2"

    for i in range(0,len(pairs)):
        for j in range(0,len(pairs[i])-1):
            if(pairs[i][j] in finalist1 and pairs[i][j+1] in finalist1):
                prunedpairs.append(pairs[i])

    candidatelist2=[]

    "Checking condition 2 of PCY Pass 2"
    for i in range(0, len(prunedpairs)):
        for j in range(0,len(prunedpairs[i])-1):
            if bitmap[int(str(itemiddic[prunedpairs[i][j]])+str(itemiddic[prunedpairs[i][j+1]]))%nbuckets]==1:
                candidatelist2.append(prunedpairs[i])
    
    "Appending frequent items of size 2 to finallist2"
    finalist2=[]
    finalfreq2={}
    counter=0
    for c in range(0,len(candidatelist2)):
        for b in range(0,len(buckets)): 
            if set(candidatelist2[c]).issubset(set(buckets[b])):
                counter+=1
        if counter>=minsupport and counter!=0:
            finalist2.append(sorted(candidatelist2[c]))
            finalfreq2[tuple(candidatelist2[c])]=counter
        counter=0

    finalist2=sorted(finalist2)

    return finalist2, finalfreq2


def size3freqset(minsupport,nbuckets,itemiddic,buckets,prevout,k=3):

    "Creating Candidate List of Size k"

    kcountofbuckets=[0]*nbuckets
    kbitmap=[0]*nbuckets
    kcombination=[]
    prevout=prevout

    "Make k combination e.g. triplets"
    for a in prevout:
        for b in prevout:
            if(a!=b):
                if set(a) & set(b) and len(list(set(a) & set(b))) >= k-2:
                    kcombination.append(sorted(set(a)|set(b)))

    # print("checking kcombination")
    kcombination=sorted(kcombination)

    "PCY Pass 1 Hashing"

    hashingstring=""

    for i in range(0,len(kcombination)):
        for x in kcombination[i]:
            hashingstring+=str(itemiddic[x])
        kcountofbuckets[int(hashingstring)%nbuckets]+=1
        hashingstring=""

    for x in range(0,len(kcountofbuckets)):
        if kcountofbuckets[x]>=minsupport:
            kbitmap[x]=1
        else:
            kbitmap[x]=0

    "Condition 1 is automatically satisfied"

    "Checking condition 2 of PCY Pass 2"
    hashingstring=""
    klist=[]

    for i in range(0, len(kcombination)):
        for j in kcombination[i]:
            hashingstring+=str(itemiddic[j])
        if kbitmap[int(hashingstring)%nbuckets]==1:
            klist.append(kcombination[i])
        teststring=""

    "Creating Candidate List of Size k"
    candidatelistk=[]
    count=1
    for i in range(1, len(klist)):
        if klist[i]==klist[i-1]:
            count+=1
        else:
            # print("ELement is: ",klist[i-1]," and count is: ",count)
            if count>=k:
                candidatelistk.append(klist[i-1])
            count=1
    if count>=k:
        candidatelistk.append(klist[i-1])
        # print("ELement is: ",klist[i-1]," and count is: ",count)

    "Appending frequent items of size k to output"
    finalist3=[]
    counter=0
    finalfreq3={}
    for c in range(0,len(candidatelistk)):
        for b in range(0,len(buckets)):
            if set(candidatelistk[c]).issubset(set(buckets[b])):
                counter+=1
        if counter>=minsupport and counter!=0:
            finalist3.append(candidatelistk[c])
            finalfreq3[tuple(candidatelistk[c])]=counter
        counter=0

    return finalist3, finalfreq3

def confidence(ifBuy,thenBuy,top=5):
    '''Generate confidence scores with a given size and return top 5 rules.'''
    confidence = {}
    for comb, count in thenBuy.items():
        confidence[comb] = count/ifBuy[tuple(comb[:-1])]
    confidence = sorted(confidence.items(), key=lambda item: (-item[1], item[0]))
    return confidence[:top]

def output(finalfreq1,finalfreq2,finalfreq3,filename='output.txt'):
    '''Save results into a txt file'''
    pairs = confidence(finalfreq1,finalfreq2)
    triples = confidence(finalfreq2,finalfreq3)
    with open(filename, 'w') as f:
        f.write('OUTPUT A'+'\n')
        for comb, conf in pairs:
            f.write(' '.join(comb)+str(' ')+str(conf)+str('\n'))
        f.write('OUTPUT B'+'\n')
        for comb, conf in triples:
            f.write(' '.join(comb)+str(' ')+str(conf)+str('\n'))

main();
