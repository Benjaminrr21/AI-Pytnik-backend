from array import array
import heapq

from ast import Str
from itertools import permutations
from lib2to3.pytree import Node
from operator import indexOf
import queue
import re
from sys import path

#from PytnikSolved.PytnikMladenZurkic.util import Node


matrica = [
    [0,25,17,12],
    [25,0,30,22],
    [17,30,0,31],
    [12,22,31,0]
]
row = 4
col = 4


# Aki
def AkiPath(mat) :
    coins = [i for i in range(1,len(mat))] #broj redova => coins = 1 2 3 
    path = []
    startNode = 0
    path.append(startNode)
    while len(coins): #dok se coins ne isprazni
        myDict = {}
        red = mat[startNode]
        for i in coins:
            myDict[i] =  red[i]
        startNode = min(myDict,key=myDict.get) #vraca key sa najmanjim value
        path.append(startNode)
        coins.remove(startNode)
    path.append(0)
    return path





#Jocke



def JockePath(mat):
    def ConvertToLIst(permut):
        permutList = list(permut)
        permutNiz = []
        for i in range(0,len(permutList)) : 
            permutNiz.append([0] + list(permutList[i]))
        return permutNiz
    perm = permutations([1,2,3])
    permutationss = ConvertToLIst(perm)
    print("Permutacije 1,2,3 u listu listi:")
    print(permutationss)
    def CalculateValue(list):
        i=0
        j=1
        path_distance = 0

        while j < len(list):
            
            path_distance += mat[list[i]][list[j]]
            i+=1
            j+=1
        return path_distance
    pathValues = []
    nizZaPermutaciju = (i for i in range(1,len(mat)))
    permutacije = permutations(nizZaPermutaciju)
    lista = ConvertToLIst(permutacije)
    #print(lista)
    mojDict = {}
    for i in range(0,len(lista)):
        val = CalculateValue(lista[i])
        #pathValues.append(val)
        mojDict[str(lista[i])] = val
    #print("Cena iznosi: ")
    #print(min(list(mojDict.values)))
    obj = min(mojDict,key=mojDict.get)
    niz = obj.replace(" ","")
    lista = []
    for i in range(1,len(niz)-1):
        if i%2!=0: lista.append(niz[i])

    #retList = list(obj) + [0]
    print("Najmanja putanja za matricu je" ,obj,", a njena vrednost je" ,mojDict[obj], ".")
    print("Niz:",niz, "Broj elemenata:",len(niz))
    print("Lista:",niz, "Broj elemenata:",len(lista))
    lista.append('0')
    return lista
    
        #return min(mojDict,key=mojDict.get)  

    
print(JockePath(matrica))

""" dic = {
}
dic[10] = "133"
dic[15] = "11"
next = min(dic,key=dic.get)

niz = [1,2,3,4]
niz2 = [i for i in range(0,len(niz))]
print(niz2)      
print(len(matrica))  
returnList = GetPath(matrica)
print(returnList)   """


#Let's make a function whitch will calculate path distance between nodes
# input -> list
# output -> value of path distance
#npr 1 3 2 0 


""" listaa = [[0,1,2,3],[0,1,3,2],[0,2,1,3],[0,2,3,1],[0,3,1,2],[0,3,2,1]]
for i in range(0,len(listaa)):
    print(CalculateValue(listaa[i])) """


#Uki - Branch and bound
def UkiPath(mat):

    class Node():
        def __init__(self, path = 0, cost = 0, level = 0, heur = 0):
            self.path = path
            self.cost = cost
            self.level = level
            self.heur = heur

        def __eq__(self, obj):
            return self.cost == obj.cost

        def __lt__(self, obj):
            return self.cost < obj.cost

        def __gt__(self, obj):
            return self.cost > obj.cost

    path = (i for i in range(1,len(mat)))
    n = len(mat)
    firstNode = Node([0],0,0)
    queueOfNodes = queue.PriorityQueue()
    queueOfNodes.put((firstNode.cost,n-len(firstNode.path),firstNode.path[-1],firstNode))
    while not queueOfNodes.empty():
            curr = queueOfNodes.get()[3] #poslednj tj najmanji
            if (len(curr.path) == (n + 1)):  #Nasli smo putanju sa ciljnim cvorom
                return curr.path
            if(len(curr.path) == n): # Ako je putanja obisla sve sem krajnjeg, treba da se vrati
                remaining = [0]
            else:
                remaining = [i for i in range(1, n) if i not in curr.path]
            for i in remaining:
                queueOfNodes.put((curr.cost + mat[curr.path[-1]][i], n - (curr.level + 1), i,
                                Node(curr.path + [i], curr.cost + mat[curr.path[-1]][i], curr.level + 1)))
    return []

print("Branch and bound: ",UkiPath(matrica))

#Micko - A*
def MickoPath(coin_distance):

        path = [i for i in range(1, len(coin_distance))]
        n = len(coin_distance)  # 8
        firstNode = (0, n, 0, [0], 0)
        listOfNodes = [firstNode]
        heapq.heapify(listOfNodes)
        while (len(listOfNodes) != 0):
            curr = heapq.heappop(listOfNodes)
            if (len(curr[3]) == (n + 1)):  # Nasli smo putanju sa ciljnim cvorom
                return curr[3]
            if (len(curr[3]) == n):  # Ako je putanja obisla sve sem krajnjeg, treba da se vrati
                remaining = [0]
            else:
                remaining = [i for i in range(1, n) if i not in curr[3]]
            expandAndCalculate(remaining, listOfNodes, curr, coin_distance, n)

def expandAndCalculate(remaining, listOfNodes, curr, coin_distance, n):
    scaledMatrix = scaleMatrix(curr, n, coin_distance)
    if not len(scaledMatrix):
        heur = 0
    else:
        heur = primsAlgorithm(scaledMatrix)
    for i in remaining:
        heapq.heappush(listOfNodes, (curr[4] + coin_distance[curr[2]][i] + heur, (curr[1] - 1), i, curr[3] + [i], curr[4] + coin_distance[curr[2]][i]))

def scaleMatrix(curr, n, coin_distance):
    newlist = []
    selected = [i for i in range(1, n) if i not in curr[3]]
    if not len(selected):
        return []
    selected.append(0)
    selected.sort()
    for i in selected:
        subList = []
        for j in selected:
            subList.append(coin_distance[i][j])
        newlist.append(subList)
    return newlist

def primsAlgorithm(scaledMatrix):
    inf = 2147483647
    n = len(scaledMatrix)
    selected_node = [0] * n
    no_edge = 0
    selected_node[0] = True
    sumAll = 0
    while (no_edge < n - 1):
        minimum = inf
        a = 0
        b = 0
        for m in range(n):
            if selected_node[m]:
                for i in range(n):
                    if((not selected_node[i]) and scaledMatrix[m][i]):
                        if minimum > scaledMatrix[m][i]:
                            minimum = scaledMatrix[m][i]
                            a = m
                            b = i
        sumAll = sumAll + scaledMatrix[a][b]
        selected_node[b] = True
        no_edge = no_edge + 1
    return sumAll
print("A* -> " ,MickoPath(matrica))