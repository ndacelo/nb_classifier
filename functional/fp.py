import sys
sys.path.append('../')
from random import sample
from collections import defaultdict
from math import log
from utils import *


def fit(data):
    """
    """
    return probability(word_count(data))


def predict(training, email):
    """
    """
    
    l = len(training['ham']) + len(training['spam'])
    p_ham = len(training['ham']) / l
    p_spam = 1 - p_ham
    
    res = defaultdict(int)
    res['spam'] = p_spam
    res['ham'] = p_ham
    for word in email:
        for label in training:
            if word in training[label]:
                res[label] += training[label][word]
            else:
                res[label] +=  log( 1 / len(training[label]))
                training[label][word] = log(1  / len(training[label]) )
    ham = res['ham'] + p_ham
    spam = res['spam'] + p_spam
    return 'spam' if spam > ham else 'ham'


def score(training, testing):
    """
    """
    correct = 0
    for tuple in testing:
        email, label = tuple
        if label == predict(training, email):
            correct += 1
    return correct / len(testing)


training, testing = split_data(sample(data, len(data)))

total = 0
for x in range(iterations):
    total += score(fit(training), testing)
print(total/iterations)

