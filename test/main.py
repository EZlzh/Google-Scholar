import networkx as nx
import json

def load_communities(comm):
    with open(comm, 'r') as f: 
        partition = json.load(f)
    print("communities completed!")
    return partition

def load_graph(graph_file):
    G = nx.Graph()
    edges = []
    with open (graph_file, 'r') as f: 
        lines = f.readlines()
        for line in lines[1:]:
            conn = line.strip().split(' ')
            edges.append((int(conn[0]),int(conn[1])))

    G.add_edges_from(edges)
    print("graph completed!")
    return G

def load_SHS(SHS_file):
    SHS = []
    with open (SHS_file, 'r') as f: 
        lines = f.readlines()
        for line in lines:
            conn = line.strip().split(' ')
            # SHS.append((int(conn[0]),int(conn[1])))
            SHS.append(int(conn[1]))
    print("SHS completed!")
    print(SHS[:10])
    return SHS

def cal_community_size(partition):
    com_size = {}
    for key in partition:
        cur = partition[key]
        if cur in com_size:
            com_size[cur] += 1
        else: 
            com_size[cur] = 1
    return com_size

def cal_spanned_communities(SHS, partition, com_size, G):
    res = []
    sum_res = []
    S = set()
    for i in SHS[:100]:
        # print("%d-th neighbors: " % i)
        for j in G.neighbors(i):
            # print(j)
            S.add(partition[str(j)])
        res.append(len(S))
        cnt = 0
        for j in S:
            cnt += com_size[j]
        sum_res.append(cnt)
    return res, sum_res

if __name__ == '__main__':

    comm_file = 'community.txt'
    partition = load_communities(comm_file)
    
    com_size = cal_community_size(partition)
    # print(len(com_size))

    SHS_file = 'top4000_AP_SHS.txt'
    SHS = load_SHS(SHS_file)

    graph_file = 'Google_Scholar.txt'
    G = load_graph(graph_file)

    res_num_spanned, res_sum_spanned = cal_spanned_communities(SHS, partition, com_size, G)
    print(res_num_spanned)
    print(res_sum_spanned)

    