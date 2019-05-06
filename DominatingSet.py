import numpy as np
import random

def DomUpper(n, delta):
    upper_bound = n * (1 + np.log(delta + 1)) / (delta + 1)
    return upper_bound

def AdjMatrix(n, threshold = 0.5):
    A = np.zeros((n,n))
    for i in range(n):
        for j in range(i+1, n):
            A[i][j] = 1 if np.random.rand() >= threshold else 0
            A[j][i] = A[i][j] 
    return A

'''
# A typical example
Adj = np.array([[0,0,1,0,0,0,0],
                [0,0,1,0,0,0,0],
                [1,1,0,1,1,0,0],
                [0,0,1,0,0,0,0],
                [0,0,1,0,0,1,1],
                [0,0,0,0,1,0,0],
                [0,0,0,0,1,0,0]])
print(Adj)
n = 7                       # num of vertices
'''

# Initialization
n = 100                     # num of vertices
Adj = AdjMatrix(n, 0.99)    # generate adjecent matrix
V = list(np.arange(n))      # index of all the vertices
U = []                      # dominating set
W = list(set(V) - set(U))   # vertices that are not in the dominating set
Dom = []                    # vertices that have been dominated
delta = np.min(np.sum(Adj, axis = 1)) # the minimum degree
print("Adjecent matrix:")
print(Adj)

# Greedy search
while len(V) != len(Dom):
    gain = [] # how many vertices will be dominated when a vertex is added to the dominating set
    '''Search candidates:'''
    for i, index in enumerate(W):
        neighbors = list(np.array(V)[Adj[index] == 1])
        neighbors.append(index)                             # include itself
        gain.append(len(set(Dom + neighbors)))

    '''Updating:'''
    candidate = W[np.argmax(np.array(gain))]                # the vertex to add to the dominating set
    Cneighbors = list(np.array(V)[Adj[candidate] == 1])     # neighbors of the candidate
    Cneighbors.append(candidate)
    U.append(candidate)
    W = list(set(V) - set(U))
    Dom = list(set(Dom + Cneighbors))

# Compare result of greedy search and the derived upper bound
print("Result of greedy search:", len(U))
print("The derived upper bound:", DomUpper(n, delta))
