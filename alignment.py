import math
class MatchPair:
    def __init__(self, char1, char2):
        self.char1 = char1
        self.char2 = char2
    def __hash__(self):
        return hash(self.char1)
    def __eq__(self, other):
     return self.__class__ == other.__class__ and self.char1.upper() == other.char1.upper() and self.char2.upper() == other.char2.upper()

class ScoreDirection:
    def __init__(self, score, direction):
        self.score = score
        self.direction = direction # 0 is free, 1 is up, 2 is left, 3 is diagonal

class ScoreMatrix:
    def __init__(self, score, matrix):
        self.score = score
        self.matrix = matrix # E = 1, F = 2, G = 3, V = 4


def openSequences(file : str):
    texts = open(file, "r")
    seq1 = texts.readline().replace('\n','')
    seq2 = texts.readline().replace('\n','')
    return [seq1, seq2]

def openScoringMatrix(file : str, gapPenalty):
    f = open(file, "r")
    eachLine = f.readlines()
    eachChar = list()
    for i in range(0, len(eachLine)):
        #eachChar.append(eachLine[i].rstrip().replace('\n', '').replace('  ', ' ').split(' '))
        eachChar.append(eachLine[i].replace('\n', '').split())
    scores = dict()
    for i in range(1, len(eachChar)):
        for j in range(1, len(eachChar[i])):
            pairer = MatchPair(eachChar[0][i].upper(), eachChar[j][0].upper())
            scores[pairer] = float(eachChar[i][j])
            indel1 = MatchPair('-', eachChar[j][0].upper())
            indel2 = MatchPair(eachChar[0][i].upper(), '-')
            scores[indel1] = gapPenalty
            scores[indel2] = gapPenalty
    return scores

def makeScoringTable(x, y, gapPenalty):
    matrix = list()
    for row in range(x):
        lister = list()
        for col in range(y):
            if row == 0:
                lister.append(ScoreDirection(col * gapPenalty, 2))
            elif col == 0:
                lister.append(ScoreDirection(row * gapPenalty, 1))
            else:
                lister.append(ScoreDirection(0, 0))
        matrix.append(lister)
    return matrix

def makeZeroTable(x, y):
    return [[ScoreDirection(0.0, 0) for col in range(y)] for row in range(x)]

def maxScoreDirection(lister):
    best = None
    bestScore = float('-inf')
    for l in lister:
        if l.score > bestScore:
            best = l
            bestScore = l.score
    return best

def minScoreDirection(lister):
    best = None
    bestScore = float('inf')
    for l in lister:
        if l.score < bestScore:
            best = l
            bestScore = l.score
    return best

def gbtraceback(seq1, seq2, scoringScheme, gapPenalty, optimization):
    matrix = makeScoringTable(len(seq1) + 1, len(seq2) + 1, gapPenalty)
    for i in range(1, len(matrix)):
        for j in range(1, len(matrix[i])):
            if optimization == "score":
                matrix[i][j] = maxScoreDirection([ScoreDirection(matrix[i-1][j-1].score + scoringScheme[MatchPair(seq1[i - 1].upper(), seq2[j - 1].upper())], 3),
                ScoreDirection(matrix[i-1][j].score + scoringScheme[MatchPair(seq1[i - 1].upper(), '-')], 1),
                ScoreDirection(matrix[i][j-1].score + scoringScheme[MatchPair('-', seq2[j - 1].upper())], 2)])
            else:
                matrix[i][j] = minScoreDirection([ScoreDirection(matrix[i-1][j-1].score + scoringScheme[MatchPair(seq1[i - 1].upper(), seq2[j - 1].upper())], 3),
                ScoreDirection(matrix[i-1][j].score + scoringScheme[MatchPair(seq1[i - 1].upper(), '-')], 1),
                ScoreDirection(matrix[i][j-1].score + scoringScheme[MatchPair('-', seq2[j - 1].upper())], 2)])

    seqX = ""
    seqY = ""
    finalScore = 0
    i = len(seq1)
    j = len(seq2)

    while (i > 0 or j > 0):
        curr_node = matrix[i][j]
        if i > 0 and j > 0 and curr_node.direction == 3:
            seqX = seq1[i - 1] + seqX
            seqY = seq2[j - 1] + seqY
            finalScore += scoringScheme[MatchPair(seq1[i - 1].upper(), seq2[j - 1].upper())]
            i = i - 1
            j = j - 1
        elif (i > 0 and curr_node.direction == 1):
            seqX = seq1[i - 1] + seqX
            seqY = '-' + seqY
            finalScore += scoringScheme[MatchPair(seq1[i - 1].upper(), '-')]
            i = i - 1
        elif (j > 0 and curr_node.direction == 2):
            seqX = '-' + seqX
            seqY = seq2[j - 1] + seqY
            finalScore += scoringScheme[MatchPair('-', seq2[j - 1].upper())]
            j = j - 1
    return (seqX, seqY, finalScore)     

def latraceback(seq1 : str, seq2 : str, scoringScheme):
    matrix = makeZeroTable(len(seq1) + 1, len(seq2) + 1) #seq1 on left; seq2 on top
    max_yet = float('-inf')
    high_i, high_j = 0, 0
    for i in range (1, len(matrix)):
        for j in range (1, len(matrix[i])):
            # -1 since we added 1 to i and j

            matrix[i][j] = maxScoreDirection([ScoreDirection(matrix[i-1][j-1].score + scoringScheme[MatchPair(seq1[i - 1].upper(), seq2[j - 1].upper())], 3),
            ScoreDirection(matrix[i-1][j].score + scoringScheme[MatchPair(seq1[i - 1].upper(), '-')], 2),
            ScoreDirection(matrix[i][j-1].score + scoringScheme[MatchPair('-', seq2[j - 1].upper())], 1),
            ScoreDirection(0.0, 0)])
            
            if matrix[i][j].score > max_yet:
                max_yet = matrix[i][j].score
                high_i, high_j = i, j
                
    seqX = ""
    seqY = ""
    finalScore = 0
    
    while (high_i > 0 and high_j > 0 and matrix[high_i][high_j].score > 0):
        curr_node = matrix[high_i][high_j]
        if (curr_node.direction == 0):
            return [seqX, seqY]
        elif (high_i > 0 and curr_node.direction == 2):
            seqX = seq1[high_i - 1] + seqX
            seqY = '-' + seqY
            finalScore += scoringScheme[MatchPair(seq1[high_i - 1].upper(), '-')]
            high_i = high_i - 1
        elif (high_j > 0 and curr_node.direction == 1):
            seqX = '-' + seqX
            seqY = seq2[high_j - 1] + seqY
            finalScore += scoringScheme[MatchPair('-', seq2[high_j - 1].upper())]
            high_j = high_j - 1
        elif high_i > 0 and high_j > 0 and curr_node.direction == 3:
            seqX = seq1[high_i - 1] + seqX
            seqY = seq2[high_j - 1] + seqY
            finalScore += scoringScheme[MatchPair(seq1[high_i - 1].upper(), seq2[high_j - 1].upper())]
            high_i = high_i - 1
            high_j = high_j - 1

    return (seqX, seqY, finalScore)

def maxScoreMatrix(lister):
    best = None
    bestScore = float('-inf')
    for l in lister:
        if l.score >= bestScore:
            best = l
            bestScore = l.score
    return best

def minScoreMatrix(lister):
    best = None
    bestScore = float('inf')
    for l in lister:
        if l.score <= bestScore:
            best = l
            bestScore = l.score
    return best

def makeAffineScoringTable(x, y, gapPenalty, continuedGapPenalty):
    v_matrix = list()
    e_matrix = list()
    f_matrix = list()
    g_matrix = list()
    for row in range(x):
        v_lister = list()
        e_lister = list()
        f_lister = list()
        g_lister = list()
        for col in range(y):
            if row == 0 and col == 0:
                v_lister.append(ScoreMatrix(0, 0))
                e_lister.append(ScoreMatrix(float('-inf'), 0))
                f_lister.append(ScoreMatrix(float('-inf'), 0))
                g_lister.append(float('-inf'))
            elif row == 0:
                e_lister.append(ScoreMatrix(gapPenalty + col * continuedGapPenalty, 0))
                v_lister.append(ScoreMatrix(gapPenalty + col * continuedGapPenalty, 1))
                f_lister.append(ScoreMatrix(float('-inf'), -1))
                g_lister.append(float('-inf'))
            elif col == 0:
                f_lister.append(ScoreMatrix(gapPenalty + row * continuedGapPenalty, 0))
                v_lister.append(ScoreMatrix(gapPenalty + row * continuedGapPenalty, 2))
                e_lister.append(ScoreMatrix(float('-inf'), -1))
                g_lister.append(float('-inf'))
            else:
                v_lister.append(ScoreMatrix(float('-inf'), -1))
                e_lister.append(ScoreMatrix(float('-inf'), -1))
                f_lister.append(ScoreMatrix(float('-inf'), -1))
                g_lister.append(float('-inf'))
        
        v_matrix.append(v_lister)
        f_matrix.append(f_lister)
        e_matrix.append(e_lister)
        g_matrix.append(g_lister)

    return v_matrix, e_matrix, f_matrix, g_matrix

def affineTraceback(seq1, seq2, scoringScheme, gapPenalty, continuedGapPenalty, optimization):
    v_matrix, e_matrix, f_matrix, g_matrix = makeAffineScoringTable(len(seq1) + 1, len(seq2) + 1, gapPenalty, continuedGapPenalty)
    for i in range(1, len(v_matrix)):
        for j in range(1, len(v_matrix[i])):

            if optimization == "score":
                g_matrix[i][j] = v_matrix[i - 1][j - 1].score + scoringScheme[MatchPair(seq1[i - 1].upper(), seq2[j - 1].upper())]
                
                e_matrix[i][j] = maxScoreMatrix({ScoreMatrix(e_matrix[i][j - 1].score + continuedGapPenalty, 1),
                                                 ScoreMatrix(v_matrix[i][j - 1].score + gapPenalty + continuedGapPenalty, 4)})
                
                f_matrix[i][j] = maxScoreMatrix({ScoreMatrix(f_matrix[i - 1][j].score + continuedGapPenalty, 2),
                                                 ScoreMatrix(v_matrix[i - 1][j].score + gapPenalty + continuedGapPenalty, 4)})

                v_matrix[i][j] = maxScoreMatrix({ScoreMatrix(g_matrix[i][j], 3),
                                                 ScoreMatrix(f_matrix[i][j].score, 2),
                                                 ScoreMatrix(e_matrix[i][j].score, 1)})
            else:
                g_matrix[i][j] = v_matrix[i - 1][j - 1].score + scoringScheme[MatchPair(seq1[i - 1].upper(), seq2[j - 1].upper())]
                
                e_matrix[i][j] = minScoreMatrix({ScoreMatrix(e_matrix[i][j - 1].score + continuedGapPenalty, 1),
                                                 ScoreMatrix(v_matrix[i][j - 1].score + gapPenalty + continuedGapPenalty, 4)})
                
                f_matrix[i][j] = minScoreMatrix({ScoreMatrix(f_matrix[i - 1][j].score + continuedGapPenalty, 2),
                                                 ScoreMatrix(v_matrix[i - 1][j].score + gapPenalty + continuedGapPenalty, 4)})

                v_matrix[i][j] = minScoreMatrix({ScoreMatrix(g_matrix[i][j], 3),
                                                 ScoreMatrix(f_matrix[i][j].score, 2),
                                                 ScoreMatrix(e_matrix[i][j].score, 1)})

    seqX = ""
    seqY = ""
    
    i = len(seq1)
    j = len(seq2)
    finalScore = v_matrix[i][j].score
    # backtrack

    curr_matrix = v_matrix
    while (i > 0 or j > 0):
        curr_node = v_matrix[i][j]
        if curr_node.matrix == 3:
            seqX = seq1[i - 1] + seqX
            seqY = seq2[j - 1] + seqY
            i = i - 1
            j = j - 1
        elif curr_node.matrix == 1: # e matrix
            while(e_matrix[i][j].matrix != 4 and j > 0):
                seqX = '-' + seqX
                seqY = seq2[j - 1] + seqY
                j = j - 1
            if (e_matrix[i][j].matrix == 4 and j > 0):
                seqX = '-' + seqX
                seqY = seq2[j - 1] + seqY
                j = j - 1
        else: # f matrix
            while(f_matrix[i][j].matrix != 4 and i > 0):
                seqY = '-' + seqY
                seqX = seq1[i - 1] + seqX
                i = i - 1
            if (f_matrix[i][j].matrix == 4 and i > 0):
                seqY = '-' + seqY
                seqX = seq1[i - 1] + seqX
                i = i - 1
            
    return (seqX, seqY, finalScore) 


def makeScoringTableLog(x, y, gapPenalty, logger):
    v_matrix = list()
    e_matrix = list()
    f_matrix = list()
    g_matrix = list()
    for row in range(x):
        v_lister = list()
        e_lister = list()
        f_lister = list()
        g_lister = list()
        for col in range(y):
            if row == 0 and col == 0:
                v_lister.append(ScoreMatrix(0, 0))
                e_lister.append(ScoreMatrix(float('inf'), 0))
                f_lister.append(ScoreMatrix(float('inf'), 0))
                g_lister.append(float('inf'))
            elif row == 0:
                e_lister.append(ScoreMatrix(gapPenalty + math.log(col, logger), 0))
                v_lister.append(ScoreMatrix(gapPenalty + math.log(col, logger), 1))
                f_lister.append(ScoreMatrix(float('inf'), -1))
                g_lister.append(float('inf'))
            elif col == 0:
                f_lister.append(ScoreMatrix(gapPenalty + math.log(row, logger), 0))
                v_lister.append(ScoreMatrix(gapPenalty + math.log(row, logger), 2))
                e_lister.append(ScoreMatrix(float('inf'), -1))
                g_lister.append(float('inf'))
            else:
                v_lister.append(ScoreMatrix(float('inf'), -1))
                e_lister.append(ScoreMatrix(float('inf'), -1))
                f_lister.append(ScoreMatrix(float('inf'), -1))
                g_lister.append(float('inf'))
        
        v_matrix.append(v_lister)
        f_matrix.append(f_lister)
        e_matrix.append(e_lister)
        g_matrix.append(g_lister)

    return v_matrix, e_matrix, f_matrix, g_matrix

def maxScoreMatrixlog(lister):
    best = None
    bestScore = float('-inf')
    counter = 0
    the_counter = 0
    for l in lister:
        counter+=1
        if l.score > bestScore:
            the_counter = counter
            best = l
            bestScore = l.score
    return (best, the_counter - 1)

def minScoreMatrixlog(lister):
    best = None
    bestScore = float('inf')
    counter = 0
    the_counter = 0
    for l in lister:
        counter+=1
        if l.score < bestScore:
            the_counter = counter
            best = l
            bestScore = l.score
    return (best, the_counter - 1)

def logaffinetraceback(seq1, seq2, scoringScheme, gapPenalty, optimization, logger):
    v_matrix, e_matrix, f_matrix, g_matrix =  makeScoringTableLog(len(seq1) + 1, len(seq2) + 1, gapPenalty, logger)

    for i in range(1, len(v_matrix)):
        for j in range(1, len(v_matrix[i])):

            if optimization == "score":
                g_matrix[i][j] = v_matrix[i - 1][j - 1].score + scoringScheme[MatchPair(seq1[i - 1].upper(), seq2[j - 1].upper())]

                temp = maxScoreMatrixlog(v_matrix[i][0:j])

                ftemp = list()
                for poo in range(0, i):
                    ftemp.append(v_matrix[poo][j])
                gootemp = maxScoreMatrixlog(ftemp)

                if (j - temp[1] == 1):
                    ebacker = 4
                else:
                    ebacker = 1

                if (i - gootemp[1] == 1):
                    fbacker = 4
                else:
                    fbacker = 2
                    
                e_matrix[i][j] = ScoreMatrix(temp[0].score + gapPenalty + math.log(j - temp[1], logger), ebacker)
                    

                f_matrix[i][j] = ScoreMatrix(gootemp[0].score + gapPenalty + math.log(i - gootemp[1], logger), fbacker)
                
                v_matrix[i][j] = maxScoreMatrixlog({ScoreMatrix(g_matrix[i][j], 3),
                                                 ScoreMatrix(f_matrix[i][j].score, 2),
                                                 ScoreMatrix(e_matrix[i][j].score, 1)})[0]
            else:
                g_matrix[i][j] = v_matrix[i - 1][j - 1].score + scoringScheme[MatchPair(seq1[i - 1].upper(), seq2[j - 1].upper())]

                temp = minScoreMatrixlog(v_matrix[i][0:j])

                ftemp = list()
                for poo in range(0, i):
                    ftemp.append(v_matrix[poo][j])
                gootemp = minScoreMatrixlog(ftemp)

                if (j - temp[1] == 1):
                    ebacker = 4
                else:
                    ebacker = 1

                if (i - gootemp[1] == 1):
                    fbacker = 4
                else:
                    fbacker = 2
                    
                e_matrix[i][j] = ScoreMatrix(temp[0].score + gapPenalty + math.log(j - temp[1], logger), ebacker)
                    

                f_matrix[i][j] = ScoreMatrix(gootemp[0].score + gapPenalty + math.log(i - gootemp[1], logger), fbacker)
                
                v_matrix[i][j] = minScoreMatrixlog({ScoreMatrix(g_matrix[i][j], 3),
                                                 ScoreMatrix(f_matrix[i][j].score, 2),
                                                 ScoreMatrix(e_matrix[i][j].score, 1)})[0]

    seqX = ""
    seqY = ""

    i = len(seq1)
    j = len(seq2)
    finalScore = v_matrix[i][j].score
    # backtrack

    curr_matrix = v_matrix
    while (i > 0 or j > 0):
        curr_node = v_matrix[i][j]
        if curr_node.matrix == 3:
            seqX = seq1[i - 1] + seqX
            seqY = seq2[j - 1] + seqY
            i = i - 1
            j = j - 1
        elif curr_node.matrix == 1: # e matrix
            while(e_matrix[i][j].matrix != 4 and j > 0):
                seqX = '-' + seqX
                seqY = seq2[j - 1] + seqY
                j = j - 1
            if (e_matrix[i][j].matrix == 4 and j > 0):
                seqX = '-' + seqX
                seqY = seq2[j - 1] + seqY
                j = j - 1
        else: # f matrix
            while(f_matrix[i][j].matrix != 4 and i > 0):
                seqY = '-' + seqY
                seqX = seq1[i - 1] + seqX
                i = i - 1
            if (f_matrix[i][j].matrix == 4 and i > 0):
                seqY = '-' + seqY
                seqX = seq1[i - 1] + seqX
                i = i - 1
            
    return (seqX, seqY, finalScore)

def globalalignmentrunner(seq1 : str, seq2 : str, scoringMatrix : str, gapPenalty : float, optimization : str):
    scoringScheme = openScoringMatrix(scoringMatrix, gapPenalty)
    seqX, seqY, finalScore = gbtraceback(seq1, seq2, scoringScheme, gapPenalty, optimization)
    return seqX, seqY, finalScore
    
def localalignmentrunner(seq1 : str, seq2 : str, scoringMatrix : str, gapPenalty : float):
    scoringScheme = openScoringMatrix(scoringMatrix, gapPenalty)
    seqX, seqY, finalScore = latraceback(seq1, seq2, scoringScheme)
    return seqX, seqY, finalScore

def affinealignmentrunner(seq1 : str, seq2 : str, scoringMatrix : str, gapPenalty : float, continuedPenalty, optimization : str):
    scoringScheme = openScoringMatrix(scoringMatrix, gapPenalty)
    seqX, seqY, finalScore = affineTraceback(seq1, seq2, scoringScheme, gapPenalty, continuedPenalty, optimization)
    return seqX, seqY, finalScore

def affinelogalignmentrunner(seq1 : str, seq2 : str, scoringMatrix : str, gapPenalty : float, logger, optimization : str):
    scoringScheme = openScoringMatrix(scoringMatrix, gapPenalty)
    seqX, seqY, finalScore = logaffinetraceback(seq1, seq2, scoringScheme, gapPenalty, optimization, logger)
    return seqX, seqY, finalScore
