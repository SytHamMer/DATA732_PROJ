import networkx as nx
matrix = [
    [0, 1, 0, 1],
    [1, 0, 1, 0],
    [0, 1, 0, 1],
    [1, 0, 1, 0]
]

# Créez un graphe à partir de la matrice carrée
G = nx.Graph()
for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        if matrix[i][j] == 1:
            G.add_edge(i, j)

# Vous pouvez ajouter des attributs aux nœuds ou aux arêtes si nécessaire
# nx.set_node_attributes(G, node_attributes)
# nx.set_edge_attributes(G, edge_attributes)

# Enregistrez le graphe au format GML pour une utilisation ultérieure avec Gephi
nx.write_gml(G, "graph.gml")