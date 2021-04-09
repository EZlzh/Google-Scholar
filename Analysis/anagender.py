import os 
import sys
import scipy.io as sio 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import extractfile
import findfile
import numpy as np

from nltk import NaiveBayesClassifier
from nltk.corpus import names
import random
from nltk.classify import accuracy
from nltk.classify import apply_features
def gender_features(name):
    features = {}
    features["first_letter"] = name[0].lower()
    features["last_letter"] = name[-1].lower()
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        features["count({})".format(letter)] = name.lower().count(letter)
        features["has({})".format(letter)] = (letter in name.lower())
    return features

def prename():
    male_names = [(name, 'male') for name in names.words('male.txt')]
    female_names = [(name, 'female') for name in names.words('female.txt')]
    labeled_names = male_names + female_names
    random.shuffle(labeled_names)
    train_set = apply_features(gender_features, labeled_names[500:])
    test_set = apply_features(gender_features, labeled_names[:500])
    classifier = NaiveBayesClassifier.train(train_set)
    
    print(accuracy(classifier, test_set))
    return classifier

def ananame(msgs, classifier):
    male = 0
    female = 0
    for msg in msgs[:2000]:
        if len(msg) < 2:
            continue
        # print(msg[1])
        cur_name = msg[1].split(' ')[0]
        gender = classifier.classify(gender_features(cur_name))
        if gender == 'male':
            male += 1
        elif gender == 'female':
            female += 1
    print(male)
    print(female)

def dealname(classifier):
    list_suffix = ['top4000SHS-AP_Greedy.txt', 'top4000-Pagerank.txt', 'top4000-randomT.txt', 'top4000-Constraint.txt']
    # list_suffix = ['top4000SHS-AP_Greedy.txt'] 
    for suffix in list_suffix:
        SHS_file = BASE_DIR + '/Comp/' + suffix
        msgs = extractfile.extfile(SHS_file)
        ananame(msgs, classifier)
        
    return 

if __name__ == '__main__':
    classifier = prename()
    dealname(classifier)