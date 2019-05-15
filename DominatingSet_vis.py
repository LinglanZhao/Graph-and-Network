import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

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

# A typical example
'''
Adj = np.array([[0,0,1,0,0,0,0],
                [0,0,1,0,0,0,0],
                [1,1,0,1,1,0,0],
                [0,0,1,0,0,0,0],
                [0,0,1,0,0,1,1],
                [0,0,0,0,1,0,0],
                [0,0,0,0,1,0,0]])
n = 7                       # num of vertices
'''

# Initialization
n = 20                      # num of vertices
Adj = AdjMatrix(n, 0.8)     # generate adjacent matrix
V = list(np.arange(n))      # index of all the vertices
U = []                      # dominating set
W = list(set(V) - set(U))   # vertices that are not in the dominating set
Dom = []                    # vertices that have been dominated
delta = np.min(np.sum(Adj, axis = 1)) # the minimum degree
print("Adjacent matrix:")
print(Adj)

# Visualization
Position = np.random.rand(n, 2)
plt.figure(1)
plt.xlabel('x_1')
plt.ylabel('x_2')
plt.title('The Input Graph')
for edge in combinations(range(n), 2):
    i, j = edge
    if Adj[i][j] == 1:
        plt.plot([Position[i][0], Position[j][0]], [Position[i][1], Position[j][1]], color='cyan')
plt.scatter(Position[:, 0], Position[:, 1], marker="o", color='black', s=50)
plt.show()

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

plt.figure(2)
plt.xlabel('x_1')
plt.ylabel('x_2')
plt.title('Visualization of Dominating Set (colored in red)')
for edge in combinations(range(n), 2):
    i, j = edge
    if Adj[i][j] == 1:
        plt.plot([Position[i][0], Position[j][0]], [Position[i][1], Position[j][1]], color='cyan')
plt.scatter(Position[U, 0], Position[U, 1], marker="o", color='red', s=100)
plt.scatter(Position[W, 0], Position[W, 1], marker="o", color='green', s=50)
plt.show()