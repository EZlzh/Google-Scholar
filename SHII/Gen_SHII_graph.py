import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
# from Comp.main import *

def Out_SHII_graph(graph_file):
    edges = []
    mx = 0
    with open (graph_file, 'r') as f: 
        lines = f.readlines()
        for line in lines[1:]:
            conn = line.strip().split(' ')
            edges.append((int(conn[0]),int(conn[1])))
            mx = max(mx, max(int(conn[0]),int(conn[1])))

    with open('./shii_google_edge_dir.txt', 'w') as f: 
        f.write(r'%%MatrixMarket matrix coordinate integer general'+'\n')
        f.write(r'%'+'\n')
        f.write(str(mx+1)+' '+str(mx+1)+' '+str(len(edges))+'\n')
        for conn in edges:
            f.write(str(conn[0]+1)+' '+str(conn[1]+1)+' '+'1'+'\n')
            f.write(str(conn[1]+1)+' '+str(conn[0]+1)+' '+'1'+'\n')


if __name__ == '__main__':
    print(BASE_DIR)
    # notice: ID start from 1.
    graph_file = BASE_DIR + '/Comp/Google_Scholar.txt'
    Out_SHII_graph(graph_file)

