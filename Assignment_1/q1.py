import networkx as nx
import random
import matplotlib.pyplot as plt

def erdos_renyi_model(n,p):
    graph = nx.Graph()
    nodes = list(i for i in range(0,n))
    for node in nodes:
        graph.add_node(node)
        for n in nodes:
            rand = random.uniform(0, 1)
            if (rand <= p) and (node > n):
                graph.add_edge(node, n)
    return graph

# graph = erdos_renyi_model(10,0.5)
# nx.draw(graph, with_labels=True, node_size=1000, node_color="skyblue")
# plt.show()
          


# ## Question 1. b

# In[29]:


def small_world_model(n,k,p):
    G = nx.Graph()
    nodes = list(i for i in range(0,n))
    for node in nodes:
        G.add_node(node)
        for i in range(0, int(k/2+1)):
            G.add_edge(node, (node+i)%n)
            G.add_edge(node, (node-i)%n)
    edges = G.edges()
    for edge in list(edges):
        if (edge[0] < edge[1]):
            rand = random.uniform(0, 1)
            if rand <= p:
                G.remove_edge(edge[0], edge[1])
                new_node = random.randint(0,n)
                G.add_edge(edge[0], new_node)
    return G

# G = small_world_model(40,2,0.6)
# plt.figure(3,figsize=(10,10))
# pos = nx.circular_layout(G)
# nx.draw(G, pos, with_labels=True, node_size=1000, node_color="skyblue", font_size=15)
# plt.show()
    


# ## Question 1. c

# In[ ]:


def node_clustering_coefficient(G,node):
    neighbors = G.neighbors(node)
    neighbors = list(neighbors)
    edges_between_neighbors = 0
    clustering_coefficient = 0
    # count edges between neighbors
    edges = G.edges()
    for edge in list(edges):
        if (edge[0] in neighbors and edge[1] in neighbors):
            edges_between_neighbors += 1
    degree = G.degree(node)
    if (degree <= 1):
        return clustering_coefficient
    clustering_coefficient = (2 * (float(edges_between_neighbors)))/(degree*(degree-1))
    return clustering_coefficient
            
    
def graph_clustering_coefficient(G):
    sum_clustering_coefficient = 0
    for node in G.nodes():
        sum_clustering_coefficient += node_clustering_coefficient(G,node)
    return sum_clustering_coefficient/G.number_of_nodes()

def calculate_diameter(G):
    diameter = 0
    if not nx.is_connected(G):
        sub_graphs = [G.subgraph(x) for x in nx.connected_components(G)]
        for component in sub_graphs:
            diameter = max(nx.algorithms.distance_measures.diameter(component), diameter)
    else:
        diameter = nx.algorithms.distance_measures.diameter(G)
    return diameter

erdos_renyi_g = erdos_renyi_model(1000, 0.2)
small_world_g = small_world_model(1000, 8, 0.2)
print "Erdos Renyi graph diameter is: ", calculate_diameter(erdos_renyi_g)
print "Erdos Renyi graph clustering coefficient is: ", graph_clustering_coefficient(erdos_renyi_g)
print "Small world graph diameter is: ", calculate_diameter(small_world_g)
print "Small world graph clustering coefficient is:", graph_clustering_coefficient(small_world_g)

degree_dist_er = {}
avg_degree_er = 0
for node in erdos_renyi_g.nodes():
    node_degree = len(erdos_renyi_g.neighbors(node))
    if node_degree not in degree_dist_er:
        degree_dist_er[node_degree] = 0
    degree_dist_er[node_degree] += 1
    avg_degree_er += node_degree
#avg_degree_er = avg_degree_er/1000

plt.bar(list(degree_dist_er.keys()), degree_dist_er.values(), color='r')

degree_dist_sm = {}
avg_degree_sm = 0
for node in small_world_g.nodes():
    node_degree = len(small_world_g.neighbors(node))
    if node_degree not in degree_dist_sm:
        degree_dist_sm[node_degree] = 0
    degree_dist_sm[node_degree] += 1
    avg_degree_sm += node_degree
#avg_degree_sm = avg_degree_sm/N


plt.bar(list(degree_dist_sm.keys()), degree_dist_sm.values(), color='g')
plt.show()

nx.draw(erdos_renyi_g)
nx.draw(small_world_g)

