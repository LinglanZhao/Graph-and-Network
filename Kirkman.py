import numpy as np
from random import sample, random

def collapse(K):
    '''Compute the loss function of the optimization problem'''
    m, n = np.shape(K)
    C = []
    for i in range(n):          # index of the girl
        c = []
        for j in range(m):      # index of the week
            pos = list(K[j]).index(i)
            mod = pos//3
            c = c + list(K[j])[mod*3: (mod+1)*3]
        C.append(c)             # C[i] contains the neighbors of the ith girl (including herself) for all the weeks
    C = np.array(C)
    Obj = []
    for i in range(n):
        Obj.append(n - len(set(C[i])))
    Obj = sum(Obj)
    return(Obj)

def h_N(x):
    '''Randomized neighborhood search for Hill Climbing'''
    x1 = np.copy(x)
    c = 0
    m, n = np.shape(K)
    k = sample(list(range(m)), 1)[0]
    i,j = sample(list(range(n)), 2)
    c = x1[k][i]
    x1[k][i] = x1[k][j]
    x1[k][j] = c
    if collapse(x1) < collapse(x):
        return x1
    else:
        return []

def h_anneling(x, T):
    '''Randomized neighborhood search for Simulated Annealing'''
    x1 = np.copy(x)
    c = 0
    m, n = np.shape(K)
    k = sample(list(range(m)), 1)[0]
    i, j = sample(list(range(n)), 2)
    c = x1[k][i]
    x1[k][i] = x1[k][j]
    x1[k][j] = c
    Ly = collapse(x1)
    Lx = collapse(x)
    threshold = np.exp((Lx-Ly)/T)
    if (Ly <= Lx) | (random() <= threshold):
        return x1
    else:
        return []


'''Initialization'''
n = 15                    # number of the schoolgirls
weeks = (n-1)//2          # number of the weeks
K = np.array([sample(list(range(n)), n) for i in range(weeks)]) # random initialization
print('Initial Point:')
print(K)

'''HEURISTIC SEARCH'''
x = K
Obj = collapse(x)
print('-current loss:', Obj)

'''Hill-Climbing'''
'''
while Obj != 0:
    y = h_N(x)
    if y != []:
        x = y
        Obj = collapse(x)
        print('-current loss:', Obj)
'''

'''Simulated Annealing'''
T = 5
alph = 0.999
while Obj != 0:
    y = h_anneling(x, T)
    if y != []:
        x = y
        Obj = collapse(x)
        print('-current loss:', Obj)
    T = T * alph
print('Optimal Solution:')
print(x)
