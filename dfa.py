import sys
import graphviz
import pydot

def openSequences(file : str):
    texts = open(file, "r")
    seq = texts.readline().replace('\n','')
    return seq

def failure(stringer : str): # table indexes at 1
    table = dict()
    i = 0
    j = 1
    table[j] = 0
    for j in range(2, len(stringer) + 1):
        i = table[j - 1]
        while stringer[j - 1] != stringer[i] and i > 0:
            i = table[i]
        if stringer[j - 1] != stringer[i] and i == 0:
            table[j] = 0
        else:
            table[j] = i + 1
    return table

def transition(stringer : str, alphabet):
    output = "digraph dfa {\n"
    ff = failure(stringer)
    transition = dict()
    # just the straight line at the beginning
    for j in range(1, len(stringer) + 1):   
        transition[j - 1] = dict()
        transition[j - 1][stringer[j - 1]] = j
        output += ("  "+str(j - 1) + " -> " + str(j) + " [ label = \""+ stringer[j - 1] +"\"];\n")
        
    output += ("  " + str(len(stringer)) + " [ peripheries = 2 ];\n")

    if (len(stringer) > 0):
        for letter in alphabet:
            if (letter != stringer[0]):
                transition[0][letter] = 0

    for j in range(1, len(stringer)):
        for letter in alphabet:
            if letter != stringer[j]:
                transition[j][letter] = transition[ff[j]][letter]
                if (transition[j][letter] != 0):
                    output += ("  " + str(j) + " -> " + str(transition[j][letter]) + " [ label = \""+ letter +"\"];\n")
    output +="}"
    return output

def runWithACGT(stringer : str):
    alphabet = ["A", "C", "G", "T"]
    return transition(stringer, alphabet)

def getAlphabet(seq : str):
    alphabet = set()
    for s in seq:
        alphabet.add(s)
    return alphabet

def writeFile(fileName : str, text : str):
    f = open(fileName, "a")
    f.truncate(0)
    f.write(text)
    f.close()

def runner(file : str, newFile : str):
    seq = openSequences(file)
    alphabet = getAlphabet(seq)
    output = transition(seq, alphabet)
    writeFile(newFile, output)

def runWithString(seq : str, filer):
    alphabet = getAlphabet(seq)
    output = transition(seq, alphabet)
    name = "uploads/"+filer
    writeFile(name+".dot", output)
    (graph,) = pydot.graph_from_dot_file(name+".dot")
    graph.write_png(name+'.png')
    return (filer+".dot", filer+".png")
