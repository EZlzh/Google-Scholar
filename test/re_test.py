
import tqdm
import os
import re

if __name__ == '__main__':
    text = ['Fudan', 'asFudan','as Fudan as','fuden']
    words = [w for w in text if re.match(".*fudan.*", w.lower())]
    print(words)
    