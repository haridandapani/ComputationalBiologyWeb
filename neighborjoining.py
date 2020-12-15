import sys
import graphviz
import pydot


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
            pairer = (sorter[0], sorter[1]) #think about adding height to this data structure
            storage[pairer] = float(lval[2])
            cluster.add(lval[0])
            cluster.add(lval[1])
            namedepth[lval[0]] = NameDepth(lval[0], 0)
            namedepth[lval[1]] = NameDepth(lval[1], 0)
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
                pairer = (sorter[0], sorter[1])
                storage[pairer] = float(eachChar[i][j])
                cluster.add(val1)
                cluster.add(val2)
                namedepth[val1] = NameDepth(val1, 0)
                namedepth[val2] = NameDepth(val2, 0)
    return storage, cluster, namedepth, heights

def getLowestPair(storage):
    val1, val2 = "", ""
    minner = float("inf")
    lexo = ""
    for key in storage.keys():
        if storage[key] < minner:
            minner = storage[key]
            val1, val2 = key[0], key[1]
            lexo = "("+val1+","+val2+")" if val1 < val2 else "("+val2+","+val1+")"
        elif storage[key] == minner:
            temper = "("+key[0]+","+key[1]+")" if key[0] < key[1] else "("+key[1]+","+key[0]+")"
            if temper < lexo:
                minner = storage[key]
                val1, val2 = key[0], key[1]
                lexo = "("+val1+","+val2+")" if val1 < val2 else "("+val2+","+val1+")"                
    return (val1, val2)

def generateQTable(storage, clusters):
    qtable = dict()
    q = 0
    maxer = float('inf')
    curr = None
    corr = len(clusters) - 2
    vone = 0
    vtwo = 0
    for key in storage.keys():
        dist = storage[key]
        valforone = 0
        valfortwo = 0
        for node in clusters:
            if node != key[0]:
                sorter =[key[0], node] if key[0] < node else [node, key[0]]
                pairer = (sorter[0], sorter[1])
                valforone += storage[pairer]
            if node != key[1]:
                sorter =[key[1], node] if key[1] < node else [node, key[1]]
                pairer = (sorter[0], sorter[1])
                valfortwo += storage[pairer]
        qtable[key] = corr * storage[key] - valforone - valfortwo
        if qtable[key] < maxer:
            maxer = qtable[key]
            curr = key
            vone = valforone
            vtwo = valfortwo
    return qtable, curr, vone, vtwo

def renewStorage(storage, clusters, namedepth, heights):
    qtable, curr, vone, vtwo = generateQTable(storage, clusters)
    newNode = "("+curr[0]+","+curr[1]+")"
    factor = 1 / (2 * (len(clusters) - 2))
    heights[(newNode, curr[0])] = 0.5 * storage[curr] - (factor * (vtwo - vone))
    heights[(newNode, curr[1])] = 0.5 * storage[curr] - (factor * (vone - vtwo))

    for node in clusters:
        if node != curr[0] and node != curr[1]:
           sorter =[node, curr[0]] if node < curr[0] else [curr[0], node]
           sorter2 =[node, curr[1]] if node < curr[1] else [curr[1], node]
           newer = [node, newNode] if node < newNode else [newNode, node]
           storage[(newer[0], newer[1])] = 0.5 * (storage[(sorter[0], sorter[1])] + storage[(sorter2[0], sorter2[1])] - storage[curr])

    copy = dict(storage)
    for key in storage.keys():
        if key[0] == curr[0] or key[0] == curr[1] or key[1] == curr[0] or key[1] == curr[1]:
            copy.pop(key)

    clusters.remove(curr[0])
    clusters.remove(curr[1])
    clusters.add(newNode)
    storage = dict(copy)
    return storage, clusters, namedepth, heights


def writeToFile(text : str, fileName : str):

    output = "graph neighborjoining { \n"
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

def constructTree(heights):
    output = "graph neighbor { \n"
    for key in heights.keys():
        output += ("\""+key[0] + "\"" +" -- " + "\"" + key[1] + "\"" + " [label = " + str(heights[key])+']\n')
    output += "}"
    return output
        

def writeToFile(text : str, fileName : str):
    f = open(fileName, "a")
    f.truncate(0)
    f.write(text)
    f.close()

def neighborrunner(distances : str, fileName : str, matrix : bool):

    storage, clusters, namedepth, heights = None, None, None, None
    if matrix:
        storage, clusters, namedepth, heights = openMatrixFormat(distances)
    else:
        storage, clusters, namedepth, heights = openAndStore(distances)
    while len(clusters) > 2:
        storage, clusters, namedepth, heights = renewStorage(storage, clusters, namedepth, heights)

    if (len(clusters) != 0):
        for key in storage.keys():
            heights[key] = storage[key]

    dotcontent = constructTree(heights)
    path = "uploads/"+fileName
    writeToFile(dotcontent, path+".dot")
    (graph,) = pydot.graph_from_dot_file(path+".dot")
    graph.write_png(path+'.png')
    return fileName+".dot", fileName+".png"

