#TurtleDefense 
#Python trial 
import enum
import random 
import simpy
import matplotlib.pyplot as plt
beta1 =.5
beta2 =.5
delta1 = .5
delta2 = .5
#maybe add list of all nodes to have each node on creation pick neighbors from
#what to do with C1 == C2
count = 0 #count of all nodes
allNodes = [] #list of  all nodes
tot_inf1 = 0 #total number of infections by meme 1
tot_inf2 = 0 #total number of infections by meme 2
total_M1 = 0#total number of nodes in state I1 (for end)
total_M2 = 0#total number of nodes in state I2 (for end)
total_S = 0 #total number of nodes in state S 
class State(enum.Enum):
    S = 0
    I1 = 1
    I2 = 2
   

class Node:
    state = State.S
    neighbors = []
    def _str_(self):
        return str(name)
    def _init_(self):
        self.state = State.S #State of node
        self.neighbors = [] #List of neighbors of node
        allNodes.append(self)
    def addNeighbors(self):#method to add neighbors to node
        if allNodes: #if this not the first node add random number of neighbors from list of all nodes 
            self.neighbors.append(random.sample(allNodes,random.randint(1,int(len(allNodes)/2)+1)))
    def isInf(self):#helper method to determine if node is infected
        if self.State == State.S:
            return False
        else:
            return True
    def attack(self):#Method to see if the node becomes infected, assuming if C1 == C2 then not infected by either   
       #print("Attack Happening")
       if self.isInf:
            return
       C1=0
       C2=0
       for neigh in neighbors:
           if neigh.state == I1 and random.random()<beta1:
               C1 = C1 + 1
           if neigh.state == I2 and random.random()<beta2:
               C2 = C2 + 1
       if C1 > C2:
            self.state = State.I1
            print("Infection by Meme 1")
            tot_inf1 = tot_inf1 + 1
       elif C2 > C1:
           self.state = State.I2
           print("Infection by Meme 2")
           tot_inf2 = tot_inf2 + 1
    def recover(self): #Method to see if node recovers assuming node cannot be infected by the other meme
        if self.state == State.I1 and random.random()<delta1:
            self.state = State.S
        if self.state == State.I2 and random.random()<delta2:
            self.state = State.S

test = Node()
for i in range(0,100): #fill list of nodes
    node = Node()
    node.addNeighbors()
    allNodes.append(node)
#for i in range(0,len(allNodes)):
#    print(allNodes[i].state)

infected = random.sample(allNodes,random.randint(1,len(allNodes)))#randomly choose how many nodes start infected with no more than half being infected

for i in range(0,len(infected)):
    infected[i].state = State.I1
 

##infected2 = random.sample(infected,random.randint(1,int(len(infected)/2)))#randomly choose how many nodes start infected  by meme 2 
infected2 = random.sample(infected,int(len(infected)/2)) #eqaul number of starting I2 and I1
for i in range(0,len(infected2)):
    infected2[i].state = State.I2
#print("Infected:")
#for i in range(0,len(infected)):
#    print(infected[i].state)

print(len(allNodes[0].neighbors))
print(len(allNodes[int(len(allNodes)/2)].neighbors))
print(len(allNodes[len(allNodes)-1].neighbors))
for t in range(0,1000):
    for i in range(0,len(allNodes)):
        allNodes[i].recover()
        allNodes[i].attack()

print("Total Infections by Meme 1:")
print(tot_inf1)
print("Total Infections by Meme 2:")
print(tot_inf2)
fig =plt.figure()

#plt.bar('Meme1',tot_inf1,color="red", width = 1)
#plt.bar('Meme2',tot_inf2,color="blue", width = 1)
#plt.xlabel("Meme")
#plt.ylabel("No. Total infections")
#plt.title("Total infections by meme")
#plt.show()
