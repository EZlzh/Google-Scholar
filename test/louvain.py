import community as community_louvain
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import networkx as nx
import json

def louvain():
    G = nx.Graph()
    edges = []
    with open ('./Google_Scholar.txt', 'r') as f: 
        lines = f.readlines()
        for line in lines[1:]:
            conn = line.strip().split(' ')
            edges.append((int(conn[0]),int(conn[1])))

    G.add_edges_from(edges)
    print("Yes")
    partition = community_louvain.best_partition(G)
    return partition

if __name__ == '__main__':
    F1 = louvain()
    with open('community.txt', 'w') as f: 
        f.write(json.dumps(F1))
