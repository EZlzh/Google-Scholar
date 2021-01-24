import networkx as nx
import json

def load_graph(graph_file):
    G = nx.Graph()
    edges = []
    with open (graph_file, 'r') as f: 
        lines = f.readlines()
        for line in lines[1:]:
            conn = line.strip().split(' ')
            edges.append((int(conn[0]),int(conn[1])))

    # G.add_edges_from(edges)

    with open('Google_NOBE.txt','w') as f: 
        for edge in edges:
            f.write(str(edge[0]+1)+" "+str(edge[1]+1)+"\n")
            f.write(str(edge[1]+1)+" "+str(edge[0]+1)+"\n")
    
    print("graph completed!")
    # return G

if __name__ == '__main__':
    
    '''
    clear all
    load ../datasets/Google_NOBE.txt
    Google_NOBE = unique(sort(Google_NOBE,2),'rows');
    G = graph(Google_NOBE(:,1),Google_NOBE(:,2),'OmitSelfLoops');
    [U,V] =graph_embedding(G,'nb',30,'normalized');
    save -ascii ../datasets/embedding_results/Google_NOBE_nbaa.txt U

    [U,V] =graph_embedding(G,'ua',30,'normalized');
    save -ascii ../datasets/embedding_results/Google_NOBE_uaaa.txt U
    '''

    graph_file = 'Google_Scholar.txt'
    G = load_graph(graph_file)