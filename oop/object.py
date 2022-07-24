import argparse
import os
import sys
from math import log
from random import sample


sys.path.append('../')
from functional.fp import (
    get_data, get_txt_files, 
    split_data
)
PATH = '../data/lingspam_public'


class Classifier():

    def __init__(self) -> None:
        pass

    def word_counter(self):
        pass

    def fit(self):
        pass

    def predict(self):
        pass

    def score(self):
        pass



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

# training, testing = split_data(sample(data, len(data)))
# total = 0
for x in range(iterations):
    classifier = Classifier(data)
    classifier.score()
#     total += classifier.score(fit(training), testing)
# print(total/iterations)
