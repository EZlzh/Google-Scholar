
from tqdm import tqdm
import os 
import re
import json

cur = 0
cnt = 0

def extract_info(prefix, curfix, nid):
    addr = prefix + curfix
    newlines = ''
    try: 
        with open(addr, 'r', encoding='UTF-8-sig') as f:
            lines = f.readlines()
        res_lines = []
        for line in lines:
            line = line.strip()
            res_lines.append(line)
            newlines += line + '\n'
    except FileNotFoundError:
        return [str(''),str(''),str('')]
        pass
        # print(line)
    # print(res_lines[2], '\n', res_lines[4], curfix, nid)
    return [res_lines[2], res_lines[1], res_lines[0]]

def preparation():
    path = '/Users/apple/Documents/gs_info/'
    with open(path+'gs_id.txt', 'r', encoding='UTF-8-sig') as f: 
        lines = f.readlines() 
    print(' total lines in gs_id:\n%d' % len(lines))
    
    nlist = []
    id2str = {}
    str2id = {}
    
    cur = 0
    cnt = 0
    for line in lines:
        cnt += 1
        conn = line.strip().split(" ")
        idnode, strnode = int(conn[0]), conn[1]
        nlist.append((idnode, strnode))
        id2str[idnode] = strnode
        str2id[strnode] = idnode
        # node_id, node_string
        # test 
        # if cur < 10:
        #     print(idnode, strnode)
        #     cur += 1

    print(" gs_info node id:\n{}".format(nlist[-1]))
    
    id2str_first2pairs = {k: id2str[k] for k in list(id2str)[:2]}
    str2id_first2pairs = {k: str2id[k] for k in list(str2id)[:2]}
    # print(id2str_first2pairs, str2id_first2pairs)
    # print(id2str[100])
    # print(str2id['---lJ78AAAAJ.parse'])

    # for nodes 
    with open(path+'nodes.txt', 'r') as f: 
        lines = f.readlines() 

    cur = 0
    cnt = 0
    nodes = []
    for line in lines:
        conn = line.strip()
        cnt += 1
        nodes.append(int(conn))
        # if cur < 10:
        #     print(conn, type(conn))
        #     cur += 1
    print('total nodes: ', cnt)
    print('last node id:', nodes[-1])
    

    # for edges
    with open(path+'edges.txt', 'r') as f: 
        lines = f.readlines() 

    cur = 0
    cnt = 0
    edges = []
    S = set()
    for line in lines:
        conn = line.strip().split(",")
        a, b = int(conn[0]), int(conn[1])
        cnt += 1
        edges.append((a,b))
        S.add(a)
        S.add(b)
        # if cur < 10:
        #     print(a, b)
        #     cur += 1
    print('total edges:\n%d' % cnt)
    print('The total # of nodes with edges:\n%d' % len(S))
    print('OK')

    htap = '/Users/apple/Documents/gs_result/'
    files = os.listdir(htap)
    print(len(files))
    # print(files[:10])

    res = 0
    T = set()
    addrs = []
    for (na, nb) in tqdm(edges):
        if na not in T: 
            T.add(na)
            # if res < 100:
            #     addr = extract_info(htap, id2str[na], na)
            #     res += 1
            #     addrs.append(addr)
            addr = extract_info(htap, id2str[na], na)
            res += 1
            addrs.append(addr)
        if nb not in T: 
            T.add(nb)
            # if res < 100:
            #     addr = extract_info(htap, id2str[nb], nb)
            #     res += 1
            #     addrs.append(addr)
            addr = extract_info(htap, id2str[nb], nb)
            res += 1
            addrs.append(addr)
    print(len(T))

    words = [w[2] for w in tqdm(addrs) if re.match(".*tsinghua.*", w[0].lower())]
    
    print(len(words))

    # words = [w[2] for w in tqdm(addrs) if re.match(".*(Pan Hui|Xiaoming Fu).*", w[1])]
    # for word in words[:2]:
    #     print(word)
    # print(len(words))
    # print(words)
    return words

if __name__ == '__main__':
    a = preparation()
    filename = 'thu_net.json'
    with open(filename, 'w') as f:
        json.dump(a, f)
    
