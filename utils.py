import os
import argparse
import sys
from typing import Dict, Tuple, List
from collections import defaultdict
from math import log




PATH = '../data/lingspam_public'



def get_txt_files(path: str) -> Dict[str, str]:
    """ a list comprehension of all txt files in a folder, are applied 
    to a map() passing each interation into get_text()
    """
    return {filename: os.path.join(dirpath, filename) 
    for dirpath, dirs, files in os.walk(path)
        for filename in files if filename.endswith('.txt') 
            and not filename.startswith('.')}


def get_data(adict: dict)-> List:
    """
    raw data 
    """
    res = []
    for filename, path in adict.items():
        if 'sp' in filename:
            res.append(([word for word in read_file(path)], 'spam'))
        else:
            res.append(([word for word in read_file(path)], 'ham'))
    return res
    

def read_file(path: str)-> List[str]:
    """
    """
    return list(open(path).read().split(' '))


def split_data(data: List):
    """ splits data in half
    into training and testing data
    """

    return data[:len(data)//2], data[len(data)//2:]


def word_count(data: List[Tuple[List, str]]) -> Dict[str, int]:
    """
    counts all occurances of words found in the data
    """
    res =  defaultdict(dict)
    res['spam']
    res['ham']

    for d in data:
        email, label = d
        for word in email:
            if word in res[label]:
                res[label][word] += 1
            else:
                res[label][word] = 1
    return res


def probability(data):
    """
    """
    res = data.copy()
    for label, d in res.items():
        for word, occ in d.items():
            res[label][word]\
                = log( (occ + 1) / len(data[label]))
    return res

##############################################################################
parser = argparse.ArgumentParser()
parser.add_argument('-B', '--bare', action='store_true', 
    help='using bare examples')
parser.add_argument('-L', '--lemma', action='store_true', 
    help='using lemma stop examples')
parser.add_argument('iter')
args = parser.parse_args()

iterations = int(args.iter)

if args.bare:
    data = get_data(get_txt_files(os.path.join(PATH, 'bare')))
elif args.lemma:
    data = get_data(get_txt_files(os.path.join(PATH, 'lemm_stop')))
else:
    sys.exit(
        "\nYou need to specify '--bare' or '--lemma' in the command.\n")
##############################################################################