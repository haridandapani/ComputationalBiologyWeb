def forwardtransform(string, delimiter):
    assert len(delimiter) == 1 and delimiter not in string
    string2 = string + delimiter
    print(string2)
    lister = list()
    for i in range(len(string2)):
        lister.append(string2[i:] + string2[0:i])
    allrotations = list(lister)
    lister.sort()
    output = ""
    for i in range(len(lister)):
        output += lister[i][len(string2) - 1]
    return output, allrotations, lister

def inversetransform(string, delimiter):
    assert len(delimiter) == 1 and string.count(delimiter) == 1
    base = list()
    adds = list()
    sorts = list()
    base[:0]=string
    temp = ["" for _ in range(len(string))]
    for j in range(len(string)):
        for k in range(len(temp)):
            temp[k] = base[k] + temp[k]
        adds.append(temp.copy())
        temp.sort()
        sorts.append(temp.copy())

    for elem in temp:
        if elem[len(string) - 1] == delimiter:
            return elem, adds, sorts
#print(forwardtransform("Barack Hussein Obama $$44$$", "|"))
#print("========")
#print(inversetransform("akn 4$$4$|  mrbBOasecaiasuH$", "|")[0])
