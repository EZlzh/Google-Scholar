
import tqdm
import os

if __name__ == '__main__':
    path = '/Users/apple/Documents/gs_info/'
    with open(path+'gs_id.txt', 'r') as f: 
        lines = f.readlines() 
    
    id2str = {}
    str2id = {}
    for line in lines:
        conn = line.strip().split(" ")
        idnode, strnode = int(conn[0]), conn[1]
        id2str[idnode] = strnode
        str2id[strnode] = idnode

    print('OK')