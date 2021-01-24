from tqdm import tqdm
import os 
import re
from ast import literal_eval
import networkx as nx 
import matplotlib.pyplot as plt
import preparation
import json

cur_year = 2021
errr = 0
good = 0

def extract_info(prefix, curfix):
    global good
    addr = prefix + curfix
    try: 
        with open(addr, 'r') as f:
            lines = f.readlines()
        res_lines = []
        for line in lines:
            line = line.strip()
            res_lines.append(line)
        good += 1
    except FileNotFoundError:
        return [str(''),str(''),str('')]
        # print(line)
    # print(res_lines[2], '\n', res_lines[4], curfix, nid)
    return res_lines

def find_earliest_year(set_papers, addr):
    year = 2021
    if len(addr) > 12:
        for paper in addr[12:]:
            new_list = literal_eval(paper)
            if re.match('\d{4}', new_list[-1]):
                if new_list[1] in set_papers:
                    year = min(year, int(new_list[-1]))
    else: 
        pass
    return year

cur = 0
edges = []

def extract_dynamic_ca(str1):
    htap = '/Users/apple/Documents/gs_result/'
    global cur
    global edges
    res = 0
    alters = []
    if str1 == 'ego':
        Chen = 'O6tge4UAAAAJ.parse'
        # addr[8] is the list of co-authors; starting from addr[12] can cal the papers.
        addr = extract_info(htap, Chen)
        ego_papers = []
        set_papers = set()
        print('total papers: ',len(addr)-12)
        if len(addr) > 8:
            new_dict = literal_eval(addr[8])
            print('total co-authors:', len(new_dict))
            # print(new_dict)
            nodes = [new_dict[key] for key in new_dict]
        if len(addr) > 12:
            # print(addr[12])
            for paper in addr[12:]:
                new_list = literal_eval(paper)
                ego_papers.append(new_list)
                # print(new_list)
                if re.match('\d{4}', new_list[-1]):
                    cur += 1
                    # print(new_list[1], new_list[-1])
                    set_papers.add(new_list[1])
                    # print(new_list)
        print('papers with year:', cur)
        
        ego = addr[1]
        nodes.append(ego)
        print(ego)
        alters = []
        for key in new_dict:
            # print(key, new_dict[key])
            addr = extract_info(htap, key+'.parse')
            year = find_earliest_year(set_papers, addr)
            if year != 2021:
                res += 1
                # print(ego,'and',new_dict[key], key, "'s co-authorship begin from",year)
                edges.append([ego, new_dict[key], year])
                alters.append(key)
        
        print('co-author with first year:', res)
        print('co-author with gs_result files:', good)
        print(alters)
    else:
        # filename = 'thu_net.json'
        # with open(filename, 'r') as f: 

        alters = preparation.preparation()
    
    #print(alters)
    for i in range(len(alters)):
        key1 = alters[i]
        addr = extract_info(htap, key1+'.parse')
        name1 = addr[1]
        alter1_papers = set()
        if len(addr) > 12:
            # print(addr[12])
            for paper in addr[12:]:
                new_list = literal_eval(paper)
                # print(new_list)
                if re.match('\d{4}', new_list[-1]):
                    cur += 1
                    # print(new_list[1], new_list[-1])
                    alter1_papers.add(new_list[1])
        for j in range(i+1, len(alters)):
            key = alters[j]
            addr = extract_info(htap, key+'.parse')
            name2 = addr[1]
            year = find_earliest_year(alter1_papers, addr)
            if year != 2021:
                res += 1
                # print(new_dict[key1],'and',new_dict[key], key, "'s co-authorship begin from",year)
                edges.append([name1, name2, year])
                # edges.append([new_dict[key1], new_dict[key], year])
    print('# of eges in ego network:', res)
    edges = sorted(edges, key=lambda x: x[2])
    
    print(len(edges))
    # print(len(nodes))
    # print(nodes)

    for edge in edges:
        print(edge)
    
    # networkx visualization is a total piece of shit...
    G = nx.Graph()
    graph_cur = 0
    # G.add_nodes_from([(node,{'name': node}) for node in nodes])
    year = edges[0][2]
    for edge in edges:
        cur_year = edge[2]
        if cur_year != year:
            year = cur_year
            edge_labels = nx.get_edge_attributes(G, 'year')
            # edge_labels = nx.get_edge_attributes(G, 'year')
            # nx.write_gexf(G, "test"+str(graph_cur)+".gexf")
            graph_cur += 1
            pos = nx.spiral_layout(G)
            nx.draw(G, pos, node_color = 'yellow', edge_color = 'brown', with_labels = True, font_size =8, node_size =10)
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
            plt.show()
        G.add_edge(edge[0], edge[1], year=str(edge[2]))

if __name__ == '__main__':
    extract_dynamic_ca('net')