# a. Implement Newman-Girvan algorithm for non-overlapping communities. The
# algorithm should receive a network and parameter k (number of communities)
# are return the communities.
import networkx as nx
import matplotlib.pyplot as plt
import itertools
from networkx.algorithms.community.centrality import girvan_newman as girvan_newman_official

def remove_edges(G):
    #num_of_components = nx.number_connected_components(G)
    betweenness = nx.edge_betweenness_centrality(G)
    bet_edges = list(betweenness.items())
    max_betweeness = max(betweenness.values())
    edges = G.edges()
    for edge in list(edges):
        if (betweenness[edge] == max_betweeness):
            G.remove_edge(*edge)
        
def newman_girvan_algorithm(G, k):
    # number of nodes is 1
    if (G.order() == 1):
        return list(G.nodes())
    num_of_components = 1
    while (num_of_components < k):
        remove_edges(G)
        communities = list(nx.connected_component_subgraphs(G))
        num_of_components = len(communities)
    return communities


with open("communities.txt") as file:
    G = nx.Graph()
    lines = [line.rstrip('\n') for line in file]
    for line in lines:
        edge = str(line).split(' ')
        G.add_edge(edge[0], edge[1])
    max_comp = max(nx.connected_component_subgraphs(G), key=len)
    com = newman_girvan_algorithm(max_comp, 3)
    print len(com)
    for i,c in enumerate(com):
        print ("Community n.%d: %s" % (i+1, c.nodes()))
        print "len:", len(c)
    print "========="
    