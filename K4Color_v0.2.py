import numpy as np
from scipy.special import comb
from itertools import combinations

def ExpWeight(ColorMat,edge_c):
    # compute the conditional expectations
    E = 0
    n, n1 = ColorMat.shape
    assert n == n1
    # loop over all K4s
    for K4 in combinations(range(n), 4):
        if set(edge_c) < set(K4):
            indicator = 0       # define the indicator variable
            numW, numB, numN = 0, 0, 0
            for edge in combinations(list(K4), 2):
                i, j = edge
                if ColorMat[i, j] == 1:
                    numW += 1
                elif ColorMat[i, j] == -1:
                    numB += 1
                else:
                    numN += 1
            assert (numW + numB + numN) == 6

            if (numW != 0) & (numB != 0):
                indicator = 0
            elif (numW == 0) & (numB == 0):
                indicator = (2.0)**(-5)
            else:
                indicator = (2.0)**(-1 * numN)

            E = E + indicator
    return E

def Count_K4(ColorMat):
    # count the number of K4
    cnt = 0
    n, n1 = ColorMat.shape
    assert n == n1
    for K4 in combinations(range(n), 4):
        numW, numB, numN = 0, 0, 0
        for edge in combinations(list(K4), 2):
            i, j = edge
            if ColorMat[i, j] == 1:
                numW += 1
            elif ColorMat[i, j] == -1:
                numB += 1
            else:
                numN += 1
        assert (numW + numB + numN) == 6
        if (numW == 6) | (numB == 6):
            cnt += 1
    return cnt
            
# Initialization
n = 20                              # num of vertices
ColorMat = np.zeros((n,n))          # the matrix to denote the color strategy. 0:not colored; 1:white; -1:black
numExp = comb(n, 4) * (2**(-5))     # the expectation of the number of K4
E_prev = numExp                     # examine if E_prev == (Ew + Eb) / 2

for num, edge in enumerate(combinations(range(n), 2)):
    if (num+1) % 20 == 0:
        print('Number of colored edges:', num+1)
    i, j = edge
    # try if colored white
    ColortempW = np.copy(ColorMat)
    ColortempW[i,j] = 1
    ColortempW[j,i] = 1
    Ew = ExpWeight(ColortempW) # compute the expectaion conditioned on that edge is colored white
    # try if colored black
    ColortempB = np.copy(ColorMat)
    ColortempB[i,j] = -1
    ColortempB[j,i] = -1
    Eb = ExpWeight(ColortempB) # compute the expectaion conditioned on that edge is colored black
    # De-randomization
    ColorMat = ColortempW if (Ew <= Eb) else ColortempB
#     assert E_prev == (Ew + Eb) / 2
    E_prev = min(Ew, Eb)

print('===========================================')
print('The number of the vertices:', n)
print('The number of K4:', int(comb(n, 4)))
print('The number of K4 of same colored edges after de-randomization:', Count_K4(ColorMat))
print("The derived expectation number of K4 of same colored edges:", int(numExp))
print('===========================================')
