from tqdm import tqdm
import os 
import sys
import scipy.io as sio 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import extractfile
import anaextendfile
import findfile
import numpy as np
remote_path = '/Users/apple/Documents/gs_info/'
idx_suffix = 'gs_info.txt'


def anasocproof(msgs, GSDic, cnt):
    A = []
    for msg in msgs[:2000]:
        if len(msg) < 4:
            A.append([])
            continue
        Tlist = anaextendfile.deal_list(msg[3])
        A.append(Tlist)
    # print(A[:10])

    cur = 0
    JS = []
    useless = 0
    for msg in tqdm(msgs[:2000]):
        # print(msg[8])
        NowDic = anaextendfile.deal_dic(msg[8])
        # print(NowDic)
        if len(A[cur]) == 0:
            # JS.append(1)
            useless = 1
        else: 
            Orinodes = anaextendfile.deal_coid(NowDic)
            Orifiles = findfile.transfer_file(Orinodes)
            newmsgs = extractfile.extractfiles(Orifiles)
            if len(newmsgs) == 0:
                # JS.append(1)
                useless = 1
            else: 
                weight = 0
                for newmsg in newmsgs:
                    if len(newmsg) < 4:
                        weight += 1
                        continue
                    Tlist = anaextendfile.deal_list(newmsg[3])
                    for everyT in Tlist:
                        if everyT in A[cur]:
                            weight += 1
                            break
                JS.append(1.0 - weight / len(newmsgs))
        cur += 1
    print(JS)
    return JS



def dealsocproof():
    list_suffix = ['top4000SHS-AP_Greedy.txt', 'top4000-Pagerank.txt', 'top4000-randomT.txt']
    cnt = 0
    Sdic = {}
    GSDic = anaextendfile.GetGSDic()
    for suffix in list_suffix:
        SHS_file = BASE_DIR + '/Comp/' + suffix
        msgs = extractfile.extfile(SHS_file)
        JS = anasocproof(msgs, GSDic, cnt)
        cur_name = suffix.split('-')[1].split('.')[0]
        Sdic[str(cur_name+'_JS')] = JS
    sio.savemat('./Ana-social-proof.mat', Sdic)
    return 

if __name__ == '__main__':
    dealsocproof()