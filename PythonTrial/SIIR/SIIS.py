#TurtleDefense    
#SIIR Model through python
#last updated 3/15/22 
#Created the two edge sets
####check math/stat keeping!!!!!!
import enum
import random 
import simpy
#import matlab.engine
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as linalg
from collections import Counter
take_sample  = False #If false one run last run printed 
smp_size = 50 # sample size
#count = 0       # used to hold value of how many times out come matches
theta = .10     #
N = 75       # N number of nodes
tm = 1000       # time of simulation
beta1 =.678
beta2 =.427
delta1 = .50
delta2 = .50
#maybe add list of all nodes to have each node on creation pick neighbors from
#what to do with C1 == C2
allNodes = [] #list of  all nodes
tot_inf1 = 0 #total number of infections by meme 1
tot_inf2 = 0 #total number of infections by meme 2
total_M1 = 0 #total number of nodes in state I1 (for plot)
total_M2 = 0 #total number of nodes in state I2 (for plot)
total_S = 0  #total number of nodes in state S 
#Classes and Function Definition
class State(enum.Enum):
    S = 0
    I1 = 1
    I2 = 2
   

#picks a random node        
def randomRem():
        nodea = random.choice(allNodes)
        removeNode(nodea)

#picks a random neighbor of a random node
def randomNeigh():
         nodea = random.choice(allNodes)
         pick = random.randint(0, 1)
         temp = nodea
         if pick == 1:
            temp =  random.choice(nodea.e1_Neighbors)
         if pick == 0:
            temp =  random.choice(nodea.e2_Neighbors)
         
         removeNode(temp)          
        
#removes the node being passed
def removeNode(nodea):
        
        #print("test: ", len(nodea.e1_Neighbors))
        allNodes.remove(nodea)
        
        for i in range(len(allNodes)): 
        #check if the removed node is a neighbor for all the nodes in the list
        #remove it, if so
            if(nodea in allNodes[i].e1_Neighbors):    
                #print("found at node ", i)
                #print("test before : ", len(allNodes[i].e1_Neighbors))
                allNodes[i].e1_Neighbors.remove(nodea)
                #print("test after : ", len(allNodes[i].e1_Neighbors))
            if(nodea in allNodes[i].e2_Neighbors):
                allNodes[i].e2_Neighbors.remove(nodea) 

#Node Object
class Node:
    count = 0
    def __init__(self):
        self.id = Node.count
        Node.count+=1
        self.e1_Neighbors = []#List of neighbors of node in edge 1
        self.e2_Neighbors = []#List of neighbors of node in edge 2
        self.state = State.S #State of nodes
        allNodes.append(self)
    #Neighbors not always neighbor 
    def addNeighbors(self):#method to add neighbors to node, call after Adj matrix mad
    ####WARNING: Make sure to sort Nodes before using#####
     for x in range(0,N):
         if A1[self.id][x] == 1:
            self.e1_Neighbors.append(allNodes[x])
            allNodes[x].e1_Neighbors.append(allNodes[self.id])
     for x in range(0,N):
        if A2[self.id][x] == 1:
            self.e2_Neighbors.append(allNodes[x])
            allNodes[x].e2_Neighbors.append(allNodes[self.id])

    def attack(self):#Method to see if the node becomes infected, assuming if C1 == C2 then not infected by either   
       if self.state != State.S:
            return
       global tot_inf1 #total of infections made by nodes infected with meme 1
       global tot_inf2 #total of infections made by nodes infected with meme 2
       global total_M1 #current # of nodes infected with meme 1
       global total_M2 #current # of nodes infected with meme 1
       C1=0
       C2=0
       for i in self.e1_Neighbors:# attacks from meme 1 that can only spread on edge 1
           if i.state == State.I1 and random.random()<beta1:
               C1 = C1 + 1
       for i in self.e2_Neighbors:# attacks from meme 1 that can only spread on edge 2
           if i.state == State.I2 and random.random()<beta2:
               C2 = C2 + 1
       if C1 > C2:
            self.state = State.I1
            tot_inf1 = tot_inf1 + 1
            total_M1 += 1
            infected_meme1.append(i)
       elif C2 > C1:
           self.state = State.I2
           tot_inf2 = tot_inf2 + 1
           total_M2 += 1
           infected_meme2.append(i)
    def recover(self): #Method to see if node recovers assuming node cannot be infected by the other meme
        global total_M1 #current # of nodes infected with meme 1
        global total_M2 #current # of nodes infected with meme 1
        if self.state == State.S:
            return
        if self.state == State.I1 and random.random()<delta1:
            #print("Infected with I1")
            self.state = State.S
            total_M1 =  total_M1 - 1
            
        if self.state == State.I2 and random.random()<delta2:
            #print("Infected with I2")
            self.state = State.S
            total_M2 =  total_M2 - 1

##sets up infected lists for infection
def set_simulation():
    global infected_meme1,infected_meme2,tot_inf1,tot_inf2
    infected_meme1 = original_inf_meme1
    infected_meme2 = original_inf_meme2
    tot_inf1 = 0
    tot_inf2 = 0
    global time,time_inf1,time_inf2 
    time = []#time for x axis
    time_inf1 = []#array of  number of infected with meme 1, to plot
    time_inf2 = []#array of  number of infected with meme 1, to plot
    #print("Len of infected:",len(infected_meme1))
    total_M1 = len(infected_meme1)
    for i in range(0,len(infected_meme1)):
        infected_meme1[i].state = State.I1
    
 

    for i in range(0,len(infected_meme2)):
        #infected_meme1.remove(infected_meme2[i])
        infected_meme2[i].state = State.I2

    total_M2 = len(infected_meme2)
   # print("Len of infected_meme2:",len(infected_meme2))

###SETUP#################################################################################################################################################################################################


#create adjacency matrix
A1 = np.random.randint(2,size = (N,N),dtype=np.int8)#adjacency matrix for edge 1, filled with random 0s and 1s
np.fill_diagonal(A1,0)#make A1 diagonal 0's
A2 = np.random.randint(2,size = (N,N),dtype=np.int8)#adjacency matrix for edge 2, filled with random 0s and 1s 
np.fill_diagonal(A2,0)#make A2 diagonal 0's

##create System Matrices
S1 = (1- delta1)* np.identity(N,dtype = np.int8) + beta1 * A1
S2 = (1- delta2)* np.identity(N,dtype = np.int8) + beta2 * A2
##get Eigen Values
eigenValues1,eigenVectors1 = linalg.eig(S1)
eigenValues2,eigenVectors2 = linalg.eig(S2)
##sort eigen values
#idx = eigenValues1.argsort()[::-1]
#eigenValues1 = eigenValues1[idx]
#eigenVectors1 = eigenVectors1[:,idx]

#idx = eigenValues2.argsort()[::-1]
#eigenValues2 = eigenValues2[idx]
#eigenVectors2 = eigenVectors2[:,idx]

eigenValuesReal1 = [0]*N
eigenValuesReal2 = [0]*N

for i in range (0,N):
    eigenValuesReal1[i] = round(np.real(abs(eigenValues1[i])),4)
    eigenValuesReal2[i] = round(np.real(abs(eigenValues2[i])),4)

eigenValueMaxDegreeValue1 = Counter(eigenValuesReal1)
eigenValueMaxDegreeValue2 = Counter(eigenValuesReal2)

##Print eigen Values
#print("Eigen Value of S1", eigenValues1[0])
#print("Eigen Value of S2", eigenValues2[0])

print("Eigenvalue1", eigenValueMaxDegreeValue1.most_common(1))
print("Eigenvalue2", eigenValueMaxDegreeValue2.most_common(1))

#Create Nodes
for i in range(0,N): #fill list of nodes
    node = Node()
##sort nodes by ID number
allNodes.sort(key= lambda x: x.id, reverse = False)
#add neighbors to nodes from adjacency matrices
for i in allNodes: 
    i.addNeighbors()


##create first list of infected nodes
#holds org sets to use for multiple lists
original_inf_meme1 = random.sample(allNodes,random.randint(1,len(allNodes)))#randomly choose how many nodes start infected with no more than half being infected
original_inf_meme2 = random.sample(original_inf_meme1,random.randint(1,int(len(original_inf_meme1))))#randomly choose how many nodes start infected  by meme 2 
set_simulation()

#method for removing random node
#randomRem()
#method for removing random neigbor        
randomNeigh()





M1_Wins = 0 #number of samples that M1 wins
M2_Wins = 0 #number of samples M2 Wins
No_win = 0  #number of samples with no clear winner 

########################MAIN LOOP################################################################################################################################################################################
if take_sample == True:
    for i in  range(0,smp_size):
        set_simulation()
        if i % 10 == 0:
                print("Sample:",i)
        for t in range(0,tm):
            time.append(t)### add time to array to use for plot
    
            for i in allNodes:
                if i.state == State.S: ##check for state therefore cutting down on how many runs of each method happen
                    i.attack()
                else:
                    i.recover()
            time_inf1.append(total_M1)
            time_inf2.append(total_M2)
        if total_M1 > total_M2 and ((total_M1-total_M2)/N) > theta: 
            M1_Wins+= 1
        elif total_M2 > total_M1 and ((total_M2-total_M1)/N) > theta: 
            M2_Wins+= 1
        else:
            No_win += 1
else:
    for t in range(0,tm):
        time.append(t)### add time to array to use for plot
        if t % 100 == 0:
               print("Time:",t)
    
        for i in allNodes:
            if i.state == State.S: ##check for state therefore cutting down on how many runs of each method happen
                i.attack()
            else:
                i.recover()
        time_inf1.append(total_M1)
        time_inf2.append(total_M2)


#################################################################################################################################################################################################
print("Number of Meme 1 wins:")
print(M1_Wins)
print("Number of Meme 2 wins:")
print(M2_Wins)
print("Number of  no clear winner:")
print(No_win)




#Showing Plots for one run
print("Total Infections by Meme 1:")
print(tot_inf1)

print("Total Infections by Meme 2:")
print(tot_inf2)
fig =plt.figure()
if take_sample == False:
   

    plt.bar('Meme1',tot_inf1,color="red", width = 1)
    plt.bar('Meme2',tot_inf2,color="blue", width = 1)
    plt.xlabel("Meme")
    plt.ylabel("No. Total infections")
    plt.title("Total infections by meme")
    plt.show()

    plt.plot(time,time_inf1,color="red", label ="Meme 1")
    plt.plot(time,time_inf2,color="blue", label ="Meme 2")
    plt.xlabel("Time,t")
    plt.ylabel("No. Total infections")
    plt.title("Total infections by meme")
    plt.show()
