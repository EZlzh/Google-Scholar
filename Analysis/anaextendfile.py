from re import A
from tqdm import tqdm
import os 
import sys
import scipy.io as sio 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from Analysis import extractfile
from Analysis import findfile
import numpy as np
import json
import math
from numpy import *
import ast
gs_result_path = '/home/nds/GScholar/gs_result/'
remote_path = '/home/nds/GScholar/gs_info/'
idx_suffix = 'gs_info.txt'
CCtest = {}

def deal_list(str):
    Alist = []
    str = str.strip('[')
    str = str.strip(']')
    if len(str) > 0:
        strs = str.split(', ')
        for s in strs:
            # print(s)
            s = s.strip('\'')
            s = s.lower()
            Alist.append(s)
    return Alist

def anatop(msgs):
    Dictop = {}
    res = 0
    cnt = 0
    A = []
    B = []
    for msg in msgs[:2000]:
        cnt += 1
        # print(msg[3])
        if len(msg) < 4:
            continue
        Tlist = deal_list(msg[3])
        # print(Tlist)
        # print(len(Tlist))
        res += len(Tlist)
        for item in Tlist:
            if item in Dictop:
                Dictop[item] += 1
            else: 
                Dictop[item] = 1
        if cnt % 200 == 0:
            # print('round: ' + str(cnt))
            # print('total:' + str(res))
            # print('set: '+ str(len(Dictop)))
            A.append(res)
            B.append(len(Dictop))

    Dic_list = sorted(Dictop.items(), key=lambda x:x[1], reverse=True)
    print(Dic_list[:10])
    return A, B

def anamail(msgs):
    Dictop = {}
    NewDic = {}
    Newlist0 = []
    Newlist = []
    for msg in msgs[:100]:
        Address = msg[2]
        # print(Address)
        # Address = msg[4]
        Address = msg[4].split(' ')[-1]
        # print(Address)
        if Address in Dictop:
            Dictop[Address] += 1
        else: 
            Dictop[Address] = 1
        
        Add_list = Address.split('.')
        cur_name = ''
        if Add_list[-1] == 'edu' or Add_list[-1] == 'org' or Add_list[-1] == 'com' or Add_list[-1] == 'gov':
            cur_name = Add_list[-2] + '.'+ Add_list[-1]
        elif Add_list[-2] == 'ac' or Add_list[-2] == 'edu' or Add_list[-2] == 'ernet' or Add_list[-2] == 're':
            cur_name = Add_list[-3] + '.'+ Add_list[-2] + '.'+ Add_list[-1]
        else:
            cur_name = Add_list[-2] + '.'+ Add_list[-1]
        
        if cur_name in NewDic:
            NewDic[cur_name] += 1
            Newlist0.append(cur_name)
        else: 
            NewDic[cur_name] = 1
            Newlist0.append(cur_name)

    # Dic_list = sorted(Dictop.items(), key=lambda x:x[1], reverse=True)
    # print(len(Dictop))
    # print(Dic_list[:10])

    # print(len(NewDic))
    NewDic2 = sorted(NewDic.items(), key=lambda x:x[1], reverse=True)
    # print(NewDic2[:10])

    Country = {}
    for key in NewDic:
        str = key.split('.')
        # print(str, key)
        if str[-1] == 'edu' or str[-1] == 'org' or str[-1] == 'com' or str[-1] == 'gov':
            cur_str = str[-2] + '.' + str[-1]
            if cur_str in Country:
                Country[cur_str] += NewDic[key]
            else: 
                Country[cur_str] = NewDic[key]
        else:
            if str[-1] in Country:
                Country[str[-1]] += NewDic[key]
            else: 
                Country[str[-1]] = NewDic[key]
    
    # print(len(Country))
    Country2 = sorted(Country.items(), key = lambda x: x[1], reverse=True)
    # print(Country2[:])

    for key in Newlist0:
        str = key.split('.')
        # print(str, key)
        cur_str = ''
        if str[-1] == 'edu' or str[-1] == 'org' or str[-1] == 'com' or str[-1] == 'gov':
            cur_str = str[-2] + '.' + str[-1]
        else: 
            cur_str = str[-1]
        Newlist.append(cur_str)
    
    # CCtest['it'] = 'Italy'
    # CCtest['uk'] = 'UK'
    # with open('Country.json', "w") as f: 
    #     for key in Country:
    #         CCtest[key] = key.upper()
    #     json.dump(CCtest, f)
    Country3 = {}
    with open('Country.json', "r") as f: 
        CC = json.load(f)
    # print(len(CC))
    # print(CC['it'])
        for key in Country:
            if CC[key] in Country3:
                Country3[CC[key]] += Country[key]
            else :
                Country3[CC[key]] = Country[key]

    # print(len(Country3))
    Country4 = sorted(Country3.items(), key = lambda x: x[1], reverse=True)
    # print(Country4[:])
    res = []
    seq = []
    total = 100
    entropy = 0
    for each_country in Country4:
        if each_country[1] == 1:
            p = each_country[1] / total
            entropy += -p*math.log2(p)
        else: 
            seq.append(each_country[0])
            res.append(float(each_country[1]))
            # total -= each_country[1]
            p = each_country[1] / total
            entropy += -p*math.log2(p)
        # print(p)
    # print(seq, res)
    seq.append('Others')
    res.append(float(total))
    # print(entropy)


    # calcuklated top-k entropy (mod 10)
    entropy = 0
    Country3 = {}
    etp = []
    for i in range(len(Newlist)):
        key = Newlist[i]
        if CC[key] in Country3:
            Country3[CC[key]] += 1
        else :
            Country3[CC[key]] = 1
        if (i + 1) % 10 == 0:
            entropy = 0
            tot = i + 1
            for key in Country3:
                p = Country3[key] / tot
                entropy += -p*math.log2(p)
            print('{0} {1}'.format(tot, entropy))
            etp.append(entropy)
    # print(Country3)

    # entropy = 0
    # tot = 100
    # for key in Country3:
    #     p = Country3[key] / tot
    #     # print(p)
    #     entropy += -p*math.log2(p)
    # print(entropy)

    return seq, res, etp


def dealtop():
    list_suffix = ['top4000SHS-AP_Greedy.txt', 'top4000-Pagerank.txt', 'top4000-randomT.txt', 'top4000-Constraint.txt']
    # list_suffix = ['top4000SHS-AP_Greedy.txt'] 
    Adic = {}
    AA = np.array([])
    BB = np.array([])
    cnt = 0
    for suffix in list_suffix:
        SHS_file = BASE_DIR + '/Comp/' + suffix
        msgs = extractfile.extfile(SHS_file)
        # msg : annotation.txt
        # print('topics of :' + suffix)
        A, B = anatop(msgs)
        cur_name = suffix.split('-')[1].split('.')[0]
        print(cur_name)
        
        if cnt == 0:
            cnt += 1
            AA = np.array(A).reshape(-1,1)
            BB = np.array(B).reshape(-1,1)
        else: 
            # print(AA.shape)
            # print(A.shape)
            AA = np.concatenate((AA, np.array(A).reshape(-1,1)), axis=1)
            BB = np.concatenate((BB, np.array(B).reshape(-1,1)), axis=1)
    Adic[str('tot_A')] = AA
    Adic[str('set_B')] = BB

    idx = []
    for i in range(0,2000,200):
        i += 200
        idx.append(i)
    # print(idx)
    Adic['idx2'] = idx 
    sio.savemat('./Ana-topic-test1.mat', Adic)

def dealmail():
    # list_suffix = ['top4000SHS-AP_Greedy.txt'] 
    list_suffix = ['top4000SHS-AP_Greedy.txt', 'top4000-Pagerank.txt', 'top4000-randomT.txt']
    Mdic = {}
    for suffix in list_suffix:
        SHS_file = BASE_DIR + '/Comp/' + suffix
        cur_name = suffix.split('-')[1].split('.')[0]
        print(cur_name)
        msgs = extractfile.extfile(SHS_file)
        seq, res, etp = anamail(msgs)
        Mdic[str(cur_name+'_result')] = res
        Mdic[str(cur_name+'_country')] = seq
        Mdic[str(cur_name+'_entropy')] = etp
    # print(Mdic)
    idx = []
    for i in range(0,100,10):
        i += 10
        idx.append(i)
        # print(i)
    Mdic['idx'] = idx 
    sio.savemat('./Ana-mail-test1.mat', Mdic)

def anaindex(Orinodes, GSDic):
    # print(Orinodes[:100])
    citations = []
    hidx = []
    gidx = []
    aca = []
    cnt = 0
    Mcitations = []
    Mhidx = []
    Mgidx = []
    Maca = []
    Dicaca = {}
    for node in Orinodes[:2000]:
        citations.append(int(GSDic[node][0]))
        hidx.append(int(GSDic[node][1]))
        gidx.append(int(GSDic[node][2]))
        aca.append(int(GSDic[node][3]))
        title = int(GSDic[node][3])
        if title in Dicaca:
            Dicaca[title] += 1
        else: 
            Dicaca[title] = 1
        # break
        cnt += 1
        if cnt % 200 == 0:
            Mcitations.append(mean(citations))
            Mhidx.append(mean(hidx))
            Mgidx.append(mean(gidx))
            Maca.append(mean(aca))
    # print(Mcitations)
    # print(Mhidx)
    # print(Mgidx)
    # print(Maca)
    # print(Dicaca)
    return Mcitations,Mhidx,Mgidx,Maca
        

def dealindex():
    list_suffix = ['top4000SHS-AP_Greedy.txt', 'top4000-Pagerank.txt', 'top4000-randomT.txt', 'top4000-Constraint.txt']
    GSDic = {}
    with open(remote_path+idx_suffix, 'r') as f: 
        lines = f.readlines()
        for line in lines:
            A = line.split()
            GSDic[int(A[0])] = A[1:]
    # print(len(GSDic))
    
    Idic = {}
    for suffix in list_suffix:
        SHS_file = BASE_DIR + '/Comp/' + suffix
        cur_name = suffix.split('-')[1].split('.')[0]
        Orinodes = findfile.transfer_node(SHS_file)
        citations,hidx,gidx,aca = anaindex(Orinodes, GSDic)
        Idic[str(cur_name+'_cite')] = citations
        Idic[str(cur_name+'_hidx')] = hidx
        Idic[str(cur_name+'_gidx')] = gidx

    idx = []
    for i in range(0,2000,200):
        i += 200
        idx.append(i)
        # print(i)
    Idic['idx2'] = idx 
    sio.savemat('./Ana-index-test1.mat', Idic)

def deal_dic(str):
    Adic = {}
    str = str.strip('{')
    str = str.strip('}')
    if len(str) > 0:
        # print(str)
        strs = str.split('\', \'')
        # print(strs)
        for s in strs:
            # print(s)
            s = s.split(': ')
            s[0] = s[0].strip('\'')
            s[1] = s[1].strip('\'')
            Adic[s[0]] = s[1]
    return Adic

def deal_cotop(CODic):
    msgs = []
    for key in CODic:
        # print(gs_result_path+key+'.parse')
        msgs.append(extractfile.extract_info(gs_result_path, key+'.parse'))
        # break
    # print(msgs)
    return msgs

def deal_coid(CODic):
    Orinodes = []
    StrDic = {}
    with open(remote_path+'gs_id.txt', "r") as f: 
        lines = f.readlines()
        for line in lines:
            line = line.split()
            StrDic[line[1].split('.')[0]] = int(line[0])
            # print(line[1].split('.')[0])
            # break
    for key in CODic:
        if key in StrDic:
            Orinodes.append(StrDic[key])
        else:
            Orinodes.append(-1)
    # print(len(Orinodes))
    return Orinodes


def anacotop(msgs):
    Dictop = {}
    res = 0
    cnt = 0
    A = []
    B = []
    for msg in msgs:
        cnt += 1
        # print(msg[3])
        if len(msg) < 4:
            continue
        Tlist = deal_list(msg[3])
        # print(Tlist)
        # print(len(Tlist))
        res += len(Tlist)
        for item in Tlist:
            if item in Dictop:
                Dictop[item] += 1
            else: 
                Dictop[item] = 1

    Dic_list = sorted(Dictop.items(), key=lambda x:x[1], reverse=True)
    # print(Dic_list[:10])
    return res, len(Dictop)

def GetGSDic():
    GSDic = {}
    with open(remote_path+idx_suffix, 'r') as f: 
        lines = f.readlines()
        for line in lines:
            A = line.split()
            GSDic[int(A[0])] = A[1:]
    return GSDic

def ana_coindex(Orinodes, GSDic, typ):
    # print(Orinodes[:100])
    citations = []
    hidx = []
    gidx = []
    for node in Orinodes:
        if node == -1:
            citations.append(int(2000))
            hidx.append(int(15))
            gidx.append(int(25))
        else: 
            citations.append(int(GSDic[node][0]))
            hidx.append(int(GSDic[node][1]))
            gidx.append(int(GSDic[node][2]))

    # if len(Orinodes) == 0:
    #     if typ == 1:
    #         citations = [5000]
    #         hidx = [45]
    #         gidx = [25]
    #     elif typ == 3:
    #         citations = [2000]
    #         hidx = [25]
    #         gidx = [15]
    #     else:
    #         citations = [32000]
    #         hidx = [120]
    #         gidx = [70]
    if len(Orinodes) == 0:
        # if typ == 1:
        #     citations = [5000]
        #     hidx = [22.5] # 45*0.2 + 25*0.7 + 120*0.1
        #     gidx = [38.5] # 45*0.2 + 15*0.7 + 120*0.1
        # elif typ == 3:
        #     citations = [2200]
        #     hidx = [16]
        #     gidx = [26]
        # else:
        #     citations = [5300] # 32000*0.1 + 2000*0.8 + 5000*0.1
        #     hidx = [46] # 45*0.1 + 25*0.7 + 120*0.2
        #     gidx = [70]
        citations = [2000]
        hidx = [15]
        gidx = [25]

    return citations,hidx,gidx

def anaco(msgs, GSDic, typ):
    tot = 0
    cnt = 0
    co_num = []
    CODic = {}
    A = []
    B = []
    C = []

    Mcitations = []
    Mhidx = []
    Mgidx = []
    citations = []
    hidx = []
    gidx = []
    Orinodes = []
    for msg in msgs[:100]:
        # print(msg[8])
        NowDic = deal_dic(msg[8])
        CODic.update(NowDic)
        # print(CODic)
        tot = len(CODic)

        Orinodes = deal_coid(NowDic)
        CC, HH, GG = ana_coindex(Orinodes, GSDic, typ)
        citations.append(mean(CC))
        hidx.append(mean(HH))
        gidx.append(mean(GG))

        cnt += 1
        if cnt % 10 == 0:
            co_num.append(tot)
            msgs = deal_cotop(CODic)
            res1, res2 = anacotop(msgs)
            B.append(res2)
            C.append(res2/tot)

            # Orinodes = deal_coid(CODic)
            # citations,hidx,gidx,_ = ana_coindex(Orinodes, GSDic)
            Mcitations.append(mean(citations))
            Mhidx.append(mean(hidx))
            Mgidx.append(mean(gidx))
        # break
    
    print(Orinodes[:10])
    print(co_num, B, C) # Non-repetitive topics
    print(Mcitations)
    print(Mhidx, Mgidx)
    return co_num, B, C, Mcitations, Mhidx, Mgidx
        

def dealcoan():
    list_suffix = ['top4000SHS-AP_Greedy.txt', 'top4000-Pagerank.txt', 'top4000-randomT.txt']
    Cdic = {}
    GSDic = GetGSDic()
    cnt = 0
    for suffix in list_suffix:
        cnt += 1
        SHS_file = BASE_DIR + '/Comp/' + suffix
        cur_name = suffix.split('-')[1].split('.')[0]
        print(cur_name)
        msgs = extractfile.extfile(SHS_file)
        co_num, co_topic, co_not, Mcitations, Mhidx, Mgidx = anaco(msgs, GSDic, cnt)
        # print(co_num)
        Cdic[str(cur_name+'_CoAN')] = co_num
        Cdic[str(cur_name+'_CoAT')] = co_topic
        Cdic[str(cur_name+'_CoANoverT')] = co_not
        Cdic[str(cur_name+'_CoMcidx')] = Mcitations
        Cdic[str(cur_name+'_CoMhidx')] = Mhidx
        Cdic[str(cur_name+'_CoMgidx')] = Mgidx
    idx = []
    for i in range(0,100,10):
        i += 10
        idx.append(i)
        # print(i)
    Cdic['idx'] = idx 
    sio.savemat('./Ana-CoA-test1.mat', Cdic)


if __name__ == '__main__':
    
    dealtop()
    # dealmail()
    # dealindex()
    # dealcoan()
