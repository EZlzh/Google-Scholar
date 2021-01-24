import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import json
# from Comp.main import *

def Out_SHII_topk(SHS_file,topk):
    SHS = []
    with open (SHS_file, 'r') as f: 
        lines = f.readlines()
        for line in lines:
            conn = line.strip().split(' ')
            # SHS.append((int(conn[0]),int(conn[1])))
            SHS.append(int(conn[1]))
    # print("SHS completed!")
    # print(SHS[:topk])
    with open('./shii_google_NOBE_topk.txt', 'w') as f: 
        cnt = 0
        for i in SHS[:topk]:
            cnt += 1
            if cnt < topk:
                f.write(str(i+1)+' ')
            else: 
                f.write(str(i+1))
        f.write('\n')
    


if __name__ == '__main__':
    print(BASE_DIR)
    # notice: ID start from 1.
    SHS_file = BASE_DIR + '/Comp/top4000-NOBE.txt'
    topk = 50
    Out_SHII_topk(SHS_file,topk)

