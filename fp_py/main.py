import argparse
import os
from random import sample
from typing import Dict, List
from collections import defaultdict
from functools import reduce
from math import log, prod



PATH = '/data/lingspam_public'


def get_txt_files(path: str) -> Dict[str, str]:
    """ a list comprehension of all txt files in a folder, are applied 
    to a map() passing each interation into get_text()
    """
    return {filename: os.path.join(dirpath, filename) 
    for dirpath, dirs, files in os.walk(path)
        for filename in files if filename.endswith('.txt') 
            and not filename.startswith('.')}


def get_data(adict: dict)-> Dict[str, List]:
    res = defaultdict(list)
    for filename, path in adict.items():
        if 'sp' in filename:
            res['spam'].append({'spam': {word: 'spam' 
            for word in read_file(path)}})
        else:
            res['ham'].append({'ham': {word: 'ham' 
            for word in read_file(path)}})
    return res


def read_file(path: str)-> List[str]:
    return [word for word in open(path).read().split(' ')]


def alpha(func):
    """ adds 1 to each word count
    before mapping each dict
    """
    def wrapper_alpha(*args, **kwargs):
        for dictionary in args:
            for key in dictionary:
                dictionary[key] += 1
        return func(*args, **kwargs)
    return wrapper_alpha

@alpha
def mapper(d1,d2):
    """ makes sure both dictionaries have same keys
    """
    for k in d2.keys():
        if k not in d1:
            d1[k] = 1
    for k in d1.keys():
        if k not in d2:
            d2[k] = 1
    return d1, d2


def word_count(alist):
    res = {}
    for email in alist:
        for word in [word for w in email.values() for word in w]:
            if word in res:
                res[word] += 1
            else:
                res[word] = 1
    return res


def wc_prob(wc):
    return {k: v / len(wc) for k,v in wc.items()}

def split_data(alist):
    return alist[:len(alist)//2], alist[len(alist)//2:]

def fit(emails):
    return wc_prob(word_count(emails))

# def predict(alist, email):
#     training_dict_ham = fit(alist['ham'])
#     training_dict_spam = fit(alist['spam'])
#     words = [word for word in email.values()]
#     for word in words:
#         if word in training_dict_ham:
            
# def score():
#     pass



##############################################################################
parser = argparse.ArgumentParser()
parser.add_argument('-B', '--bare', action='store_true', 
    help='using bare examples')
parser.add_argument('-L', '--lemma', action='store_true', 
    help='using lemma stop examples')
args = parser.parse_args()

if args.bare:
    data = get_data(get_txt_files(os.path.join(PATH, 'bare')))
elif args.lemma:
    data = get_data(get_txt_files(os.path.join(PATH, 'lemm_stop')))
else:
    exit(
        "\nYou need to specify '--bare' or '--lemma' in the command.\n")
##############################################################################

ham_data = data['ham']
spam_data = data['spam']

ham_training, ham_testing = split_data(ham_data)
spam_training, spam_testing = split_data(spam_data)

len_ham = len(ham_training)
len_spam = len(spam_training)

PRIOR_HAM = len_ham / (len_ham + len_spam) # P(Ham)
PRIOR_SPAM = 1 - PRIOR_HAM # P(Spam)

ham_wc, spam_wc = mapper(word_count(ham_training), word_count(spam_training)) # alpha applied 

ham_probs = {} # P(B|A) / P(B)
for word in ham_wc:
    ham_probs[word] = ham_wc[word]/ (len_ham )
    
spam_probs = {}
for word in spam_wc:
    spam_probs[word]  = spam_wc[word] / len_spam
    
for ht in ham_training:
    temp = []
    for k,v in ht.items():
        for word in v:
            if word in ham_probs:
                temp.append(ham_probs[word])
    product = 1
    for x in temp:
        product = product * x
    
    print(product)

