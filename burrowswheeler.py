def forwardtransform(string):
    string2 = string +'|'
    print(string2)
    lister = list()
    for i in range(len(string2)):
        lister.append(string2[i:] + string2[0:i])
    allrotations = list(lister)
    lister.sort()
    output = ""
    for i in range(len(lister)):
        output += lister[i][len(string2) - 1]
    return output

def inversetransform(string):
    base = list()
    base[:0]=string
    temp = ["" for _ in range(len(string))]
    for j in range(len(string)):
        for k in range(len(temp)):
            temp[k] = base[k] + temp[k]
        temp.sort()

    for elem in temp:
        if elem[len(string) - 1] == "|":
            return elem

#forwardtransform("Hari")
print(inversetransform(forwardtransform("^BANANA")))
print(inversetransform(forwardtransform("Barack Hussein Obama 44$$")))
