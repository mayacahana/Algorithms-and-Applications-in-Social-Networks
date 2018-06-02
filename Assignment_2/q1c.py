import community 
import networkx as nx

def generate_dendogram(graph, part_init = None) :
    """Find communities in the graph and return the associated dendogram
    A dendogram is a tree and each level is a partition of the graph nodes.  Level 0 is the first partition, which contains the smallest communities, and the best is len(dendogram) - 1. The higher the level is, the bigger are the communities
    Parameters
    ----------
    graph : networkx.Graph
        the networkx graph which will be decomposed
    part_init : dict, optionnal
        the algorithm will start using this partition of the nodes. It's a dictionary where keys are their nodes and values the communities
    Returns
    -------
    dendogram : list of dictionaries
        a list of partitions, ie dictionnaries where keys of the i+1 are the values of the i. and where keys of the first are the nodes of graph
    
    Raises
    ------
    TypeError
        If the graph is not a networkx.Graph
    See Also
    --------
    best_partition
    Notes
    -----
    Uses Louvain algorithm
    References
    ----------
    .. 1. Blondel, V.D. et al. Fast unfolding of communities in large networks. J. Stat. Mech 10008, 1-12(2008).
    Examples
    --------
    >>> G=nx.erdos_renyi_graph(100, 0.01)
    >>> dendo = generate_dendogram(G)
    >>> for level in range(len(dendo) - 1) :
    >>>     print "partition at level", level, "is", partition_at_level(dendo, level)
    """
    if type(graph) != nx.Graph :
        raise TypeError("Bad graph type, use only non directed graph")
    current_graph = graph.copy()
    status = Status()
    status.init(current_graph, part_init)
    mod = __modularity(status)
    status_list = list()
    __one_level(current_graph, status)
    new_mod = __modularity(status)
    partition = __renumber(status.node2com)
    status_list.append(partition)
    mod = new_mod
    current_graph = induced_graph(partition, current_graph)
    status.init(current_graph)
    
    while True :
        __one_level(current_graph, status)
        new_mod = __modularity(status)
        if new_mod - mod < __MIN :
            break
        partition = __renumber(status.node2com)
        status_list.append(partition)
        mod = new_mod
        current_graph = induced_graph(partition, current_graph)
        status.init(current_graph)
    return status_list[:]


G = nx.Graph()
for i in range(1,7):
    G.add_node(i)
print G.nodes()
G.add_edge(1,2, weight = 2)
G.add_edge(1,5, weight = 3)
G.add_edge(5,2, weight = 2.5)
G.add_edge(3,2, weight = 3.5)
G.add_edge(3,4, weight = 3.5)
G.add_edge(4,5, weight = 5.5)
G.add_edge(4,6, weight = 5)
dendo = generate_dendogram(G)
print dendo

