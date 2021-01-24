import ReadGraph
import scipy.io as sio 
import networkx as nx
import json

def GetPRValue(PRdic):
    PRlist = []
    for key in PRdic:
        # print(key)
        PRlist.append((key, PRdic[key]))
    return PRlist

def GetPRPortion(PRval):
    total_nodes_num = len(PRval)
    PRval = sorted(PRval, key=lambda x:x[1])

    print(PRval[:5])
    print(PRval[-5:])

    cur_degree = 0.01
    cnt = 0
    CClist = []
    for node in PRval:
        if node[1]*100000 > cur_degree:
            while node[1]*100000 > cur_degree:
                CClist.append((cur_degree, cnt))
                cur_degree += 0.01                
        cnt += 1
    CClist.append((cur_degree, cnt))
    # print(len(CClist))
    CC_x = []
    CC_y = []
    x_num = len(CClist)
    for i in range(x_num):
        CC_x.append(CClist[i][0])
        CC_y.append(CClist[i][1]/total_nodes_num)
    
    print(CC_x[:5], CC_y[:5])
    print(CC_x[95:100], CC_y[95:100])
    sio.savemat('./LCC/Pagerank.mat', {'Pagerank_x':CC_x[:100], 'Pagerank_y':CC_y[:100]})

if __name__ == '__main__':
    G = ReadGraph.Read_Graph()
    
    # PRdic = nx.pagerank(G)
    # for i in range(5):
    #     print(PRdic[i])
    # PRval = GetPRValue(PRdic)
    # print(len(PRval))
    # print(PRval[:10])
    # with open('PageRankval.json', "w") as f:
    #     json.dump(PRval, f)
    

    PRval_new = []
    with open('PageRankval.json', "r") as f:
        PRval_new = json.load(f)
    # print(PRval_new[:10], PRval_new[-10:])

    PRres = GetPRPortion(PRval_new)