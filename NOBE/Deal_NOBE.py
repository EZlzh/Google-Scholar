import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import json
import numpy as np
from Comp.main import *
from tqdm import tqdm

def load_NOBE(NOBE_file):
    embed = []
    with open(NOBE_file, "r") as f: 
        data = f.readlines()
        for line in data:
            str_numbers = line.split()
            numbers = []
            for number in str_numbers:
                numbers.append(float(number))
            embed.append(numbers)
    return embed

def deal_comm(partition):
    Cdic = {}
    for key in partition:
        key1 = int(key)
        value1 = partition[key]
        if value1 in Cdic:
            Cdic[value1].append(key1)
        else: 
            Cdic[value1] = []
            Cdic[value1].append(key1)
    return Cdic

def cal_U_c(Cdic, embed):
    U_c = {}
    R_c = {}
    for Ckey in Cdic:
        cur_len = len(Cdic[Ckey])
        res = np.zeros(30)
        for i in range(cur_len):
            if i == 0:
                res = np.array(embed[Cdic[Ckey][i]])
            else: 
                res = res + np.array(embed[Cdic[Ckey][i]])
        res = res/cur_len
        U_c[Ckey] = res
        res2 = 0
        for i in range(cur_len):
            res2 = res2 + np.linalg.norm(np.array(embed[Cdic[Ckey][i]]) - res)
        R_c[Ckey] = res2
    return U_c, R_c

def cal_RDS(embed, U_c, R_c, partition):
    RDS = []
    for i in tqdm(range(len(embed))):
        C_v = partition[str(i)]
        numerator = np.linalg.norm(np.array(embed[i]) - U_c[C_v]) / R_c[C_v]
        denominator = 1000000000
        for j in range(len(U_c)):
            if j == 0:
                denominator = np.linalg.norm(np.array(embed[i]) - U_c[j]) / R_c[j]
            else:
                denominator = min(denominator ,np.linalg.norm(np.array(embed[i]) - U_c[j]) / R_c[j])
        RDS.append((i, numerator / denominator))
    
    RDS = sorted(RDS, key=lambda x:x[1], reverse=True)
    return RDS

def Out_NOBE(RDS, Fi):
    with open('top4000-'+Fi+'.txt', 'w') as f: 
        for i in range(4000):
            f.write(str(i+1)+" "+str(RDS[i][0]))
            f.write("\n")

if __name__ == '__main__':
    comm_file = BASE_DIR + '/Comp/community.txt'
    partition = load_communities(comm_file)
    SHS_file = BASE_DIR + '/Comp/top4000SHS-AP_Greedy.txt'
    topk = 50
    SHS = load_SHS(SHS_file)
    # for node in SHS[:50]:
    #     print(node, partition[str(node)])
    GA = True
    if GA:
        NOBE_file = BASE_DIR + '/NOBE/Google_NOBE_uaaa.txt'
        Fi = 'NOBE_GA'
    else: 
        NOBE_file = BASE_DIR + '/NOBE/Google_NOBE_nbaa.txt'
        Fi = 'NOBE'
    embed = load_NOBE(NOBE_file)
    # print(embed[0])

    Cdic = deal_comm(partition)

    U_c, R_c = cal_U_c(Cdic, embed)
    # print(U_c[20], R_c[20])
    # print(len(embed))
    # print(len(U_c))

    RDS = cal_RDS(embed, U_c, R_c, partition)
    # print(RDS[:50])
    with open(BASE_DIR + '/NOBE/RDS_'+ Fi +'.json', 'w') as f:
        json.dump(RDS, f)

    with open(BASE_DIR + '/NOBE/RDS_'+ Fi +'.json', 'r') as f: 
        RDS = json.load(f)
    Out_NOBE(RDS, Fi)
    

