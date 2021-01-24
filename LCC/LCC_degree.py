import ReadGraph
import scipy.io as sio 



def GetDegree():
    Alist = list(G.nodes)
    Ddic = G.degree(Alist)
    return Ddic

def GetDegreeValue(Ddic):
    Dlist = []
    for key in Ddic:
        # print(key)
        Dlist.append((key[0], key[1]))
    return Dlist

def GetDegreePortion(Dval):
    total_nodes_num = len(Dval)
    # print(total_nodes_num)
    
    Dval = sorted(Dval, key=lambda x:x[1])
    cur_degree = 1
    cnt = 0
    DPlist = []
    for node in Dval:
        if node[1] != cur_degree:
            while node[1] > cur_degree:
                DPlist.append((cur_degree, cnt))
                cur_degree += 1                
        cnt += 1
    DPlist.append((cur_degree, cnt))
    # print(len(DPlist))
    # print(DPlist[:5], DPlist[-5:])

    Degree_x = []
    Degree_y = []
    x_num = len(DPlist)
    for i in range(x_num):
        Degree_x.append(DPlist[i][0])
        Degree_y.append(DPlist[i][1]/total_nodes_num)
    
    # print(Degree_x[:5], Degree_x[-5:])
    # print(Degree_y[:5], Degree_y[-5:])
    print(Degree_x[95:100], Degree_y[95:100])
    sio.savemat('./LCC/Degree.mat', {'Degree_x':Degree_x[:100], 'Degree_y':Degree_y[:100]})

if __name__ == '__main__':
    G = ReadGraph.Read_Graph()
    # print(G.number_of_nodes())
    
    Ddic = GetDegree()
    # for i in range(5):
    #     print(i, Ddic[i])
    
    Dval = GetDegreeValue(Ddic)
    # print(len(Dval))
    # print(Dval[:10])

    
    Dres = GetDegreePortion(Dval)
    # print(Dval[:5], Dval[-5:])
