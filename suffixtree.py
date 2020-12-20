class SuffixNode:
    def __init__(self, character, depth, producer, parent = None):
        self.character = character
        self.depth = depth
        self.parent = parent
        self.producer = producer
    def __str__(self):
        return "\""+self.character + str(self.depth)+str(self.producer)+"\""
    def toString(self):
        return self.__str__()
    def __hash__(self):
        return hash(self.character) * hash(self.depth) * hash(self.producer)
    def __eq__(self, other):
        # recursive equals
        return self.__class__ == other.__class__ and self.character == other.character and self.depth == other.depth and self.parent == other.parent


def makeSuffixTree(stringer : str, delimiter = "$"):
    assert len(delimiter) == 1 and delimiter not in stringer
    stringer = stringer + delimiter
    totalcounts = 0
    lister = list()
    for s in range(len(stringer)):
        temp = stringer[s:len(stringer)]
        prev = None
        for j in range(len(temp)):
            newer = SuffixNode(temp[j], j, totalcounts, prev)
            totalcounts += 1

            if newer in lister:
                for it in lister:
                    if newer == it:
                        newer = it
            else:
                lister.append(newer)
            prev = newer
    return(constructDot(lister, delimiter))

def constructDot(lister, delimiter):
    counter = 0
    text = "digraph suffixtree {\n"
    text += ("head [shape=circle, style=filled, fillcolor=black]\n")
    for elem in lister:
        delimits = elem.character == delimiter
        if elem.parent != None:
            if delimits:
                text += (elem.parent.toString() +" -> " + str(counter) + " [label = \" "+elem.character+"\"]\n")
                counter += 1
            else:
                text += (elem.parent.toString() +" -> " + elem.toString() + " [label = \" "+elem.character+"\"]\n")
                text += (elem.toString() +" [shape=circle, style=filled, fillcolor=black]\n")
        else:
            if delimits:
                text += ("head -> " + str(counter) + " [label = \" "+elem.character+"\"]\n")
                counter += 1
            else:
                text += ("head -> " + elem.toString() + " [label = \" "+elem.character+"\"]\n")
                text += (elem.toString() +" [shape=circle, style=filled, fillcolor=black]\n")
    text += "}"
    return(text)

def writeFile(fileName : str, text : str):
    f = open(fileName, "a")
    f.truncate(0)
    f.write(text)
    f.close()

def suffixTreeMaker(seq : str, delimiter, filer):
    output = makeSuffixTree(seq, delimiter)
    name = "uploads/"+filer
    writeFile(name+".dot", output)
    (graph,) = pydot.graph_from_dot_file(name+".dot")
    graph.write_png(name+'.png')
    return (filer+".dot", filer+".png")

#makeSuffixTree("Hari")
#makeSuffixTree("abrabra")
#makeSuffixTree("ABRACADABRA", "!")
#thisNode = SuffixNode("A", 0, None)
#thatNode = SuffixNode("B", 0, thisNode)
#print(thatNode)
#thatNodex = SuffixNode("B", 0)
#lister = {thisNode}
#print(thatNode in lister)
