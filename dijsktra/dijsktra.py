import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

"""get and visualize the shortest path in a 15 nodes network """

g= nx.Graph()
for i in range(15):
    g.add_edge(i,np.random.randint(1,13),weight=np.random.randint(20,30))
    g.add_edge(i,np.random.randint(2,13),weight=np.random.randint(1,30))
    g.add_edge(i,np.random.randint(3,12),weight=np.random.randint(1,40))
pos = nx.spring_layout(g)

nx.draw(g,with_labels=True,node_color='skyblue',node_shape='s',alpha=0.8)
dijsk = nx.shortest_path(g,source=0,target=14)
plt.show()

print("shortest path is",dijsk)
print(nx.get_edge_attributes(g,'weight'))
print(nx.shortest_path(g, source=0, weight='weight'))