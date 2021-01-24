import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import json
# from Comp.main import *

def Out_SHII_communities(comm):
    with open(comm, 'r') as f: 
        partition = json.load(f)
    print("communities completed!")
    Cdic = {}
    for key in partition:
        key1 = int(key)
        value1 = partition[key]
        if value1 in Cdic:
            Cdic[value1].append(key1+1)
        else: 
            Cdic[value1] = []
            Cdic[value1].append(key1+1)

    print(len(Cdic))
    mx = 0
    mi = 2000000
    with open('./shii_google_label.txt', 'w') as f: 
        for Ckey in Cdic:
            mx = max(mx,len(Cdic[Ckey]))
            mi = min(mi,len(Cdic[Ckey]))
            len1 = len(Cdic[Ckey])
            cnt = 0
            for node in Cdic[Ckey]:
                cnt += 1
                if cnt < len1:
                    f.write(str(node)+'\t')
                else:
                    f.write(str(node))
            f.write('\n')
    print(mx)
    print(mi)
    Lenlist = []
    for Ckey in Cdic:
        Lenlist.append(len(Cdic[Ckey]))
    print(Lenlist)


    # return partition


if __name__ == '__main__':
    print(BASE_DIR)
    # notice: ID start from 1.
    comm = BASE_DIR + '/Comp/community.txt'
    Out_SHII_communities(comm)


    # # run in current directory.
    # comm_file = BASE_DIR + '/Comp/community.txt'
    # partition = load_communities(comm_file)
    
    # com_size = cal_community_size(partition)
    # print(len(com_size))

