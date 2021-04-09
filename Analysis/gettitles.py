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
remote_path = '/Users/apple/Documents/gs_info/'
idx_suffix = 'gs_info.txt'
import re
r4 =  "\\【.*?】+|\\《.*?》+|\\#.*?#+|[.!/_,$&%^*()<>+""'?@|:;~{}#]+|[——！\\\，。=？、：“”‘’￥……（）《》【】]"


def getrawtitles(msgs):
    SHtitles = []
    for msg in msgs[:2000]:
        A = []
        if len(msg) < 12:
            A.append([])
            continue
        for idx in range(12, len(msg)):
            Tlist = anaextendfile.deal_list(msg[idx])
            A.append(Tlist)
        SHtitles.append(A)
    # for idx in range(10):
    #     print(len(SHtitles[idx]))
    # mx = 0
    # sm = 0
    # for each in SHtitles:
    #     mx = max(mx,len(each))
    #     sm += len(each)
    # sm /= len(SHtitles)
    # print(mx,sm)
    return SHtitles

    # cur = 0
    # JS = []
    # useless = 0
    # for msg in tqdm(msgs[:2000]):
    #     # print(msg[8])
    #     NowDic = anaextendfile.deal_dic(msg[8])
    #     # print(NowDic)
    #     if len(A[cur]) == 0:
    #         # JS.append(1)
    #         useless = 1
    #     else: 
    #         Orinodes = anaextendfile.deal_coid(NowDic)
    #         Orifiles = findfile.transfer_file(Orinodes)
    #         newmsgs = extractfile.extractfiles(Orifiles)
    #         if len(newmsgs) == 0:
    #             # JS.append(1)
    #             useless = 1
    #         else: 
    #             weight = 0
    #             for newmsg in newmsgs:
    #                 if len(newmsg) < 4:
    #                     weight += 1
    #                     continue
    #                 Tlist = anaextendfile.deal_list(newmsg[3])
    #                 for everyT in Tlist:
    #                     if everyT in A[cur]:
    #                         weight += 1
    #                         break
    #             JS.append(1.0 - weight / len(newmsgs))
    #     cur += 1
    # print(JS)
    # return JS
import gensim
def read_corpus(fname, tokens_only=False):
    for i, line in enumerate(fname):
        tokens = gensim.utils.simple_preprocess(line)
        if tokens_only:
            yield tokens
        else:
            # For training data, add tags
            yield gensim.models.doc2vec.TaggedDocument(tokens, [i])

def doc_to_vec_test(Rawtitles):
    titles = []
    for Rawtitle in Rawtitles:
        titles.append(Rawtitle[1])
    # print(titles)

    # # deleting stopwords is not need for doc2vec.
    # from nltk.corpus import stopwords 
    # stop = set(stopwords.words('english')) 
    # for i in range(len(titles)):
    #     titles[i] = re.sub(r4,'',titles[i])
    #     filter_sentence= [w for w in titles[i].split(' ') if w not in stopwords.words('english')]
    #     titles[i] = ' '.join(filter_sentence)
    
    for i in range(len(titles)):
        titles[i] = re.sub(r4,'',titles[i])

    train_corpus = list(read_corpus(titles)) 
    model = gensim.models.doc2vec.Doc2Vec(vector_size=50, min_count=2, epochs=40)
    model.build_vocab(train_corpus)
    model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
    # vector = model.infer_vector(['only', 'you', 'can', 'prevent', 'forest', 'fires'])
    # print(vector)


    print(titles[-10:])
    print(train_corpus[-10:])
    print(len(titles))

def dealsocproof():
    list_suffix = ['top4000SHS-AP_Greedy.txt', 'top4000-Pagerank.txt', 'top4000-randomT.txt']
    cnt = 0
    for suffix in list_suffix:
        SHS_file = BASE_DIR + '/Comp/' + suffix
        msgs = extractfile.extfile(SHS_file)
        Rawtitles = getrawtitles(msgs)
        doc_to_vec_test(Rawtitles[0])
        return 

if __name__ == '__main__':
    dealsocproof()