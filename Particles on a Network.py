# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 11:30:59 2024

@author: Tobias Brewer
"""

import matplotlib
import random


class Edge2D:
    i,j = 0,1 #Connects nodes 0 and 1
    idx=-1 #Edge Index = -1
    def __init__(self, *args, **kwargs):
        self.i = args[0] #"Lower" Node
        self.j = args[1] #"Upper" Node
        if(kwargs.__contains__('idx')):
            self.idx=kwargs['idx'] #Edge ID

    def __next__(self,Elist):
        l=len(Elist)
        return Elist[(self.idx+1)%l]
    
    def __prev__(self,Elist):
        l=len(Elist)
        return Elist[(self.idx-1)%l]
    #Scroll through edges
    
    def __move__(self, *args):
        self.i,self.j=args[0],args[1]
    #Move edge
    
    def echeck(self, *args):
        if args[0]==self.i:
            return self.j
        else:
            return self.i
    #Checks which node is at the opposing end of edge
            
    def __delete__(self,Nlist,Elist):
        (Nlist[self.i].iel).remove(self.idx)
        (Nlist[self.j].iel).remove(self.idx)
        Elist[self.idx]=None #Delete edge from list
        return None
    #Delete Edge

    def __str__(self):
        return 'Edge {} connecting nodes {} and {}'.format(self.idx,self.i,self.j)
    #Define String


class Node2D:
    def __init__(self, *args, **kwargs):
        self.i = args[0] #X position
        self.j = args[1] #Y position
        self.w = args[2] #Weight
        self.iel = [] #Internal edge list
        self.ipl = -1 #Internal particle list

        ###DEFAULTS
        self.idx=-1 #Node Index = -1
        self.edge_max=0 #Maximum edges = 0
        if(kwargs.__contains__('idx')):
            self.idx=kwargs['idx'] #Edge ID
        if(kwargs.__contains__('conn')):
            self.edge_max=kwargs['conn'] #Connectivity

    def __next__(self,Nlist):
        l=len(Nlist)
        return Nlist[(self.idx+1)%l]
    
    def __prev__(self,Nlist):
        l=len(Nlist)
        return Nlist[(self.idx-1)%l]
    #Scroll through nodes

    def __move__(self, *args):
        self.i=args[0]
    #Move node
    
    def ocheck(self):
        if self.ipl==-1:
            occ=False
        else:
            occ=True
        return occ
    #Occupancy check
    
    def __delete__(self,Nlist,Elist,Plist):
        ne=len(self.iel) #Number of edges connected to node
        for a in range(len(self.iel)): #For each related edge
            Elist[self.iel[ne-a-1]].__delete__(Nlist, Elist)
            #Delete Edges in reverse order in list
        if self.ocheck(): #If node occupied
            Plist[self.ipl].__delete__(Nlist, Plist) #Delete occupying particle
        Nlist[self.idx]=None #Delete node from list
        return None
    #Delete Node

    def __str__(self):
        return 'Node {} at co-ord {},{}'.format(self.idx,self.i,self.j)
    

class Particle2D:
    def __init__(self, *args, **kwargs):
        self.i = args[0] #Node occupying

        ###DEFAULTS
        self.idx=-1 #Particle Index = -1
        if(kwargs.__contains__('idx')):
            self.idx=kwargs['idx']

    def __next__(self,Plist):
        l=len(Plist)
        return Plist[(self.idx+1)%l]
    
    def __prev__(self,Plist):
        l=len(Plist)
        return Plist[(self.idx-1)%l]
    #Scroll through particles

    def __move__(self, Nlist, *args):
        Nlist[0].ipl=-1; #Empty node's internal particle list
        self.i=args[0] #Update particle's node
        print(self.i)
        Nlist[self.i].ipl=self.idx #Update next node's internal particle list
        
    #Move particle

    def __delete__(self,Nlist,Plist):
        (Nlist[self.i].ipl).remove(self.idx) #Remove particle from nodes internal list
        Plist[self.idx]=None #Delete particle from list
        return None
    #Delete Node

    def __str__(self):
        return 'Particle {} on node {}'.format(self.idx,self.i)

    
class NetworkPart:
    #2D Network where nodes are randomnly connected
    ###GENERATE PARTICLE ACTIVITY
    
    N = 0 #0 Nodes in network
    def __init__(self, *args, **kwargs):
        self.N = args[0]
        self.M = args[1]
        self.p = args[2] #Number of particles
        self.Nlist=[] #List of nodes
        self.Elist=[] #List of edges
        self.Plist=[] #List of particles
        matplotlib.pyplot.figure() #New figure
        matplotlib.pyplot.xlim([0,100])
        matplotlib.pyplot.ylim([0,100])
        for a in range(self.N): #Nodes
            self.i=round(random.random()*100,2)
            self.j=round(random.random()*100,2)
            self.w=round(random.random(),2)
            (self.Nlist).append(Node2D(self.i,self.j,self.w,idx=a,conn=self.N)) #Add each node to list
            print((self.Nlist[a]).__str__()) #Print node
            matplotlib.pyplot.plot(self.i,self.j,'bo',markersize=20) #Plot node
        matplotlib.pyplot.show
        print("\n")
        for a in range(self.M): #Edges
            print("\n")
            l=random.randint(0,self.N-1) #Random node
            r=random.randint(0,self.N-1) #Random node
            (self.Elist).append(Edge2D(l,r,idx=a)) #Add edge to list
            print((self.Elist[a]).__str__()) #Print edge
            ((self.Nlist[l]).iel).append(a) #Add edge to list within node
            ((self.Nlist[r]).iel).append(a) #and other node       
            matplotlib.pyplot.plot([self.Nlist[l].i,self.Nlist[r].i],[self.Nlist[l].j,self.Nlist[r].j],'r-') #Plot edge 
        matplotlib.pyplot.show
        print("\n")
        for a in range(self.p): #Particles
            r=random.randint(0,self.N-1) #Random node
            while(self.Nlist[r].ocheck()==True): #Until empty
                r=random.randint(0,self.N-1) #Pick a random node
            (self.Plist).append(Particle2D(r,idx=a)) #Add particle to list
            (self.Nlist[r]).ipl=a #Add particle to list within node
            print((self.Plist[a]).__str__()) #Print particle

    def __addedge__(self, *args):
        self.a,self.b=args[0],args[1]
        L=len(self.Elist)
        (self.Elist).append(Edge2D(self.a,self.b,idx=L))
        ((self.Nlist[self.a]).iel).append(L) #Add edge to list within node
        ((self.Nlist[self.b]).iel).append(L) #Add edge to list within node
        self.M=L+1
        #Add edge with ends args[0] and args[1] and index = M-1
        #M is new number of edges

    def __addnode__(self, *args):
        (self.i)=args[0]
        (self.Nlist).append(Node2D(self.i,0,idx=self.N,conn=self.N+1))
        self.N=self.N+1
        
    def __addparticle__(self, *args):
        (self.i)=args[0]
        (self.Plist).append(Particle2D(self.i,idx=self.p))
        self.p=self.p+1
        
    def __moveedge__(self, *args):
        self.idx=args[0]
        self.i,self.j=args[1],args[2]
        self.Elist[self.idx].i=self.i     
        self.Elist[self.idx].j=self.j   
        #Move edge with idx args[0] to node args[1] to node args[2]
        
    def __movenode__(self, *args):
        (self.idx)=args[0]
        (self.i)=args[1]
        (self.j)=args[2]
        ((self.Nlist)[self.idx]).i=self.i
        #Move node with idx args[0] to position args[1],args[2]
                       
    def __moveparticle__(self, *args):
        (self.idx)=args[0]
        (self.i)=args[1]
        ((self.plist)[self.idx]).i=self.i
        #Move particle with idx args[0] to node args[1]
        
    def __changew__(self, *args):
        (self.idx)=args[0]
        (self.w)=args[1]
        ((self.Nlist)[self.idx]).w=self.w
        #Change variable associated with node
        
    def __deleteedge__(self, *args):
        (self.Elist[args[0]]).__delete__(self.Nlist,self.Elist) 
        #Delete edge with idx args[0]
            
    def __deletenode__(self, *args):
        (self.Nlist[args[0]]).__delete__(self.Nlist,self.Elist,self.plist) 
        #Delete node with idx args[0]
        
    def __deleteparticle__(self, *args):
        (self.plist[args[0]]).__delete__(self.Nlist,self.plist) 
        #Delete particle with idx args[0]

    def __activate__(self, *args):
        h=args[0]; #Number of hops
        for a in range(0,h):
            r=random.randint(0,self.p-1) #Random particle
            n=(self.Plist[r]).i #Node occupying        
            ne=len((self.Nlist[n]).iel) #Number of connected edges
            if ne>0: #if any
                r2=random.randint(0,ne-1) #Random number 0 to ne
                e=self.Elist[(self.Nlist[n]).iel[r2]] #corresponds to random connected edge
                nn=e.echeck(n); #Return index of next node at opposite end of edge
                if(self.Nlist[nn].ocheck()==False): #If node unnoccupied
                    self.Plist[r].__move__(self.Nlist,nn) #Move particle to next node
        
        matplotlib.pyplot.figure() #New figure
        matplotlib.pyplot.xlim([0,100])
        matplotlib.pyplot.ylim([0,100])

    def __plot__(self, Nlist, Elist, plist):
        matplotlib.pyplot.figure() #New figure
        matplotlib.pyplot.xlim([0,100])
        matplotlib.pyplot.ylim([0,100])
        n = len(Nlist)
        m = len(Elist)
        p = len(plist)
        for a in range(0,n-1):            
            matplotlib.pyplot.plot(self.Nlist[a].i,self.Nlist[a].j,'bo',markersize=20) #Plot edge 
        for a in range(0,m-1):  
            ln=self.Elist[a].i
            un=self.Elist[a].j
            matplotlib.pyplot.plot([self.Nlist[ln].i,self.Nlist[un].i],[self.Nlist[ln].j,self.Nlist[un].j],'r-') #Plot edge 
        for a in range(0,p-1):            
            matplotlib.pyplot.plot(self.Nlist[plist[a].i].i,self.Nlist[plist[a].i].j,'kx') #Plot edge 


class NetworkDesign:
    Nlist=[] #List of nodes
    Elist=[] #List of edges
    Plist=[] #List of particles   
    
    N=0 #Number of particles
    M=0 #Number of edges
    p=0 #Number of particles
    
    def __plot__(self, Nlist, Elist, plist):
        matplotlib.pyplot.figure() #New figure
        matplotlib.pyplot.xlim([0,100])
        matplotlib.pyplot.ylim([0,100])
        n = len(Nlist)
        m = len(Elist)
        p = len(plist)
        for a in range(0,n):            
            matplotlib.pyplot.plot(self.Nlist[a].i,self.Nlist[a].j,'bo',markersize=20) #Plot edge 
        for a in range(0,m):  
            ln=self.Elist[a].i
            un=self.Elist[a].j
            matplotlib.pyplot.plot([self.Nlist[ln].i,self.Nlist[un].i],[self.Nlist[ln].j,self.Nlist[un].j],'r-') #Plot edge 
        for a in range(0,p):            
            matplotlib.pyplot.plot(self.Nlist[plist[a].i].i,self.Nlist[plist[a].i].j,'kx') #Plot edge 
    
    def __addnode__(self, *args):
        (self.i)=args[0]
        (self.j)=args[1]
        (self.Nlist).append(Node2D(self.i,self.j,0,idx=self.N,conn=self.N+1))
        self.N=self.N+1

    def __addedge__(self, *args):
        self.a,self.b=args[0],args[1]
        L=len(self.Elist)
        (self.Elist).append(Edge2D(self.a,self.b,idx=L))
        ((self.Nlist[self.a]).iel).append(L) #Add edge to list within node
        ((self.Nlist[self.b]).iel).append(L) #Add edge to list within node
        self.M=L+1
        #Add edge with ends args[0] and args[1] and index = M-1
        #M is new number of edges
    
    def __deletenode__(self, *args):
        (self.Nlist[args[0]]).__delete__(self.Nlist,self.Elist,self.Plist)
        #self.N=self.N-1
        #Delete node with idx args[0]

    def __deleteedge__(self, *args):
        (self.Elist[args[0]]).__delete__(self.Nlist,self.Elist)
        #self.M=self.M-1
        #Delete edge with idx args[0]
        
    def __printn__(self):
        for a in range(0,self.N):
            print(self.Nlist[a])
            
    def __printe__(self):
        for a in range(0,self.M):
            print(self.Elist[a])

    def __str__(self):
        tp="" #String to print
        for a in range(0,self.N):
            tp+=self.Nlist[a].__str__()
            tp+="\n"
        for a in range(0,self.M):
            tp+=self.Elist[a].__str__()
            tp+="\n"
        return(tp)
    
    def __init__(self, *args, **kwargs):
        self.Nlist=[] #List of nodes
        self.Elist=[] #List of edges
        self.Plist=[] #List of particles
        self.__plot__(self.Nlist,self.Elist,self.Plist)
        run = True
        cmd=""
        i,j=0,0
        while(run==True):
            cmd=input("\nNext command: ")
            if cmd=="node":
                i=int(input("X Co-ordinate: "))
                j=int(input("Y Co-ordinate: "))
                self.__addnode__(i,j)
                self.__printn__()
            if cmd=="edge":
                i=int(input("Node 1: "))
                j=int(input("Node 2: "))
                self.__addedge__(i,j)
                self.__printe__()
            if cmd=="printn":
                self.__printn__()
            if cmd=="printe":
                self.__printe__()
            if cmd=="printN":
                print(self.__str__())               
            if cmd=="deleten":
                i=int(input("Node: "))
                self.__deletenode__(i)
            if cmd=="deletee":
                i=int(input("Edge: "))
                self.__deleteedge__(i)
            if cmd=="plot":
                self.__plot__(self.Nlist,self.Elist,self.Plist)
            if cmd=="end":
                break
        
        
        
###Clean Up Codes
###Add comments to codes
###TEST AND DEBUG

n=100 #20 nodes
m=60 #8 edges
p=10 #5 particles

print("NETWORK")
Np=NetworkPart(n,m,p) #Generate Network
Np.__activate__(20) #Activate 
Np.__plot__(Np.Nlist,Np.Elist,Np.Plist)
###Hop fails if node has no neighbours or jump is to occupied node
###Each hop is followed by a figure 


print("\n")
print("\nDesigned Network")
dN=NetworkDesign()
#dN.__plot__(dN.Nlist,dN.Elist,dN.Plist)

###TESTS