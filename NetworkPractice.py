# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

"""NETWORKS"""
import matplotlib
import random

###Network Type
###Number of networks

N = 10 #Define number of nodes in network
M = 5 #Number of edges in network

#Code for simple networks
###Create a class for nodes
class Node:
    ###DEFAULTS
    i,j,k = 0,0,0 #Give nodes 0 co-ordinates in x,y and z planes
    w = 0
    idx=-1 #Node Index = 1
    edge_max=0 #Maximum edges = 0
       
    def __init__(self, *args, **kwargs):
        self.i = args[0]
        self.j = args[1]
        self.k = args[2]
        self.w = args[3]
        
        if(kwargs.__contains__('idx')):
            self.idx=kwargs['idx']
        edge_max=kwargs['conn']
        print(self.i,self.j,self.k,self.w,self.idx,edge_max)
    #Give nodes adjoining edges (initialise)

    def __next__(self,Nlist):
        return Nlist[self.idx+1]       
    #Scroll through nodes
    
    def __str__(self):
        return 'Node of index {} at co-ord {},{},{}'.format(self.idx,self.i,self.j,self.k)

class Node1D:
    def __init__(self, *args, **kwargs):
        self.i = args[0]
        self.w = args[1]
        self.iel = [] #Internal edge list

        ###DEFAULTS
        self.idx=-1 #Node Index = -1
        self.edge_max=0 #Maximum edges = 0
        if(kwargs.__contains__('idx')):
            self.idx=kwargs['idx']
        if(kwargs.__contains__('conn')):
            self.edge_max=kwargs['conn']

    def __next__(self,Nlist):
        l=len(Nlist)
        return Nlist[(self.idx+1)%l]
    #Scroll through nodes

    def __delete__(self,Nlist,Elist):
        ne=len(self.iel) #Number of edges connected to node
        for a in range(ne): #For each related edge
            Elist[self.iel[ne-a-1]].__delete__(Nlist, Elist)
            #Delete Edges in reverse order in list
        Nlist[self.idx]=None #Delete node from list
        return None
    #Delete Node

    def __str__(self):
        return 'Node[{}] of index {} at co-ord {} - {}'.format(self.edge_max,self.idx,self.i,self.iel)

class Node2D:
    def __init__(self, *args, **kwargs):
        self.i = args[0]
        self.j = args[1]
        self.w = args[2]
        self.iel = [] #Internal edge list

        ###DEFAULTS
        self.idx=-1 #Node Index = -1
        self.edge_max=0 #Maximum edges = 0
        if(kwargs.__contains__('idx')):
            self.idx=kwargs['idx']
        if(kwargs.__contains__('conn')):
            self.edge_max=kwargs['conn']

    def __next__(self,Nlist):
        l=len(Nlist)
        return Nlist[(self.idx+1)%l]
    #Scroll through nodes

    def __delete__(self,Nlist,Elist):
        ne=len(self.iel) #Number of edges connected to node
        for a in range(len(self.iel)): #For each related edge
            Elist[self.iel[ne-a-1]].__delete__(Nlist, Elist)
            #Delete Edges in reverse order in list
        Nlist[self.idx]=None #Delete node from list
        return None
    #Delete Node

    def __str__(self):
        return 'Node[{}] of index {} at co-ord {},{} - {}'.format(self.edge_max,self.idx,self.i,self.j,self.iel)


#Create special node the inherits from node but with additional properties
class SNode:
    pass
    #def __init__(self, *args, **kwargs):
        #Node.__init__(self, *args, **kwargs)
        #rho = self.w*(1-self.w)

class Edge1D:
    i,j = 0,1 #Connects nodes 0 and 1
    idx=-1 #Edge Index = -1
    def __init__(self, *args, **kwargs):
        self.i = args[0]
        self.j = args[1]
        if(kwargs.__contains__('idx')):
            self.idx=kwargs['idx']

    def __next__(self,Elist):
        l=len(Elist)
        return Elist[(self.idx+1)%l]
    #Scroll through edges

    def __delete__(self,Nlist,Elist):
        (Nlist[self.i].iel).remove(self.idx)
        (Nlist[self.j].iel).remove(self.idx)
        Elist[self.idx]=None #Delete edge from list
        return None
    #Delete Edge

    def __str__(self):
        return 'Edge of index {} connecting nodes {} and {}'.format(self.idx,self.i,self.j)

class Edge2D:
    i,j = 0,1 #Connects nodes 0 and 1
    idx=-1 #Edge Index = -1
    def __init__(self, *args, **kwargs):
        self.i = args[0]
        self.j = args[1]
        if(kwargs.__contains__('idx')):
            self.idx=kwargs['idx']

    def __next__(self,Elist):
        l=len(Elist)
        return Elist[(self.idx+1)%l]
    #Scroll through edges

    def __delete__(self,Nlist,Elist):
        (Nlist[self.i].iel).remove(self.idx)
        (Nlist[self.j].iel).remove(self.idx)
        Elist[self.idx]=None #Delete edge from list
        return None
    #Delete Edge

    def __str__(self):
        return 'Edge of index {} connecting nodes {} and {}'.format(self.idx,self.i,self.j)

class NetworkSimp:
    #Simple network where nodes are in a circle and connected to neighbours 
    
    N = 0 #0 Nodes or Edges in network 
    def __init__(self, *args, **kwargs):
        self.N = args[0]
        self.Nlist=[] #List of nodes
        self.Elist=[] #List of edges
        for a in range(self.N):
            (self.Nlist).append(Node1D(a,0,idx=a,conn=2)) #Add each node to list
            print((self.Nlist[a]).__str__()) #Print node
            matplotlib.pyplot.plot(a,pow(a,2),'kx') #Plot node
        matplotlib.pyplot.show
        print("\n")
        for a in range(self.N):
            print("\n")
            b=(a+1)%self.N #Neighbouring node
            (self.Elist).append(Edge1D(a,b,idx=a)) #Add edge to list
            print((self.Elist[a]).__str__()) #Print edge
            ((self.Nlist[a]).iel).append(a) #Add edge list within node
            ((self.Nlist[b]).iel).append(a) #and other node           
            print((self.Nlist[a]).iel) #Print internal lists
            print((self.Nlist[b]).iel)
            matplotlib.pyplot.plot([a,b],[pow(a,2),pow(b,2)],'r-') #Plot edge 
    
    def __deleteedge__(self, *args):
        (self.Elist[args[0]]).__delete__(self.Nlist,self.Elist) 
        #Delete edge with idx args[0]
        
    def __deletenode__(self, *args):
        (self.Nlist[args[0]]).__delete__(self.Nlist,self.Elist) 
        #Delete node with idx args[0]
               
    ###Add Node
    ##Change node property (w)

class NetworkCircR:
    #Network where nodes are in a circle and connected to random others
    
    N = 0 #0 Nodes or Edges in network
    def __init__(self, *args, **kwargs):
        self.N = args[0]
        self.M = args[1]
        self.Nlist=[] #List of nodes
        self.Elist=[] #List of edges
        matplotlib.pyplot.figure() #New figure
        matplotlib.pyplot.xlim([0,20])
        matplotlib.pyplot.ylim([0,400])
        for a in range(self.N): #Nodes
            self.i=round(random.random()*20,2)
            (self.Nlist).append(Node1D(self.i,0,idx=a,conn=self.N)) #Add each node to list
            print((self.Nlist[a]).__str__()) #Print node
            matplotlib.pyplot.plot(self.i,pow(self.i,2),'kx') #Plot node
        matplotlib.pyplot.show
        print("\n")
        for a in range(self.M): #Edges
            print("\n")
            l=random.randint(0,self.N-1) #Random node
            r=random.randint(0,self.N-1) #Random node
            (self.Elist).append(Edge1D(self.Nlist[l],self.Nlist[r],idx=a)) #Add edge to list
            print((self.Elist[a]).__str__()) #Print edge
            ((self.Nlist[l]).iel).append(a) #Add edge list within node
            ((self.Nlist[r]).iel).append(a) #and other node           
            print((self.Nlist[l]).iel) #Print internal lists
            print((self.Nlist[r]).iel)
            matplotlib.pyplot.plot([self.Nlist[l].i,self.Nlist[r].i],[pow(self.Nlist[l].i,2),pow(self.Nlist[r].i,2)],'r-') #Plot edge 
        matplotlib.pyplot.show

    def __addedge__(self, *args):
        self.a,self.b=args[0],args[1]
        L=len(self.Elist)
        (self.Elist).append(Edge1D(self.a,self.b,idx=L))
        self.M=L+1
        #Add edge with ends args[0] and args[1] and index = M-1
        #M is new number of edges

    def __addnode__(self, *args):
        (self.i)=args[0]
        (self.Nlist).append(Node1D(self.i,0,idx=self.N,conn=self.N+1))
        self.N=self.N+1
        
    def __moveedge__(self, *args):
        self.idx=args[0]
        self.i,self.j=args[1],args[2]
        self.Elist[self.idx].i=self.i     
        self.Elist[self.idx].j=self.j   
        
    def __movenode__(self, *args):
        (self.idx)=args[0]
        (self.i)=args[1]
        ((self.Nlist)[self.idx]).i=self.i
                        
    ##Change node property (w)
        
class Network2D:
    #2D Network where nodes are randomnly connected
    
    N = 0 #0 Nodes or Edges in network
    def __init__(self, *args, **kwargs):
        self.N = args[0]
        self.M = args[1]
        self.Nlist=[] #List of nodes
        self.Elist=[] #List of edges
        matplotlib.pyplot.figure() #New figure
        matplotlib.pyplot.xlim([0,100])
        matplotlib.pyplot.ylim([0,100])
        for a in range(self.N): #Nodes
            self.i=round(random.random()*100,2)
            self.j=round(random.random()*100,2)
            (self.Nlist).append(Node2D(self.i,self.j,0,idx=a,conn=self.N)) #Add each node to list
            print((self.Nlist[a]).__str__()) #Print node
            matplotlib.pyplot.plot(self.i,self.j,'kx') #Plot node
        matplotlib.pyplot.show
        print("\n")
        for a in range(self.M): #Edges
            print("\n")
            l=random.randint(0,self.N-1) #Random node
            r=random.randint(0,self.N-1) #Random node
            (self.Elist).append(Edge2D(self.Nlist[l],self.Nlist[r],idx=a)) #Add edge to list
            print((self.Elist[a]).__str__()) #Print edge
            ((self.Nlist[l]).iel).append(a) #Add edge to list within node
            ((self.Nlist[r]).iel).append(a) #and other node           
            print((self.Nlist[l]).iel) #Print internal lists
            print((self.Nlist[r]).iel)
            matplotlib.pyplot.plot([self.Nlist[l].i,self.Nlist[r].i],[self.Nlist[l].j,self.Nlist[r].j],'r-') #Plot edge 
        matplotlib.pyplot.show

    def __addedge__(self, *args):
        self.a,self.b=args[0],args[1]
        L=len(self.Elist)
        (self.Elist).append(Edge1D(self.a,self.b,idx=L))
        self.M=L+1
        #Add edge with ends args[0] and args[1] and index = M-1
        #M is new number of edges

    def __addnode__(self, *args):
        (self.i)=args[0]
        (self.Nlist).append(Node1D(self.i,0,idx=self.N,conn=self.N+1))
        self.N=self.N+1
        
    def __moveedge__(self, *args):
        self.idx=args[0]
        self.i,self.j=args[1],args[2]
        self.Elist[self.idx].i=self.i     
        self.Elist[self.idx].j=self.j   
        
    def __movenode__(self, *args):
        (self.idx)=args[0]
        (self.i)=args[1]
        ((self.Nlist)[self.idx]).i=self.i
                        
    ##Change node property (w)
#Create three types of network:
    #Simple where nodes are in a circle and connected to neighbours 
    #Circle where nodes are in a circle and edges are random
    #2-D random where nodes positions are random and edges are random
    
#Create a network app

n=8 #8 nodes
print("NETWORK")
Ns=NetworkSimp(n) #Generate Network

###Tests
print("\n")
print("TESTS")
print((Ns.Nlist[6]).__str__())  #Print a node
print((Ns.Nlist[6]).__next__(Ns.Nlist)) #Iterate and print

print((Ns.Elist[1]).__str__())  #Print an edge
nb=(Ns.Elist[1]).__next__(Ns.Elist) #Iterate
print(nb)
nb=nb.__next__(Ns.Elist) #Iterate again
print(nb) 

le=(Ns.Nlist[7]).iel[0] #Lower edge
print("Edge ",le)
de=((Ns.Elist[le]).__next__(Ns.Elist)).idx #Iterate edge
print("Edge ",de)
de=((Ns.Elist[de]).__next__(Ns.Elist)).idx #Iterate edge
print("Edge ",de)
print("Lower node",Ns.Elist[de].i) #Lower node

print("\n")
print((Ns.Elist[0]).__str__())
Ns.__deleteedge__(0)
print((Ns.Elist[0]).__str__())

print((Ns.Elist[1]).__str__())
Ns.__deleteedge__(1)
print((Ns.Elist[1]).__str__())

print((Ns.Nlist[1]).__str__())
#Delete Edge

print("\n")
print((Ns.Nlist[2]).__str__())
Ns.__deletenode__(2)
print((Ns.Nlist[2]).__str__())

print((Ns.Nlist[5]).__str__())
Ns.__deletenode__(5)
print((Ns.Nlist[5]).__str__())
#Delete node


#n=8 #8 nodes
#m=3 #5 edges
#print("\n\n\n\nNETWORK - RANDOM")
#Nr=NetworkCircR(n,m) #Generate Network

###Tests
#print("\n")
#print("TESTS")
#print((Nr.Nlist[6]).__str__())  #Print a node
#print((Nr.Nlist[6]).__next__(Ns.Nlist)) #Iterate

#print((Nr.Elist[1]).__str__())  #Print an edge
#nb=(Nr.Elist[1]).__next__(Nr.Elist) #Iterate
#print(nb)
#nb=nb.__next__(Nr.Elist)
#print(nb) 


#n=100 #8 nodes
#m=24 #3 edges
#print("\n\n\n\n2D RANDOM NETWORK")
#N2D=Network2D(n,m) #Generate Network

#le=(Ns.Nlist[7]).iel[0] #Lower edge
#print("Edge ",le)
#de=((Ns.Elist[le]).__next__(Ns.Elist)).idx #Iterate edge
#print("Edge ",de)
#de=((Ns.Elist[de]).__next__(Ns.Elist)).idx #Iterate edge
#print("Edge ",de)
#print("Lower node",Ns.Elist[de].i) #Lower node

###
#Test add and move edge, add and move node

#######################################
#matplotlib.pyplot.figure(2)
#Nlist=[] #List of nodes
#Elist=[] #List of edges
#for a in range(N):
#    Nlist.append(Node1D(a,0,idx=a,conn=N-1))
#    print(Nlist[a].__str__())
#    matplotlib.pyplot.plot(a,pow(a,2),'kx')
#matplotlib.pyplot.show
#print("\n")
#for a in range(M):
#    b=(a+1)%N
#    Elist.append(Edge1D(a,b))
#    print(Elist[a].__str__())
#    matplotlib.pyplot.plot([a,b],[pow(a,2),pow(b,2)],'r-')

#Node 1 then 0 then 4 (Randomnly chosen)
#print("\n")
#print(Nlist[1].__str__())
#nb=Nlist[1].__next__(Nlist); #Neighbour
#print(nb.__str__())

#print(Nlist[0].__str__())
#nb=Nlist[0].__next__(Nlist); #Neighbour
#print(nb.__str__())

#print(Nlist[4].__str__())
#nb=Nlist[4].__next__(Nlist); #Neighbour
#print(nb.__str__())

#Nlist.append(SNode(1,2,3,0,idx=5,conn=N-1))