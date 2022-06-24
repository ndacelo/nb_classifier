import argparse
import os
from random import sample
from typing import Dict, List
from collections import defaultdict



BASE_PATH = os.getcwd()
LING_DIR = 'lingspam_public'


def get_txt_files(path: str) -> Dict[str, str]:
    """ a list comprehension of all txt files in a folder, are applied to a map() passing each interation into get_text()
    """
    return {filename: os.path.join(dirpath, filename) for dirpath, dirs, files in os.walk(path)
    for filename in files if filename.endswith('.txt') and not filename.startswith('.')}


def get_data(adict: dict)-> Dict[str, List]:
    res = defaultdict(list)
    for filename, path in adict.items():
        if 'sp' in filename:
            res['spam'].append({'spam': {word: 'spam' for word in read_file(path)}})
        else:
            res['ham'].append({'ham': {word: 'ham' for word in read_file(path)}})
    return res


def read_file(path: str)-> List[str]:
    return [word for word in open(path).read().split(' ')]



###################################################################################################################
parser = argparse.ArgumentParser()
parser.add_argument('--f', dest='dir_path', default= BASE_PATH, required=False,  help='path to examples directory')
parser.add_argument('-B', '--bare', action='store_true', help='using bare examples')
parser.add_argument('-L', '--lemma', action='store_true', help='using lemma stop examples')

args = parser.parse_args()

if args.dir_path == BASE_PATH and os.path.exists(os.path.join(BASE_PATH, LING_DIR)):
    path = os.path.join(BASE_PATH, LING_DIR)
elif args.dir_path != BASE_PATH and os.path.exists(os.path.join(args.dir_path, LING_DIR)):
    path = os.path.join(args.dir_path, LING_DIR)
else:
    exit("\n'lingspam_public' not found")

if args.bare:
    data = get_data(get_txt_files(os.path.join(path, 'bare')))
elif args.lemma:
    data = get_data(get_txt_files(os.path.join(path, 'lemm_stop')))
else:
    exit("\nYou need to specify '--bare' | '-B' or '--lemma' | '-L' in the command.\n")
######################################################################################################################

print(data)