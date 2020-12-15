import sys

def openSequences(file : str):
    texts = open(file, "r")
    seq1 = texts.readline().replace('\n','')
    seq2 = texts.readline().replace('\n','')
    return (seq1, seq2)

def failure(stringer : str): # table indexes at 0
    table = dict()
    i = 0
    j = 1
    table[j - 1] = 0
    for j in range(2, len(stringer) + 1):
        i = table[j - 2]
        while stringer[j - 1] != stringer[i] and i > 0:
            i = table[i - 1]
        if stringer[j - 1] != stringer[i] and i == 0:
            table[j - 1] = 0
        else:
            table[j - 1] = i + 1
    return table

def kmp(search, pattern):
    j = 0
    k = 0
    hits = list()
    pat_length = len(pattern)
    search_length = len(search)
    ff = failure(pattern)

    if (pat_length > 0):
        while j < search_length:
            if pattern[k] == search[j]:
                j += 1
                k += 1
                if (k == pat_length):
                    hits.append(j - k)
                    k = ff[k - 1]
            else:
                if k != 0:
                    k = ff[k - 1]
                else:
                    j += 1
    return(hits, ff)

def convert_output(output):
    if len(output) == 0:
        return -1
    elif len(output) == 1:
        return output[0]
    else:
        return output

def highlightHits(search, hits):
    highlighted = ""
    for i in range(len(search)):
        if i in hits:
            highlighted +="<mark>"+search[i]+"</mark>"
        else:
            highlighted += search[i]
    return highlighted

def knuth(search, pattern):
    hits, ff = kmp(search, pattern)
    highlights = highlightHits(search, hits)
    return highlights, list(pattern), ff

def runner(file : str):
    seq1, seq2 = openSequences(file)
    output = kmp(seq1, seq2)
    print(convert_output(output))

#runner(sys.argv[1])
