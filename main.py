
"""@package SIIS
Python Simulation of the SIIS Model from 
‘Competing Memes Propagation on Networks: A Network Science Perspective’ 
Use random number generation 
@author Robert Bacigalupo
@author Tyler Ovendan
@author Auerman Atif 
@version 3.0
@date MAY 2022
"""
###\cite X. Wei, N. C. Valler, B. A. Prakash, I. Neamtiu, M. Faloutsos, and C. Faloutsos, “Competing memes propagation on networks: A network science perspective,” IEEE Journal on Selected Areas in Communications, vol. 31, no. 6, pp. 1049–1060, 2013. 
"""Imports"""
import enum
import random
import simpy
# import matlab.engine
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as linalg
from collections import Counter

"""
Simulation Description Variables
"""
##@var N
# Number of nodes
N = 200
##@var tm
# Discrete time units
tm = 1000
"""
Sampling Variables
"""
##@var take_Sample
# Enables Sampling 0 - Single Run, 1 - Same Matrix multiple runs , 2 - Different Matrix each run/holds eigen values
take_sample = 0
##@var smp_size
# sample size
smp_size = 10

""" Meme Parameters"""
##@var theta
# Margin off error to see if a Meme won in sampling, if less than theta no clear winner
theta = .10

beta1 = .005
beta2 = .005
delta1 = .2
delta2 = .2

M1_Wins = 0  # number of samples that M1 wins
M2_Wins = 0  # number of samples M2 Wins
No_win = 0  # number of samples with no clear winner
allNodes = []  # list of  all nodes
tot_inf1 = 0  # total number of infections by meme 1
old_inf1 = 0  # total number of infections by meme 1 for plotting
old_inf2 = 0  # total number of infections by meme 2 for plotting
tot_inf2 = 0  # total number of infections by meme 2
total_M1 = 0  # total number of nodes in state I1 (for plot)
total_M2 = 0  # total number of nodes in state I2 (for plot)
total_S = 0  # total number of nodes in state S

"""
States for each Meme (Susceptible, Infected with Meme 1, Infected with Meme 2)
"""
##@class State
# Enumeration for States
class State(enum.Enum):
    S = 0
    I1 = 1
    I2 = 2


"""
List of Suppression Methods
"""

################################################################################################################################################################################################################################################################################################################################################################
# SUPPRESSION METHODS
################################################################################################################################################################################################################################################################################################################################################################

""" 
Remove a Random Node
"""
##randomRem
# picks a random node
def randomRem():
    nodea = random.choice(allNodes)
    removeNode(nodea)

""" 
Remove a Random Neighbor of a Node
"""
##randomNeigh
# @param pick What edge to delete node from
# picks a random neighbor of a random node
def randomNeigh(pick):
    nodea = random.choice(allNodes)
    # pick = random.randint(0, 2)
    temp = nodea
    if pick == 1:
        temp = random.choice(nodea.e1_Neighbors)
    if pick == 0:
        temp = random.choice(nodea.e2_Neighbors)

    removeNode(temp)

""" 
Remove the Node With the Largest Degree
"""
##max_degree
# @param edge What edge to delete node from
# removes node max degree or most connections
def max_degree(edge):
    if edge == 1:
        tmp = A1.sum(axis=1)
        i = np.max(tmp)
        removeNode(allNodes[i])
    else:
        tmp = A2.sum(axis=1)
        i = np.max(tmp)
        removeNode(allNodes[i])

""" 
Method to Remove a Node from the Network
"""
##removeNode
# @param nodea The node to be deleted
# removes the node being passed
def removeNode(nodea):
    allNodes.remove(nodea)

    for i in range(len(allNodes)):
        ##check if the removed node is a neighbor for all the nodes in the list
        # remove it, if so
        if (nodea in allNodes[i].e1_Neighbors):
            allNodes[i].e1_Neighbors.remove(nodea)

        if (nodea in allNodes[i].e2_Neighbors):
            allNodes[i].e2_Neighbors.remove(nodea)

        ##@class Node


# @brief Class to implement node object
# each node object has unique id, list of its neighbors on each edge, and its state
#
class Node:
    ##@var count
    # class variable
    # count of total amount of nodes created, used to create unique Node ids
    count = 0

    ##_init_
    # @param self The object pointer
    # increases count after giving Node id
    def __init__(self):
        self.id = Node.count
        Node.count += 1
        self.e1_Neighbors = []  # List of neighbors of node in edge 1
        self.e2_Neighbors = []  # List of neighbors of node in edge 2
        self.state = State.S  # State of nodes
        allNodes.append(self)

    # Neighbors not always neighbor
    def addNeighbors(self):  # method to add neighbors to node, call after Adj matrix made
        ##WARNING: Make sure to sort Nodes before using#####
        for x in range(0, N):
            if A1[self.id][x] == 1:
                self.e1_Neighbors.append(allNodes[x])
            # allNodes[x].e1_Neighbors.append(allNodes[self.id])
        for x in range(0, N):
            if A2[self.id][x] == 1:
                self.e2_Neighbors.append(allNodes[x])
            # allNodes[x].e2_Neighbors.append(allNodes[self.id])

    def attack(self):  # Method to see if the node becomes infected, assuming if C1 == C2 then not infected by either
        if self.state != State.S:
            return
        global tot_inf1  # total of infections made by nodes infected with meme 1
        global tot_inf2  # total of infections made by nodes infected with meme 2
        C1 = 0
        C2 = 0
        for i in self.e1_Neighbors:  # attacks from meme 1 that can only spread on edge 1
            if i.state == State.I1 and random.random() < beta1:
                C1 = C1 + 1
        for i in self.e2_Neighbors:  # attacks from meme 1 that can only spread on edge 2
            if i.state == State.I2 and random.random() < beta2:
                C2 = C2 + 1
        if C1 > C2:
            self.state = State.I1
            tot_inf1 = tot_inf1 + 1
            infected_meme1.append(self)
        elif C2 > C1:
            self.state = State.I2
            tot_inf2 = tot_inf2 + 1
            infected_meme2.append(self)

    def recover(self):  # Method to see if node recovers assuming node cannot be infected by the other meme
        if self.state == State.S:
            return
        if self.state == State.I1 and random.random() < delta1:
            # print("Infected with I1")
            self.state = State.S
            if self in infected_meme1:
                infected_meme1.remove(self)

        if self.state == State.I2 and random.random() < delta2:
            # print("Infected with I2")
            self.state = State.S
            if self in infected_meme2:
                infected_meme2.remove(self)


################################################################################################################################################################################################################################################################################################################################################################
# Sim Methods
################################################################################################################################################################################################################################################################################################################################################################
##sets up infected lists for infection
def set_simulation():
    global infected_meme1, infected_meme2, tot_inf1, tot_inf2
    for i in allNodes:
        i.state = State.S
    tot_inf1 = 0
    tot_inf2 = 0
    global time, time_inf1, time_inf2
    time = []  # time for x axis
    time_inf1 = []  # array of  number of infected with meme 1, to plot
    time_inf2 = []  # array of  number of infected with meme 1, to plot
    # print("Len of infected:",len(infected_meme1))

    for i in range(0, len(infected_meme1)):
        infected_meme1[i].state = State.I1

    remove = []

    for i in range(0, len(infected_meme2)):
        if infected_meme2[i].state != State.I1:
            infected_meme2[i].state = State.I2
        else:
            remove.append(infected_meme2[i])
    for i in remove:
        infected_meme2.remove(i)
    count()


# print("Len of infected_meme2:",len(infected_meme2))
def count():
    global total_M1, total_M2
    countM1 = countM2 = 0
    for i in allNodes:
        if i.state == State.I1:
            countM1 += 1
        elif i.state == State.I2:
            countM2 += 1
    total_M1 = countM1
    total_M2 = countM2


def run_sim():
    global take_sample, allNodes, smp_size, total_M1, total_M2, tot_inf1, tot_inf2
    global infected_meme1, infected_meme2, M1_Wins, M2_Wins, No_win
    if take_sample == 1:
        for i in range(0, smp_size):
            set_simulation()
            if i % 10 == 0:
                print("Sample:", i)
            for t in range(0, tm):
                time.append(t)  ### add time to array to use for plot

                for i in allNodes:
                    if i.state == State.S:  ##check for state therefore cutting down on how many runs of each method happen
                        i.attack()
                    else:
                        i.recover()
                count()
                time_inf1.append(total_M1)
                time_inf2.append(total_M2)
            if total_M1 > total_M2 and ((total_M1 - total_M2) / N) > theta:
                M1_Wins += 1
            elif total_M2 > total_M1 and ((total_M2 - total_M1) / N) > theta:
                M2_Wins += 1
            else:
                No_win += 1
    else:
        for t in range(0, tm):
            time.append(t)  ### add time to array to use for plot
            if t % 100 == 0:
                print("Time:", t)

            for i in allNodes:
                if i.state == State.S:  ##check for state therefore cutting down on how many runs of each method happen
                    i.attack()
                else:
                    i.recover()
            count()
            # print("M1:",total_M1,"M2:",total_M2)
            time_inf1.append(total_M1)
            time_inf2.append(total_M2)


def plot_res(pause, supress, spr):
    global old_inf1, old_inf2
    fig = plt.figure()
    if take_sample == 0:

        plt.bar('Meme1', tot_inf1, color="red", width=1)
        plt.bar('Meme2', tot_inf2, color="blue", width=1)
        plt.xlabel("Meme")
        plt.ylabel("No. Total infections")
        plt.title("Total infections by meme")
        plt.show()
        if supress == True and pause == True:
            old_inf1 = time_inf1
            old_inf2 = time_inf2
        elif supress == True and pause == False:
            plt.plot(time, old_inf1, color="red",
                     label="Meme 1 λ = {}".format(eigenValues1[0]))
            plt.plot(time, old_inf2, color="blue",
                     label="Meme 2 λ ={}".format(eigenValues2[0]))
            plt.plot(time, time_inf1, color="green",
                     label="Meme 1 After {} Most common λ = {}".format(spr, eigenValues1[0]))
            plt.plot(time, time_inf2, color="yellow",
                     label="Meme 2 After {} Most common λ = {}".format(spr, eigenValues2[0]))
        plt.xlabel("Time,t")
        plt.ylabel("No. Total infections")
        plt.title("Total infections by meme")
        plt.legend()
        if pause != True:
            plt.show()

    if take_sample == 1:
        plt.bar('Meme1 wins', M1_Wins, color="red", width=1)
        plt.bar('Meme2 wins ', M2_Wins, color="blue", width=1)
        plt.bar('No Decisive winner', No_win, color="green", width=1)
        plt.xlabel("Meme")
        plt.ylabel("No. Total infections")
        plt.title("Total infections by meme")
        plt.show()


###SETUP#################################################################################################################################################################################################

"""
Setting up the Simulation Matrices
"""
A1 = np.random.randint(2, size=(N, N), dtype=np.int8)  # adjacency matrix for edge 1, filled with random 0s and 1s
np.fill_diagonal(A1, 0)  # make A1 diagonal 0's
A2 = np.random.randint(2, size=(N, N), dtype=np.int8)  # adjacency matrix for edge 2, filled with random 0s and 1s
np.fill_diagonal(A2, 0)  # make A2 diagonal 0's
##Make sure adj are symmetric and values are 2 or 1
##By making it symmetric, we are making sure if Node 1 is connected to Node 2, then Node 2 is also connected to Node 1.
A1 = (A1 + A1.T - np.diag(A1.diagonal())) % 2
A2 = (A2 + A2.T - np.diag(A2.diagonal())) % 2
##create System Matrices
S1 = (1 - delta1) * np.identity(N, dtype=np.int8) + beta1 * A1
S2 = (1 - delta2) * np.identity(N, dtype=np.int8) + beta2 * A2

# print(A1,"\n**********\n",A2,"\n**********\n",S1,"\n**********\n",S2,"\n**********\n")
""" 
Find the Eigenvalues of The System Matrices
"""

##get Eigen Values
eigenValues1, eigenVectors1 = linalg.eig(S1)
eigenValues2, eigenVectors2 = linalg.eig(S2)

##sort list of found eigenvalues to find the largest one
idx = eigenValues1.argsort()[::-1]
eigenValues1 = eigenValues1[idx]
eigenVectors1 = eigenVectors1[:,idx]

idx = eigenValues2.argsort()[::-1]
eigenValues2 = eigenValues2[idx]
eigenVectors2 = eigenVectors2[:,idx]

#Round largest eigenvalue so that it is not visually too large
eigenValues1[0] = round(eigenValues1[0], 4)
eigenValues2[0] = round(eigenValues2[0], 4)

print("Largest Eigen Value for Meme1: ", eigenValues1[0])
print("Largest Eigen Value for Meme2: ", eigenValues2[0])

""" 
Creating all the Nodes for the Simulation
"""
# Create Nodes
## Using our created Node data type, we fill a list with nodes of length N
for i in range(0, N):
    node = Node()
##sort nodes by ID number
allNodes.sort(key=lambda x: x.id, reverse=False)

# add neighbors to nodes from adjacency matrices
for i in allNodes:
    i.addNeighbors()

##create first list of infected nodes
## holds org sets to use for multiple lists
infected_meme1 = random.sample(allNodes,10)  # choose how many nodes start infected by meme 1
infected_meme2 = random.sample(allNodes, 10)  # choose how many nodes start infected  by meme 2


set_simulation()
count()

# method for removing random node
# randomRem()
# method for removing random neigbor


# sampled_M1_Wins = np.empty([2,50])
# sampled_M2_Wins = np.empty([2,50])
# sampled_No_Wins = np.empty([2,50])

""" 
Calling Methods to Run the Simulation without Meme Suppression
"""

################################################################################################################################################################################################################################################################################################################################################################
# Run Simulation without Supression
################################################################################################################################################################################


########################MAIN LOOP################################################################################################################################################################################

run_sim()
plot_res(True, True, "")
print("Number of Meme 1 wins:")
print(M1_Wins)
print("Number of Meme 2 wins:")
print(M2_Wins)
print("Number of  no clear winner:")
print(No_win)

# Showing Plots for one run
print("Total Infections by Meme 1:")
print(tot_inf1)

print("Total Infections by Meme 2:")
print(tot_inf2)

""" 
Calling Methods to Run the Simulation without Meme Suppression
"""
######################################################################################################################################################################################################################################################################################################################
# Run with Suppression Methods 
#####################################################################################################################################################################################################################################################################################################################

#############################
if total_M1 > total_M2:
    edge = 1
else:
    edge = 2
# infected_meme1 = random.sample(allNodes,random.randint(1,len(allNodes)/2))#randomly choose how many nodes start infected with no more than half being infected
# infected_meme2 = random.sample(allNodes,random.randint(1,len(allNodes)/2))#randomly choose how many nodes start infected  by meme 2
infected_meme1 = random.sample(allNodes,
                               2)  # randomly choose how many nodes start infected with no more than half being infected
infected_meme2 = random.sample(allNodes, 2)  # randomly choose how many nodes start infected  by meme 2

set_simulation()
print("M1:", total_M1)
print("M2:", total_M2)
count()
print("M1:", total_M1)
print("M2:", total_M2)
# randomNeigh(edge)
# randomRem()
max_degree(edge)
run_sim()
plot_res(False, True, "Max_Degree")

# Showing Plots for one run
print("After suppression\nTotal Infections by Meme 1:")
print(tot_inf1)

print("Total Infections by Meme 2:")
print(tot_inf2)

