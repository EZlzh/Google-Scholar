import networkx as nx
import json
import scipy.io as sio 

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
    # print("graph completed!")
    return G

def load_SHS(SHS_file):
    SHS = []
    with open (SHS_file, 'r') as f: 
        lines = f.readlines()
        for line in lines:
            conn = line.strip().split(' ')
            # SHS.append((int(conn[0]),int(conn[1])))
            SHS.append(int(conn[1]))
    # print("SHS completed!")
    # print(SHS[:10])
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

def cal_property(SHS_file):
    Adic  = {}

    klist = []
    for i in range(100):
        klist.append(i+1)
    Adic['k_nodes'] = klist

    for SHS_file in SHS_files:
        SHS = []
        cur_name = SHS_file.split('.')[0].split('-')[1]
        print(cur_name)
        SHS = load_SHS(SHS_file)
        res_num_spanned, res_sum_spanned = cal_spanned_communities(SHS, partition, com_size, G)
        avg_size = [res_sum_spanned[i] / res_num_spanned[i] for i in range(len(res_num_spanned))]
        Adic[str(cur_name+'_number_community_spanned')] = res_num_spanned
        Adic[str(cur_name+'_number_sizes_spanned')] = res_sum_spanned
        Adic[str(cur_name+'_avg_community_size')] = avg_size
        print(res_num_spanned)
        print(res_sum_spanned)
        print(avg_size)
    
    for key in Adic:
        print(key)

    sio.savemat('./Metrics-test0.mat', Adic)

if __name__ == '__main__':
    # run in current directory.
    comm_file = 'community.txt'
    partition = load_communities(comm_file)
    
    com_size = cal_community_size(partition)
    # print(len(com_size))

    

    graph_file = 'Google_Scholar.txt'
    G = load_graph(graph_file)


    SHS_files = ['top4000SHS-AP_Greedy.txt', 'top4000SHS-AP_BICC.txt', 
        'top4000-maxClosenessCentrality.txt', 'top4000-two_Step.txt', 'top4000-Pagerank.txt',
        'top4000-HIS.txt', 'top4000-pathCount.txt', 'top4000-Constraint.txt', 'top4000-MaxD.txt', 
        'top4000-NOBE.txt', 'top4000-NOBE_GA.txt'
        ]
    cal_property(SHS_files)

    

    