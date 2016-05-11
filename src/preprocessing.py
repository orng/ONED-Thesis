#!/usr/bin/env python

"""Module containing preprocessing stuff"""

__author__ = "Orn Gudjonsson"

from math import log
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

def tokenize(text):
    return nltk.word_tokenize(text)
    

def to_wordlist(text):
    return remove_stopwords(
            stem_words(
                #remove_numbers(
                    remove_punctuation(
                        text)))#)

def get_sentences(text):
    return re.split(r' *[\.\?!\n][\'"\)\]]*\s+', text)

def to_wordlist_multi(text):
    sentences = get_sentences(text)
    return [tuple(to_wordlist(sentence)) for sentence in sentences]


def preprocess(string):
    #return remove_duplicates(to_wordlist(string))
    return to_wordlist(string)


#TODO: MOVE FOLLOWING FUNCTIONS TO OTHER MODULE
def document_frequency(wordList, docFreqDict):
    """
    Add 1 for each unique item in wordList to docFreqDict
    """
    for word in set(wordList):
        docFreqDict[word] += 1
    return docFreqDict

def collection_frequency(wordList, freqDict):
    """
    Add the number of a currances of each word to freqDict
    """
    for word in wordList:
        freqDict[word] += 1
    return freqDict

def term_frequency(wordList):
    """
    Given a list of words, returns a dict mapping words 
    to how often they appear in the list
    """
    #freqDict = defaultdict(float)
    freqDict = defaultdict(int)
    freqDict = collection_frequency(wordList, freqDict)
    #l = float(len(wordList))
    #for key, value in freqDict.iteritems():
        #freqDict[key] /= l
    return freqDict

def filter_common(wordList, frequencyDict, threshold):
    """
    Filter the word list based on the top threshold most common items 
    in the frequencyDict
    """
    freqTuples = sorted(frequencyDict.items(), key = lambda x: x[1], reverse=True)
    totalFreq = 0
    total = sum(frequencyDict.values())
    mostFrequent = []
    if total == 0:
        return []
    for i in range(int(threshold*len(frequencyDict))):
    #while totalFreq/float(total) < threshold and len(freqTuples) > 1:
        nextTuple = freqTuples[i]
        
        frequency = nextTuple[1]
        mostFrequent.append(nextTuple[0])
        totalFreq += frequency
    return mostFrequent

def filter_overThreshold(wordList, frequencyDict, threshold, seenDocuments):
    """
    Filter the word list base on the frequencyDict
    anything above the given threshold is removed
    """
    wordsToFilter = []
    if seenDocuments == 0:
        return wordsToFilter

    n = float(seenDocuments)
    for word in set(wordList):
        if frequencyDict[word]/n > threshold:
            wordsToFilter.append(word)
    return wordsToFilter
        
def filter_tfidf(wordList, dfDict, threshold, n):
    """
    Filter the given wordlist using td-idf.
    Using the document frequency dict dfDict
    Any item who's td-idf score is below threshold is ignored
    n is the number of documents
    """
    tfDict = term_frequency(wordList)
    itemsToFilter = []
    td_idf = 0
    for word in set(wordList):
        df = dfDict[word]
        if df == 0: 
            continue
        tf = log(tfDict[word] + 1.0, 2)
        idf = log(n+1/(float(df + 0.5)), 2)
        tf_idf = tf*idf
        #if tf_idf < threshold:
            #itemsToFilter.append(word)
        itemsToFilter.append((word, tf_idf))
    sortedItems = sorted(itemsToFilter, key=lambda x: x[1], reverse=True)
    #print sortedItems[:int(threshold)]
    wordsToFilter = [x[0] for x in sortedItems[int(threshold):]]
    return wordsToFilter
    #return removeListFromList(itemsToFilter, wordList)

def removeListFromList(filterList, wordList):
    return filter(lambda x: x not in filterList, wordList)

def removePairs(filterList, pairList):
    return filter(lambda s: not isSetItemInList(filterList, s), pairList)

def flattenPairSet(pairSet):
    """
    input: frozenset([frozenset(['foo']), frozenset(['bar'])])
    output: frozenset(['foo', 'bar'])
    """
    return frozenset([y for x in pairSet for y in x])

def isSetItemInList(filterList, pairSet):
    flatPairs = flattenPairSet(pairSet)
    for item in flatPairs:
        if item in filterList:
            return True
    return False


