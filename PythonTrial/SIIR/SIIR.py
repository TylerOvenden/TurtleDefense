#TurtleDefense 
#Python
#In this simulation we assume adj matrix is matrix of all nodes infected with that meme, so it does
#not include nodes in state S or the other plane
#need a way to update adjacency matrix
###add and remove node number adj
###make infected list global and update as infections happen
####check math/stat keeping!!!!!!
import enum
import random 
import simpy
import matlab.engine
import matplotlib.pyplot as plt
import numpy as np
beta1 =.5
beta2 =.5
delta1 = .1
delta2 = .1
#maybe add list of all nodes to have each node on creation pick neighbors from
#what to do with C1 == C2
allNodes = [] #list of  all nodes
tot_inf1 = 0 #total number of infections by meme 1
tot_inf2 = 0 #total number of infections by meme 2
total_M1 = 0#total number of nodes in state I1 (for plot)
total_M2 = 0#total number of nodes in state I2 (for plot)
total_S = 0 #total number of nodes in state S 

class State(enum.Enum):
    S = 0
    I1 = 1
    I2 = 2
   

class Node:
    count = 0
    def __init__(self):
        self.id = Node.count
        Node.count+=1
        self.neighbors = []#List of neighbors of node
        self.neighborsID = []#list of neighbors of node IDs
        self.state = State.S #State of nodes
        allNodes.append(self)
    def addNeighbors(self):#method to add neighbors to node
        if allNodes: #if this not the first node add random number of neighbors from list of all nodes 
           self.neighbors = random.sample(allNodes,random.randint(1,int(len(allNodes)/2)+1))
           for node in self.neighbors:
               self.neighborsID.append(node.id)
    def attack(self):#Method to see if the node becomes infected, assuming if C1 == C2 then not infected by either   
       if self.state != State.S:
            return
       global tot_inf1 #total of infections made by nodes infected with meme 1
       global tot_inf2 #total of infections made by nodes infected with meme 2
       global total_M1 #current # of nodes infected with meme 1
       global total_M2 #current # of nodes infected with meme 1
       C1=0
       C2=0
       for i in self.neighbors:
           if i.state == State.I1 and random.random()<beta1:
               C1 = C1 + 1
           if i.state == State.I2 and random.random()<beta2:
               C2 = C2 + 1
       if C1 > C2:
            self.state = State.I1
            tot_inf1 = tot_inf1 + 1
            total_M1 += 1
       elif C2 > C1:
           self.state = State.I2
           tot_inf2 = tot_inf2 + 1
           total_M2 += 1
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
def updateAdj():#current way to update adjaceny matrix after every t, therer may be a better way to do this
    ##create list of node numbers for each nodes neighbors
    ##for node in matrix check if node number is "in" the array
    ##maybe add row/col        to hold ids
    ##if so set to 1
    i =0
    for node in infected:
        A1[i][0] = node.id
        A1[0][i] = node.id
        i+=1
    i=0
    for node in infected2:
        A2[i][0] = node.id
        A2[0][i] = node.id
        i+=1
        





#Create Nodes
for i in range(0,1000): #fill list of nodes
    node = Node()
    node.addNeighbors()


infected = random.sample(allNodes,random.randint(1,len(allNodes)))#randomly choose how many nodes start infected with no more than half being infected
print("Len of infected:",len(infected))
total_M1 += len(infected)
for i in range(0,len(infected)):
    infected[i].state = State.I1
    
 

##infected2 = random.sample(infected,random.randint(1,int(len(infected)/2)))#randomly choose how many nodes start infected  by meme 2 
infected2 = random.sample(infected,int(len(infected)/2)) #eqaul number of starting I2 and I1
for i in range(0,len(infected2)):
    infected[i].state = State.I2

total_M2 += len(infected2)
print("Len of infected2:",len(infected2))



A1 = np.zeros([total_M1+1,total_M1+1])#adjacency matrix for meme1 with the 0 row and 0 column have ids of infected nodes
A2 = np.zeros([total_M2+1,total_M2+1])#adjacency matrix for meme1 with the 0 row and 0 column have ids of infected nodes 
time_inf1 = []#array of  number of infected with meme 1, to plot
time_inf2 = []#array of  number of infected with meme 1, to plot
time = []#time for x axis

########################MAIN LOOP################################################################################################################################################################################
for t in range(0,1000):
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
  

#test for push  
#################################################################################################################################################################################################
#Showing Plots
print("Total Infections by Meme 1:")
print(tot_inf1)

print("Total Infections by Meme 2:")
print(tot_inf2)

fig =plt.figure()

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
