import numpy as np
import copy

def has_negative_cycle(graph):
    V = len(graph)
    for i in range(V):
        if graph[i][i] < 0:
            return True
    return False

def matrix_multiplication(graph):
    # Get the number of vertices in the graph
    V = len(graph)
    
    # Initialize the distance matrix with the same values as the graph
    dist = [row[:] for row in graph]
    dist_copied = copy.deepcopy(dist)

    for i in range(V):
        choosen_row = dist[i]
        for k in range(V):
            choosen_column = []
            for row in dist:
                choosen_column.append(row[k])
        
            for c_val, r_val in zip(choosen_column, choosen_row):
                if dist[i][k] > c_val + r_val:
                    dist_copied[i][k] = c_val + r_val
    
    return dist_copied

# Example usage:
INF = float('inf')
graph = [
    [0, 3, 5, 2],
    [1, 0, -2, 4],
    [-3, 5, 0, 6],
    [1, 2, -1, 0]
]

while not has_negative_cycle(graph):
    graph = matrix_multiplication(graph)


print(np.array(graph))
