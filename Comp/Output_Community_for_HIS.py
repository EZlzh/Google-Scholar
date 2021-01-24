import networkx as nx
import json
import scipy.io as sio 

def load_communities(comm):
    with open(comm, 'r') as f: 
        partition = json.load(f)
    print("communities completed!")
    return partition


if __name__ == '__main__':
    
    comm_file = 'community.txt'
    partition = load_communities(comm_file)
    Dic_len = len(partition)
    print(Dic_len)
    
    Alist = []
    for i in range(Dic_len):
        Alist.append(partition[str(i)])
    
    with open("Google_community.txt", "w") as f: 
        for i in range(Dic_len):
            f.write(str(Alist[i]+1))
            f.write('\n')
    print("Alist append completed!")