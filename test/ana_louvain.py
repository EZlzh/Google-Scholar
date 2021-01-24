import community as community_louvain
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import networkx as nx
import json

def ana_louvain():
    G = nx.Graph()
    edges = []
    with open ('./Google_Scholar.txt', 'r') as f: 
        lines = f.readlines()
        for line in lines[1:]:
            conn = line.strip().split(' ')
            edges.append((int(conn[0]),int(conn[1])))

    G.add_edges_from(edges)
    print("Yes")

    with open('community.txt', 'r') as f: 
        partition = json.load(f)

    # draw the graph
    pos = nx.spring_layout(G)
    # color the nodes according to their partition
    cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
    nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=40,
                        cmap=cmap, node_color=list(partition.values()))
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    plt.show()

if __name__ == '__main__':
    ana_louvain()
    # 191 communities in total.