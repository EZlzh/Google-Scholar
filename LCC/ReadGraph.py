import networkx as nx




def Read_Graph():
    G = nx.Graph()
    edges = []
    with open ('./Google_Scholar.txt', 'r') as f: 
        lines = f.readlines()
        for line in lines[1:]:
            conn = line.strip().split(' ')
            edges.append((int(conn[0]),int(conn[1])))

    G.add_edges_from(edges)
    return G

if __name__ == '__main__':
    G = Read_Graph()
    print(G.number_of_nodes())