import sys
sys.path.append('../')
from math import log
from random import sample
from collections import defaultdict
from utils import *


class Classifier():

    def __init__(self, data) -> None:
        self.data = sample(data, len(data))
        self.training = self.data[:len(data) // 2]
        self.testing = self.data[len(data) // 2:]

    def fit(self):
        """
        """
        self.prob =  defaultdict(dict)
        self.prob['spam']
        self.prob['ham']
        for d in self.training:
            email, label = d
            for word in email:
                if word in self.prob[label]:
                    self.prob[label][word] += 1
                else:
                    self.prob[label][word] = 1
        for label, d in self.prob.items():
            for word, occ in d.items():
                self.prob[label][word]\
                    = log( (occ + 1) / len(self.prob[label]))


    def predict(self, email):
        
        l = len(self.prob['ham']) + len(self.prob['spam'])
        p_ham = len(self.prob['ham']) / l
        p_spam = 1 - p_ham 

        res = defaultdict(int)
        res['spam'] = p_spam
        res['ham'] = p_ham
        for word in email:
            for label in self.prob:
                if word in self.prob[label]:
                    res[label] += self.prob[label][word]
                else:
                    res[label] +=  log( 1 / len(self.prob[label]))
                    self.prob[label][word] = log(1  / len(self.prob[label]) )
        ham = res['ham'] + p_ham
        spam = res['spam'] + p_spam
        return 'spam' if spam > ham else 'ham'


    def score(self):
        """
        
        """
        correct = 0
        for tuple in self.testing:
            email, label = tuple
            if label == self.predict(email):
                correct += 1
        return correct / len(self.testing)


total = 0
for x in range(iterations):
    classifier = Classifier(data)
    classifier.fit()
    total += classifier.score()
print(total/iterations)

