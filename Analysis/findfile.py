from tqdm import tqdm
import os 
import sys
import re
import json
import random
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

remote_path = '/Users/apple/Documents/gs_info/'
dic_suffix = 'Dictnode.txt'
file_suffix = 'gs_id.txt'
Dicfile = remote_path + dic_suffix
Transfile = remote_path + file_suffix


LCC2Node = {}
Node2Str = {}

def gen_random(file):
    nodes = []
    with open(file, 'r') as f: 
        lines = f.readlines()
        for line in lines:
            conn = line.strip().split(' ')
            nodes.append((int(conn[0]),int(conn[1])))
            LCC2Node[int(conn[1])] = int(conn[0])
            # conn[1]: LCC_node_id; 
            # conn[0]: Origin_node_id;
    
    Arandom = random.sample(nodes, 4000)
    with open(BASE_DIR + '/Comp/' + 'top4000-random.txt', 'w') as f: 
        for i in range(len(Arandom)):
            f.write(str(i+1)+" "+str(Arandom[i][1])+"\n")
    return 

def gen_node2file():
    with open(Transfile, 'r') as f: 
        lines = f.readlines() 
        for line in lines:
            conn = line.strip().split(" ")
            Node2Str[int(conn[0])] = conn[1]

def transfer_node(file):
    # print(file)
    Orinodes = []
    with open(file, 'r') as f: 
        lines = f.readlines()
        for line in lines:
            conn = line.strip().split(' ')
            Orinodes.append(LCC2Node[int(conn[1])])
    # print(Orinodes[:10])
    return Orinodes

def transfer_file(nodes):
    Orifiles = []
    for node in nodes:
        Orifiles.append(Node2Str[node])
    return Orifiles

def findafile(SHS_file):
    Orinodes = transfer_node(SHS_file)
    Orifiles = transfer_file(Orinodes)
    return Orifiles

def prefind():
    gen_random(Dicfile)
    gen_node2file()

def findfiles():
    prefind()
    list_suffix = ['top4000SHS-AP_Greedy.txt', 'top4000-Pagerank.txt', 'top4000-randomT.txt']
    for suffix in list_suffix:
        SHS_file = BASE_DIR + '/Comp/' + suffix
        Orifiles = findafile(SHS_file)
        # print(Orifiles[:20])

if __name__ == '__main__':

    # SHS_suffix = 'top4000SHS-AP_Greedy.txt'
    # SHS_file = BASE_DIR + '/Comp/' + SHS_suffix
    # print(SHS_file)
    
    findfiles()

    
    