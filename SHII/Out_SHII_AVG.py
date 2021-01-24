import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import json

if __name__ == '__main__':
    topk = 50
    print(BASE_DIR)
    # notice: ID start from 1.
    SHS_dir = BASE_DIR + '/SHII/Output_SHII/'
    prefix = 'shii_google_'
    IC = 0
    suffix = ''
    mod = ''

    files = ['AP_BICC', 'AP_Greedy', 'HIS', 'Pagerank', 'Constraint', 'NOBE', 'NOBE_GA']
    for IC in range(2):
        if IC == 0:
            suffix = '_IC.txt'
            mod = 'IC'
        else :
            suffix = '_LT.txt'
            mod ='LT'
        
        for file in files:
            fname = prefix + file + suffix
            with open(SHS_dir + fname, "r") as f: 
                data = f.readlines()
                res1 = 0.0
                res2 = 0.0
                for line in data: 
                    numbers = line.split()
                    # print(float(numbers[0]), float(numbers[1]))
                    res1 += float(numbers[0])
                    res2 += float(numbers[1])
                res1 /= topk
                res2 /= topk
            
            print(file, mod, ":")
            print(res1,res2)



