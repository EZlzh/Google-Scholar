import ReadGraph
import scipy.io as sio 
import networkx as nx
import json

def GetCCValue(CCdic):
    CClist = []
    for key in CCdic:
        # print(key)
        CClist.append((key, CCdic[key]))
    return CClist

def GetCCPortion(CCval):
    total_nodes_num = len(CCval)
    CCval = sorted(CCval, key=lambda x:x[1])

    cur_degree = 0.00
    cnt = 0
    CClist = []
    for node in CCval:
        if node[1] > cur_degree:
            while node[1] > cur_degree:
                CClist.append((cur_degree, cnt))
                cur_degree += 0.01                
        cnt += 1
    CClist.append((cur_degree, cnt))
    
    CC_x = []
    CC_y = []
    x_num = len(CClist)
    for i in range(x_num):
        CC_x.append(CClist[i][0])
        CC_y.append(CClist[i][1]/total_nodes_num)
    
    print(CC_x[:5], CC_y[:5])
    print(CC_x[95:100], CC_y[95:100])
    sio.savemat('./LCC/CC.mat', {'CC_x':CC_x, 'CC_y':CC_y})

if __name__ == '__main__':
    G = ReadGraph.Read_Graph()

    # CCdic = nx.clustering(G)
    # # for i in range(5):
    # #     print(CCdic[i])
    # CCval = GetCCValue(CCdic)
    # print(len(CCval))
    # print(CCval[:10])
    # with open('CCval.json', "w") as f:
    #     json.dump(CCval, f)
    
    CCval_new = []
    with open('CCval.json', "r") as f:
        CCval_new = json.load(f)
    # print(CCval_new[:10], CCval_new[-10:])

    Cres = GetCCPortion(CCval_new)

    print("average_clustering of LCC:", nx.average_clustering(G))