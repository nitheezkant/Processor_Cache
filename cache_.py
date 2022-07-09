import sys
import math

sys.stdout = open('output.txt', 'w')

#class cache, that can be configured according to need.
class configurable_cache:
    
    #Class variables, initalised to 0

    #Main cache memory unit
    cache=[]
    
    #Tracking variables
    hits=0
    misses=0

    #Inputed variables
    ways=0
    size=0
    block=0

    #Calculated variables
    lines=0
    index=0
    offset=0
    tag=0

    #Initialisation function to set up the cache
    def __init__(self,ways,size,block):

        #Load inputed variables
        self.ways=ways
        self.size=size
        self.block=block

        #Load calculated variables
        self.lines= int((size * 1024)/ (block * ways))
        self.index=int(math.log(self.lines,2))
        self.offset=int(math.log(block,2))
        self.tag=32-self.index-self.offset

        #Initialise memory locations
        x=0
        for i in range(self.lines):
            line=[format(x, "032b")]
            for way in range(ways):
                line.append([0,"tagbit","data",0])
            self.cache.append(line)
            x=x+self.tag
    
    #Function to try a cache lookup, see if it is a hit, and cache it if not
    def cache_lookup(self,p):
        
        #Slice the trace
        tag =p[0:self.tag]
        add=int(p[self.tag:self.tag+self.index],2)
        cache_line=self.cache[add]

        #Check if it's a hit 
        flag=1      
        for i in range(1,self.ways+1):  
            if (cache_line[i][0]==1):
                if(tag==cache_line[i][1]):
                    self.hits=self.hits+1
                    #Increase the importance of the way
                    self.cache[add][i][3]=self.cache[add][i][3]+1
                    flag=0
    
        #If miss, then cache it
        if flag==1:
            self.misses=self.misses+1

            #check if any way is free, if yes, use it
            flag2=1
            for i in range(1,self.ways+1):
                if (cache_line[i][0]==0):
                    self.cache[add][i][1]=tag
                    self.cache[add][i][0]=1
                    flag2=0
                    break

            #If all ways are full, then remove least important one and cache it 
            if flag2==1:
                min=sys.maxsize
                min_ind=-1
                for i in range(1,self.ways+1):
                    if(self.cache[add][i][3]<min):
                        min=self.cache[add][i][3]
                        min_ind=i
                self.cache[add][min_ind][1]=tag
                self.cache[add][min_ind][0]=1
                self.cache[add][min_ind][3]=0



#Main-Driver Code

#1 A
tests=[["gcc.trace",4,512,4,"1"],["gzip.trace",4,512,4,"1"],["mcf.trace",4,512,4,"1"],["swim.trace",4,512,4,"1"],["twolf.trace",4,512,4,"1"]]

#1 B
#tests=[["gcc.trace",4,2048,4,"1 b"],["gzip.trace",4,2048,4,"1 b"],["mcf.trace",4,2048,4,"1 b"],["swim.trace",4,2048,4,"1 b"],["twolf.trace",4,2048,4,"1 b"]]

#1 C
#tests=[["gcc.trace",4,512,1,"1 c"],["gcc.trace",4,512,4,"1 c"],["gcc.trace",4,512,8,"1 c"],["gcc.trace",4,512,16,"1 c"],["gzip.trace",4,512,1,"1 c"],["gzip.trace",4,512,4,"1 c"],["gzip.trace",4,512,8,"1 c"],["gzip.trace",4,512,16,"1 c"],["mcf.trace",4,512,1,"1 c"],["mcf.trace",4,512,4,"1 c"],["mcf.trace",4,512,8,"1 c"],["mcf.trace",4,512,16,"1 c"],["swim.trace",4,512,1,"1 c"],["swim.trace",4,512,4,"1 c"],["swim.trace",4,512,8,"1 c"],["swim.trace",4,512,16,"1 c"],["twolf.trace",4,512,1,"1 c"],["twolf.trace",4,512,4,"1 c"],["twolf.trace",4,512,8,"1 c"],["twolf.trace",4,512,16,"1 c"]]

print("    Welcome to our cache demonstration!    ")
print("===========================================")
countt=1
for test in tests:
    print("***************************************************")
    print("          Test",countt,",as part of question",test[4],"   ")
    print("---------------------------------------------------")
    sys.stdin = open(test[0], 'r')
    my_cache=configurable_cache(test[1],test[2],test[3])
    while True:
        k=input()
        if k=="end":
            break
        else:
            line=(bin(int(k[4:12], 16)))[2:].zfill(32)
            my_cache.cache_lookup(line)
    print("Analysis for a ", test[1]," way set-associative cache with a\nmemory of ", test[2],"kb and block size of ",test[3],"bytes in the\ntrace file",test[0], " is:")
    print("")
    print("Hits=",my_cache.hits)
    print(" ")
    print("Misses=",my_cache.misses)
    print("")
    print("Hit rate=",(my_cache.hits/(my_cache.hits+my_cache.misses))*100,"%")
    print("")
    countt=countt+1
