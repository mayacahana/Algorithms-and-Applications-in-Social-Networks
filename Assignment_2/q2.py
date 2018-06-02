# Implement k-clique communities detection algorithm. The algorithm should
# receive a network and parameter k (size of clique) are return the communities.
# Implement k-clique communities detection algorithm. The algorithm should
# receive a network and parameter k (size of clique) are return the communities.
import networkx as nx
import itertools
from networkx.algorithms.community import k_clique_communities as k_clique_communities_official

def initArray(n):
    array = []
    for i in range (0, n):
        array.append(0)
    return array

def k_clique_communities(G, k):
    cliques = list(nx.find_cliques(G))
    num_of_cliques = len(cliques)
    matrix = []
    for clique_i in cliques:
        col = 0
        matrix_row = initArray(num_of_cliques)
        for clique_j in cliques:
            sharedNodes = 0
            for node_i in clique_i:
                for node_j in clique_j:
                    if node_i == node_j :
                        sharedNodes += 1
            matrix_row[col] = sharedNodes
            col += 1
        matrix.append(matrix_row)
    
    # threshold the matrix
    thresh_matrix = []
    for i in range (0, num_of_cliques):
        thresh_row = []
        for j in range (0, num_of_cliques):
            if i == j:
                if matrix[i][j] >= k:
                    thresh_row.append(1)
                else:
                    thresh_row.append(0)
            else:
                if matrix[i][j] >= k-1:
                    thresh_row.append(1)
                else:
                    thresh_row.append(0)
        thresh_matrix.append(thresh_row)

    
    #get graph of cliques from thresh_matrix
    N=nx.Graph()
    for row in range(0,num_of_cliques):
        for col in range(0,num_of_cliques):
            if thresh_matrix[row][col] == 1:
                N.add_edge(row,col)
     
    communities_of_nodes = []
    con_components = nx.connected_components(N)            
    for comp in con_components:
        newSet = set()
        for index in comp:
            for node in cliques[index]:
                newSet.add(node)
        communities_of_nodes.append(newSet)
    return (communities_of_nodes)

with open("communities_q2.txt") as file:
    G = nx.Graph()
    lines = [line.rstrip('\n') for line in file]
    for line in lines:
        edge = str(line).split(' ')
        G.add_edge(edge[0], edge[1])
    print "================"
    max_comp = max(nx.connected_component_subgraphs(G), key=len)
    com = k_clique_communities(max_comp, 3)
    for i, c in enumerate(com):
        print ("Community n.%d: %s" % (i+1, list(c)))
    com_official = list(k_clique_communities_official(max_comp, 3))
    for i, c in enumerate(com_official):
        print ("Official Community n.%d: %s" % (i+1, list(c)))