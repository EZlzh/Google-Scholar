from tqdm import tqdm
import os 
import sys
import re
import json
import random
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from Analysis import findfile

gs_result_path = '/home/nds/GScholar/gs_result/'
findfile.prefind()

def extract_info(prefix, curfix):
    addr = prefix + curfix
    res_lines = []
    try: 
        with open(addr, 'r', encoding='UTF-8-sig') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            res_lines.append(line)
    except FileNotFoundError:
        # print("Warning!")
        return res_lines 
    return res_lines

def extractfiles(Orifiles):
    msg = []
    for Orifile in Orifiles:
        msg.append(extract_info(gs_result_path, Orifile))
    return msg

def extfile(SHS_file):
    
    Orifiles = findfile.findafile(SHS_file)
    # print(Orifiles[:20])
    msg = extractfiles(Orifiles)
    # print(msg[0])
    # with open('test.json','w') as f: 
    #     json.dump(msg[0], f)
    # with open('test2.json','w') as f: 
    #     json.dump(msg[1], f)
    # with open('test3.json','w') as f: 
    #     json.dump(msg[2], f)
    return msg
        

if __name__ == '__main__':
    list_suffix = ['top4000SHS-AP_Greedy.txt'] 
    for suffix in list_suffix:
        SHS_file = BASE_DIR + '/Comp/' + suffix
        extfile(SHS_file)
    