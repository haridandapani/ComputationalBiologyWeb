import random
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def gauss(mu, sigma):
    x = random.gauss(mu, sigma)
    return round(x, 3)

def generate2d(mu1, sigma1, mu2, sigma2):
    x = gauss(mu1, sigma1)
    y = gauss(mu2, sigma2)
    return [x, y]

def generateKpoints(k, gridsize):
    points = []
    mu1 = random.randrange(1, gridsize)
    sigma1 = random.randrange(3, 6)
    mu2 = random.randrange(1, gridsize)
    sigma2 = random.randrange(3, 6)
    for j in range(k):
        points.append(generate2d(mu1, sigma1, mu2, sigma2))
    return points

def generateKclusters(k, gridsize):
    allpoints = []
    numpoints = random.randrange(25, 75)
    for j in range(k):
        allpoints += generateKpoints(numpoints, gridsize)
        print(len(allpoints))
    return(allpoints)

def writeToCSV(name, allpoints, labels):
    csv = open(name, 'w')
    csv.write("X, Y, Label \n")
    for index, point in enumerate(allpoints):
        csv.write(str(point[0]) +"," + str(point[1]) +", " + str(labels[index]))
        csv.write("\n")

def scatter(allpoints, labels):
    x = allpoints[:, 0]
    y = allpoints[:, 1]
    plt.scatter(x, y, c = labels, alpha=0.5)
    plt.show()

def savescatter(allpoints, labels, name):
    x = allpoints[:, 0]
    y = allpoints[:, 1]
    maxnum = int(np.max(labels)) + 2
    print(maxnum)
    print(labels)
    colorlist = colors(maxnum)
    plt.scatter(x, y, c = labelstocolors(colorlist, labels), alpha=0.5)
    plt.savefig(name)

def labelstocolors(colors, labels):
    output = []
    for i in labels:
        output.append(colors[int(1+i)])
    return output

def dbscan(allpoints, distfunc, epsilon, minpoints):
    labels = np.zeros(np.shape(allpoints)[0])
    c = 0
    for p in range (np.shape(allpoints)[0]):
        if labels[p] != 0:
            continue
        neighbors = rangequery(allpoints, distfunc, allpoints[p], epsilon)
        if (len(neighbors) < minpoints):
            labels[p] = -1
            continue
        c+=1
        labels[p] = c
        neighbors.remove(p)
        while neighbors:
            q = neighbors.pop(0)
            if labels[q] == -1:
                labels[q] = c
            elif labels[q] != 0:# already labeled
                continue
            labels[q] = c
            newneighbors = rangequery(allpoints, distfunc, allpoints[q], epsilon)
            if (len(newneighbors) >= minpoints):
                neighbors += newneighbors
    return(labels)
            

def distfunc(a, b):
    dist = np.linalg.norm(a-b)
    return dist

def rangequery(allpoints, distfunc, pointer, epsilon):
    neighbors = []
    for p in range(np.shape(allpoints)[0]):
        if (distfunc(pointer, allpoints[p]) < epsilon):
            neighbors.append(p)
    return neighbors
        

def colors(number_of_colors):
    color = ["#"+''.join([random.choice('123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]
    color[0] = "#000000"
    return color

def runner():
    allpoints = np.array(generateKclusters(5, 100))
    labels = dbscan(allpoints, distfunc, 4, 4)
    print(labels)
    scatter(allpoints, labels)
    writeToCSV("namer.csv", allpoints, labels)
    

def DBSCANWithParams(gridsize, numclusters, name):
    allpoints = np.array(generateKclusters(int(numclusters), int(gridsize)))
    labels = dbscan(allpoints, distfunc, 4, 4)
    print("finished with algorithm")
    sname = name+".png"
    scattername = "uploads/"+sname
    cname = name+".csv"
    csvname = "uploads/"+cname
    print("pre scatter")
    savescatter(allpoints, labels, scattername)
    print("at  csv")
    writeToCSV(csvname, allpoints, labels)
    return cname, sname
    
