# a. Implement Newman-Girvan algorithm for non-overlapping communities. The
# algorithm should receive a network and parameter k (number of communities)
# are return the communities.
import networkx as nx
import matplotlib.pyplot as plt


def remove_edge(G):
    #num_of_components = nx.number_connected_components(G)
    #while (nx.number_connected_components(G) <= num_of_components):
    betweenness = nx.edge_betweenness_centrality(G, weight='weight')
    max_betweeness = max(betweenness.values())
    edges = G.edges()
    for edge in list(edges):
        if (betweenness[edge] == max_betweeness):
            G.remove_edge(*edge)
        
def newman_girvan_algorithm(network, k):
    # number of nodes is 1
    if (network.order() == 1):
        return list(network.nodes())
    # until no edges left - 
    result = []
    num_of_components = 1
    while (num_of_components < k):
        remove_edge(G)
        num_of_components = nx.number_connected_components(G)
    components = list(nx.connected_component_subgraphs(G))
    for c in components:
        nodes = []
        for node in c.nodes():
            nodes.append(node)
        print nodes
        result.append(nodes)
    return result

with open("communities.txt") as file:
    G = nx.Graph()
    lines = [line.rstrip('\n') for line in file]
    for line in lines:
        edge = str(line).split(' ')
        G.add_edge(edge[0], edge[1])
    com = newman_girvan_algorithm(G, 3)
    print type(com)
    for i, c in enumerate(com):
        print ("Community n.%d: %s" % (i+1, c))
