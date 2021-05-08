from tqdm import tqdm
import os 
import sys
import scipy.io as sio 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from Analysis import extractfile
from Analysis import anaextendfile
from Analysis import findfile
import numpy as np
remote_path = '/home/nds/GScholar/gs_info/'
idx_suffix = 'gs_info.txt'
import re
r4 =  "\\【.*?】+|\\《.*?》+|\\#.*?#+|[.!/_,$&%^*()<>+""'?@|:;~{}#]+|[——！\\\，。=？、：“”‘’￥……（）《》【】]"
import json
TEST = True
MI = (1<<31)
Vdic = {}

def deal_raw_list(str):
    Alist = []
    str = str.strip('[')
    str = str.strip(']')
    if len(str) > 0:
        strs = str.split('\', ')
        for s in strs:
            # print(s)
            s = s.strip('\'')
            # s = s.lower()
            Alist.append(s)
    return Alist

def getrawtitle(msg):
    '''
        extract paper titles with citation > 1.
    '''
    A = []
    if len(msg) < 12:
        A.append([])
        return A
    for idx in range(12, len(msg)):
        Tlist = deal_raw_list(msg[idx])
        # print(Tlist)
        if len(Tlist) > 2 and str(Tlist[-2]).isdigit() and str(Tlist[-1]).isdigit():
            if int(Tlist[-2]) > 1:
                # print(Tlist)
                A.append(Tlist)
    return A

def getcoauthor(msg):
    NowDic = anaextendfile.deal_dic(msg[8])
    # print(NowDic)
    return NowDic

def getcoauthorfreq(NowDic, Rawtitles, topkcoauthor):
    NewDic = {}
    for key in NowDic:
        s = NowDic[key].strip().split(' ')
        first_letter = s[0][0]
        last_name = s[-1]
        cnt = 0
        # print(first_letter, last_name)
        for rawtitle in Rawtitles:
            authors = rawtitle[2].split(', ')
            # print(authors)
            for author in authors:
                each_name = author.strip().split(' ')
                if each_name[-1] == last_name:
                    if each_name[0][0] == first_letter:
                        cnt += 1    
        if cnt > 0:
            NewDic[key] = cnt          
    # print(len(NewDic))
    # print(NowDic)
    Sorted_NewDic = sorted(NewDic.items(), key=lambda x: x[1], reverse=True)
    

    Orifiles = []
    Coauthors_count = []
    for key in Sorted_NewDic:
        s = key[0] + '.parse'
        Orifiles.append(s)
        Coauthors_count.append(key[1])
    # if TEST:
    #     print(Orifiles)
    #     print(len(Orifiles))
    newmsgs = extractfile.extractfiles(Orifiles)  
    
    # if TEST:
    #     print(len(newmsgs))
    #     print(newmsgs[0])
    
    Coauthor_Rawtitles_list = []
    CoAuthors = []
    for i, newmsg in enumerate(newmsgs):
        if len(newmsg) > 12:   
            Coauthor_Rawtitles = getrawtitle(newmsg)
            # print(len(Coauthor_Rawtitles))     
            Coauthor_Rawtitles_list.append(Coauthor_Rawtitles)
            CoAuthors.append(newmsg[0])
    # print(len(Coauthor_Rawtitles_list))
    return Coauthor_Rawtitles_list, Coauthors_count, CoAuthors

def similarity(a_vect, b_vect):

    dot_val = 0.0
    a_norm = 0.0
    b_norm = 0.0
    cos = None
    for a, b in zip(a_vect, b_vect):
        dot_val += a*b
        a_norm += a**2
        b_norm += b**2
    if a_norm == 0.0 or b_norm == 0.0:
        cos = -1
    else:
        cos = dot_val / ((a_norm*b_norm)**0.5)
    return cos


def doc_to_vec(Rawtitles, Coauthor_Rawtitles_list, Coauthors_count, Author, CoAuthors):
    titles = set()
    sum_list = []
    ori_sum = 0
    for Rawtitle in Rawtitles:
        titles.add(Rawtitle[1])
        ori_sum += int(Rawtitle[-2])
    # print(ori_sum)

    for Coauthor_Rawtitles in Coauthor_Rawtitles_list:
        coa_sum = 0
        for Rawtitle in Coauthor_Rawtitles:
            titles.add(Rawtitle[1])
            coa_sum += int(Rawtitle[-2])
        sum_list.append(coa_sum)
    # print(len(titles))
    titles = list(titles)
    for i in range(len(titles)):
        titles[i] = re.sub(r4,'',titles[i])
    # print(titles[:10])
    
    # 5
    # train_corpus = list(read_corpus(titles))

    if len(titles) < 3:
        return [],[]
    Flag = True
    for title in titles:
        if title != '':
            Flag = False
            break
    if Flag == True:
        return [],[]
    # print(train_corpus)
    # if TEST:
    #     print(titles[:10])
    #     print(train_corpus[:5])

    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('paraphrase-distilroberta-base-v1')
    sentence_embeddings = model.encode(titles)

    # 1
    # model = gensim.models.doc2vec.Doc2Vec(vector_size=50, min_count=2, epochs=40)
    # model.build_vocab(train_corpus)
    # model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
    
    titles_Dic = {}
    for i,title in enumerate(titles):
        titles_Dic[title] = i
        # if title == 'Electrochemical approach of anticancer drugs–DNA interaction':
        #     print(model.dv[i])

    ori_vec = np.zeros((50,))
    # now_sum = 0
    global Vdic
    if Author in Vdic:
        ori_vec = Vdic[Author]
    else: 
        for i,Rawtitle in enumerate(Rawtitles):
            title = Rawtitle[1]
            title = re.sub(r4,'',title)
            # now_vec = model.dv[titles_Dic[title]]
            # 2
            now_vec = sentence_embeddings[titles_Dic[title]]
            # print(type(now_vec),now_vec.dtype, now_vec.shape)
            if i == 0:
                ori_vec = now_vec * (int(Rawtitle[-2])/ori_sum)
            else: 
                ori_vec += now_vec * (int(Rawtitle[-2])/ori_sum)
        Vdic[Author] = ori_vec

    Cos_list = []
    Cos_cnt = []
    # print(len(Coauthor_Rawtitles_list))
    for j,Coauthor_Rawtitles in enumerate(Coauthor_Rawtitles_list):
        coa_vec = np.zeros((50,))
        if CoAuthors[j] in Vdic:
            coa_vec = Vdic[CoAuthors[j]]
        else: 
            for i,Rawtitle in enumerate(Coauthor_Rawtitles):
                title = Rawtitle[1]
                title = re.sub(r4,'',title)
                # now_vec = model.dv[titles_Dic[title]]
                # 3
                now_vec = sentence_embeddings[titles_Dic[title]]
                if i == 0:
                    coa_vec = now_vec * (int(Rawtitle[-2])/sum_list[j])
                else: 
                    coa_vec += now_vec * (int(Rawtitle[-2])/sum_list[j])
            Vdic[CoAuthors[j]] = coa_vec
        coss = similarity(ori_vec, coa_vec)
        # cost = similarity(coa_vec, ori_vec)
        # print(coss)
        Cos_list.append(coss)
        Cos_cnt.append(Coauthors_count[j])
    return Cos_list, Cos_cnt
    

def dealsocenrichment():
    list_suffix = ['top4000SHS-AP_Greedy.txt', 'top4000-Pagerank.txt', 'top4000-randomT.txt']
    # list_suffix = [ 'top4000-randomT.txt']
    cnt = 0
    topk = 2000
    topkcoauthor = 10
    Sdic = {}
    for suffix in list_suffix:
        SHS_file = BASE_DIR + '/Comp/' + suffix
        msgs = extractfile.extfile(SHS_file)
        # Rawtitles = getrawtitles(msgs)
        ans_list = []
        ans_cnt = []
        Total_list = []
        Total_cnt = []
        for msg in tqdm(msgs[:topk]):
            Rawtitles = getrawtitle(msg)
            Author = msg[0]
            NowDic = getcoauthor(msg)
            Coauthor_Rawtitles_list, Coauthors_count, CoAuthors = getcoauthorfreq(NowDic, Rawtitles, topkcoauthor)
            Cos_list, Cos_cnt = doc_to_vec(Rawtitles, Coauthor_Rawtitles_list, Coauthors_count, Author, CoAuthors)
            Total_list.append(Cos_list)
            Total_cnt.append(Cos_cnt)
            if len(Cos_list) >= topkcoauthor:
                ans_list.append(Cos_list[:topkcoauthor])
                ans_cnt.append(Cos_cnt[:topkcoauthor])
            # if suffix == 'top4000-randomT.txt':
            #     print(len(Cos_list))
            
        # with open ('soc_enr_freq_sim_'+suffix, 'w') as f: 
        #     json.dump(Total_list,f)
        # with open ('soc_enr_freq_cnt_'+suffix, 'w') as f: 
        #     json.dump(Total_cnt,f)
        ans_list_matrix = np.array(ans_list)
        ans_cnt_matrix = np.array(ans_cnt)
        print(ans_list_matrix.shape)
        if ans_list_matrix.size != 0:
            print(ans_list_matrix.mean(axis=0))
            print(ans_cnt_matrix.mean(axis=0))
        cur_name = suffix.split('-')[1].split('.')[0]
        Sdic[str(cur_name+'_freq_sim_top'+str(topkcoauthor)+'_')] = ans_list_matrix.mean(axis=0)
        Sdic[str(cur_name+'_freq_cnt_top'+str(topkcoauthor)+'_')] = ans_cnt_matrix.mean(axis=0)
    sio.savemat('./Ana-freq-soc-enc-BERT.mat', Sdic)

if __name__ == '__main__':
    dealsocenrichment()