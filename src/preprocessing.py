#!/usr/bin/env python

"""Module containing preprocessing stuff"""

__author__ = "Orn Gudjonsson"

from collections import defaultdict
from stemming.porter2 import stem
from nltk.corpus import stopwords
import regex as re

def stem_words(string):
    """
    Given a string returns a list of all the words, stemmed.
    """
    return [stem(x.lower()) for x in string.split()]
    #return [x.lower() for x in string.split()]

def remove_stopwords(words):
    """
    Given a list of english words returns the list with all stopwords removed.
    """
    swords = set(stopwords.words('english'))
    return [x for x in words if x not in swords]

def remove_duplicates(words):
    return list(set(words))

def remove_punctuation(text):
        return re.sub(ur"\p{P}+", " ", text)

def remove_numbers(words):
    return filter(lambda x: not x.isdigit(), words)
    

def to_wordlist(string):
    return remove_stopwords(
            stem_words(
                remove_numbers(
                    remove_punctuation(
                        string))))


def preprocess(string):
    return remove_duplicates(to_wordlist(string))



def word_frequency(wordList):
    """
    Given a list of words, returns a dict mapping words 
    to how often they appear in the list
    """
    freqDict = defaultdict(int)
    for word in wordList:
        freqDict[word] += 1
    return freqDict

def filter_common(wordList, frequencyDict, n):
    frequencyTuples = sorted(frequencyDict.items(), key = lambda x: x[1])
    totalCount = sum(frequencyDict.values())
    freqList = [(x, y/float(totalCount)) for (x,y) in frequencyTuples]
    totalFreq = 0
    mostFrequent = []
    #TODO: perhaps limit to a certain amount of elements in mostFrequent
    while totalFreq < n and len(freqList) > 1:
        nextTuple = freqList[0]
        mostFrequent.append(nextTuple[0])
        totalFreq += nextTuple[1]
        freqList = freqList[1:]
    return filter(lambda x: x in mostFrequent, wordList)
        


        




