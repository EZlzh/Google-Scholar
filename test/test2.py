from tqdm import tqdm
import os 
import re
from ast import literal_eval

cur_year = 2021

def extract_info(prefix, curfix):
    addr = prefix + curfix
    try: 
        with open(addr, 'r') as f:
            lines = f.readlines()
        res_lines = []
        for line in lines:
            line = line.strip()
            res_lines.append(line)
    except FileNotFoundError:
        return [str(''),str(''),str('')]
        # print(line)
    # print(res_lines[2], '\n', res_lines[4], curfix, nid)
    return res_lines

def find_earliest_year(set_papers, addr):
    year = 2021
    if len(addr) > 12:
        for paper in addr[12:]:
            new_list = literal_eval(paper)
            if re.match('\d{4}', new_list[-1]):
                if new_list[1] in set_papers:
                    year = min(year, int(new_list[-1]))
    else: 
        pass
    return year
cur = 0

if __name__ == '__main__':
    htap = '/Users/apple/Documents/gs_result/'
    Li = 'rU4xX5wAAAAJ.parse'
    # addr[8] is the list of co-authors; starting from addr[12] can cal the papers.
    addr = extract_info(htap, Li)
    ego_papers = []
    set_papers = set()
    print('total papers: ',len(addr)-12)
    if len(addr) > 8:
        new_dict = literal_eval(addr[8])
        print('total co-authors:', len(new_dict))
        # print(new_dict)
    if len(addr) > 12:
        # print(addr[12])
        for paper in addr[12:]:
            new_list = literal_eval(paper)
            ego_papers.append(new_list)
            # print(new_list)
            if re.match('\d{4}', new_list[-1]):
                cur += 1
                # print(new_list[1], new_list[-1])
                set_papers.add(new_list[1])
                print(new_list)
    print('papers with year:', cur)
    
    ego = addr[1]
    print(ego)
    res = 0
    for key in new_dict:
        # print(key, new_dict[key])
        addr = extract_info(htap, key+'.parse')
        year = find_earliest_year(set_papers, addr)
        if year != 2021:
            res += 1
            print(ego,'and',new_dict[key], key, "'s co-authorship begin from",year)
    print(res)