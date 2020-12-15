import sys
import graphviz
import pydot

class MatchPair:
    def __init__(self, char1, char2):
        self.char1 = char1
        self.char2 = char2
    def __hash__(self):
        return hash(self.char1 + self.char2)
    def __eq__(self, other):
     return self.__class__ == other.__class__ and ((self.char1 == other.char1 and self.char2 == other.char2)
                                                   or (self.char1 == other.char2 and self.char2 == other.char1))
    def __str__(self):
        return "("+self.char1+","+self.char2+")"

class NameDepth:
    def __init__(self, name, depth):
        self.name = name
        self.depth = depth

def openAndStore(file : str):
    storage = dict()
    cluster = set()
    namedepth = dict()
    heights = dict()
    with open(file) as dists:
        for line in dists:
            lval = line.replace('\n','').split()
            sorter =[lval[0], lval[1]] if lval[0] < lval[1] else [lval[1], lval[0]]
            pairer = MatchPair(sorter[0], sorter[1]) #think about adding height to this data structure
            storage[pairer] = float(lval[2])
            cluster.add(lval[0])
            cluster.add(lval[1])
            namedepth[lval[0]] = NameDepth(lval[0], 0)
            namedepth[lval[1]] = NameDepth(lval[1], 0)
            heights[lval[0]] = 0
            heights[lval[1]] = 0
    return storage, cluster, namedepth, heights

def openMatrixFormat(file : str):
    storage = dict()
    cluster = set()
    namedepth = dict()
    heights = dict()

    f = open(file, "r")
    eachLine = f.readlines()
    eachChar = list()
    for i in range(0, len(eachLine)):
       eachChar.append(eachLine[i].replace('\n', '').split())

    for i in range(1, len(eachChar)):
        for j in range(1, len(eachChar[i])):
            val1 = eachChar[0][i]
            val2 = eachChar[j][0]
            sorter =[val1, val2] if val1 < val2 else [val2, val1]
            if sorter[0] != sorter[1]:
                pairer = MatchPair(sorter[0], sorter[1])
                storage[pairer] = float(eachChar[i][j])
                cluster.add(val1)
                cluster.add(val2)
                namedepth[val1] = NameDepth(val1, 0)
                namedepth[val2] = NameDepth(val2, 0)
                heights[val1] = 0
                heights[val2] = 0
    return storage, cluster, namedepth, heights

def getLowestPair(storage):
    val1, val2 = "", ""
    minner = float("inf")
    lexo = ""
    for key in storage.keys():
        if storage[key] < minner:
            minner = storage[key]
            val1, val2 = key.char1, key.char2
            lexo = "("+val1+","+val2+")" if val1 < val2 else "("+val2+","+val1+")"
        elif storage[key] == minner:
            temper = "("+key.char1+","+key.char2+")" if key.char1 < key.char2 else "("+key.char2+","+key.char1+")"
            if temper < lexo:
                minner = storage[key]
                val1, val2 = key.char1, key.char2
                lexo = "("+val1+","+val2+")" if val1 < val2 else "("+val2+","+val1+")"                
    return (val1, val2)

def renewStorage(storage, val1, val2, text, clusters, namedepth, heights):

    correction = 5.0
    val12 = [val1, val2] if val1 < val2 else [val2, val1]
    depth = max(namedepth[val1].depth, namedepth[val2].depth) + 1
    
    newNode = "("+val1+","+val2+")" if val1 < val2 else "("+val2+","+val1+")"
    namedepth[newNode] = NameDepth(namedepth[val12[0]].name + namedepth[val12[1]].name, depth)
    heights[newNode] = storage[MatchPair(val12[0], val12[1])] /2
    

    text += (namedepth[val1].name + str(namedepth[val1].depth) +" -- " +
             namedepth[newNode].name + str(namedepth[newNode].depth)+"[label = " + str(heights[newNode] - heights[val1])+
             ', minlen ='+ str((heights[newNode] - heights[val1])/correction)+']\n')
    text += (namedepth[val2].name + str(namedepth[val2].depth) +" -- " +
             namedepth[newNode].name + str(namedepth[newNode].depth)+"[label = " + str(heights[newNode] - heights[val2])+
             ', minlen ='+ str((heights[newNode] - heights[val2])/correction)+']\n')

    clusters.remove(val1)
    clusters.remove(val2)
    clusters.add(newNode)
    
    copy = dict(storage) 

    for cluster in clusters:
        if cluster != newNode:
            sorter = [newNode, cluster] if newNode < cluster else [cluster, newNode]
            pairer = MatchPair(sorter[0], sorter[1])

            sorterval1 = [val1, cluster] if val1 < cluster else [cluster, val1]
            sorterval2 = [val2, cluster] if val2 < cluster else [cluster, val2]
            
            copy[pairer] = ((storage[MatchPair(sorterval1[0], sorterval1[1])] * (val1.count(",") + 1)) +
                            storage[MatchPair(sorterval2[0], sorterval2[1])] * (val2.count(",") + 1)) / (val1.count(",") + val2.count(",") + 2)
            
    for key in storage.keys():
        if key.char1 == val1 or key.char1 == val2 or key.char2 == val1 or key.char2 == val2:
            copy.pop(key)
    
    return copy, text, clusters, namedepth

def finish(clusters, namedepth, text, heights, storage):
    correction = 5.0
    val1 = clusters.pop()
    val2 = clusters.pop()

    val12 = [val1, val2]
    val12.sort()
    
    depth = max(namedepth[val1].depth, namedepth[val2].depth) + 1

    newNode = "("+val1+","+val2+")" if val1 < val2 else "("+val2+","+val1+")"
    heights[newNode] = storage[MatchPair(val12[0], val12[1])] /2
    namedepth[newNode] = NameDepth(namedepth[val12[0]].name + namedepth[val12[1]].name, depth)

    text += (namedepth[val1].name + str(namedepth[val1].depth) +" -- " + namedepth[newNode].name +
             str(namedepth[newNode].depth)+"[label = " + str(heights[newNode] - heights[val1])+
             ', minlen ='+ str((heights[newNode] - heights[val1])/correction)+']\n')
    text += (namedepth[val2].name + str(namedepth[val2].depth) +" -- " + namedepth[newNode].name +
             ', minlen ='+ str((heights[newNode] - heights[val2])/correction)+']\n')


    return newNode, text

def writeToFile(text : str, fileName : str):

    output = "graph upgma { \n"
    output += text
    output += "}"
    f = open(fileName, "a")
    f.truncate(0)
    f.write(output)
    f.close()

def printStorage(storage):
    for key in storage.keys():
        print(key, end = ":")
        print(storage[key])

def runner(distances : str, fileName : str, matrix : bool):

    storage, clusters, namedepth, heights = None, None, None, None
    if matrix:
        storage, clusters, namedepth, heights = openMatrixFormat(distances)
    else:
        storage, clusters, namedepth, heights = openAndStore(distances)

    text = ""
    while len(clusters) > 2:
        p1, p2 = getLowestPair(storage)
        storage, text, clusters, namedepth = renewStorage(storage, p1, p2, text, clusters, namedepth, heights)

    end = ""
    if (len(clusters) != 0):
        end, text = finish(clusters, namedepth, text, heights, storage)
    path = "uploads/"+fileName
    writeToFile(text, path+".dot")
    (graph,) = pydot.graph_from_dot_file(path+".dot")
    graph.write_png(path+'.png')
    return fileName+".dot", fileName+".png"
