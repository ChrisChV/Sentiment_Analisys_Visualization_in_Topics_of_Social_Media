import community
import networkx as nx
import matplotlib.pyplot as plt

#better with karate_graph() as defined in networkx example.
#erdos renyi don't have true community structure
#G = nx.erdos_renyi_graph(30, 0.05)

#print type(G)

#print G
#G=nx.erdos_renyi_graph(1000, 0.01)

G = community.load_binary("graph2.bin")

#first compute the best partition
partition = community.best_partition(G)

#drawing
size = float(len(set(partition.values())))
pos = nx.spring_layout(G)
count = 0.
for com in set(partition.values()):
    count = count + 1.
    list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
    nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 5,
                                node_color = str(count / size))

""""
dendrogram = community.generate_dendrogram(G)
for level in range(len(dendrogram) - 1) :
    print("partition at level", level, "is", community.partition_at_level(dendrogram, level))


print level

partition = dendrogram[0].copy()
for index in range(1, level + 1):
    for node, community in partition.items():
        partition[node] = dendrogram[index][community]
	print community

print partition
"""


nx.draw_networkx_edges(G, pos, alpha=0.5)
plt.show()