#!/usr/bin/env python

"""Filters and filter helper functions"""

__author__ = "Orn Gudjonsson"

from math import log
from collections import defaultdict

def filterWordList(words, wordFrequency, filterType, threshold, docuCount):
    """
        Input:
            words: the list of words to filter
            wordFrequency: a dictionary counting the document frequency of words
            filterType: the type of filtering to use
            threshold: the threshold to use for filtering
            docuCount: the number of documents previously seen
        Output: 
            wordsToFilter: words that should be filtered based on filterType and 
                           threshold
            wordFrequency: updated dictionary with document frequencies
    """
    wordsToFilter = []
    if filterType == 'cf':
        wordsToFilter = filter_common(words, wordFrequency, threshold)
        wordFrequency  = collection_frequency(words, wordFrequency)
    elif filterType == 'df':
        wordsToFilter = filter_overThreshold(words, wordFrequency, threshold, docuCount-1)
        wordFrequency = document_frequency(words, wordFrequency)
    elif filterType == 'tfidf':
        wordsToFilter = filter_tfidf(words, wordFrequency, threshold, docuCount)
        wordFrequency = document_frequency(words, wordFrequency)
    elif filterType == 'none':
        pass
    else:
        raise Exception("Invalid filter type" + filterType)

    return wordsToFilter, wordFrequency

def filter_enumeration(enumeration, whitelist):
    words = [x for x in enumeration if len(x) == 1]
    pairs = [x for x in enumeration if len(x) > 1]
    retWords = removeWords(whitelist, words)
    retPairs = removePairs(whitelist, pairs)
    return retWords + retPairs


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
    to how often they appear in the list in proportion to the length of the
    wordlist.
    """
    #TODO: speed up with custom function to only traverse list once maybe?
    freqDict = defaultdict(float)
    freqDict = collection_frequency(wordList, freqDict)
    l = float(len(wordList))
    for key, value in freqDict.iteritems():
        freqDict[key] /= l
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
        

def tfidf(word, termFrequencies, docFrequencies, docNumber):
    """
    Input:
        word: "someword"
        termFrequencies: {"someword": 0.3, "someotherword": 0.7}
        docFrequencies: {"someword": 40, "otherword": 10, "foo": 1}
        docNumber: 50
    Ouput:
        the tf-idf of word, i.e. 0.4
    """
    df = docFrequencies[word]
    tf = log(termFrequencies[word] + 1.0, 2)
    idf = log(docNumber+1/(float(df + 0.5)), 2)
    return tf*idf


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
        #if df == 0: 
            #continue
        tf = log(tfDict[word] + 1.0, 2)
        idf = log(n+1/(float(df + 0.5)), 2)
        #tf_idf = tfidf(word, tfDict, dfDict, n)
        tf_idf = tf*idf
        #if tf_idf < threshold:
            #itemsToFilter.append(word)
        itemsToFilter.append((word, tf_idf))
    sortedItems = sorted(itemsToFilter, key=lambda x: x[1], reverse=True)
    #print sortedItems[:int(threshold)]
    wordsToFilter = [x[0] for x in sortedItems[:int(threshold)]]
    return wordsToFilter
    #return removeListFromList(itemsToFilter, wordList)


def removeListFromList(filterList, wordList):
    return filter(lambda x: x not in filterList, wordList)

def removeFilterWords(filterList, wordList):
    """
    input: 
        filterList: ['foo', 'baz']
        wordList: [frozenset(['foo']), frozenset(['bar'])]
    output: ['bar']
    """
    words = [y for x in wordList for y in x]
    return removeListFromList(filterList, words)

def removeWords(whitelist, wordList):
    """
    input: 
        filterList: ['foo', 'baz']
        wordList: [frozenset(['foo']), frozenset(['bar'])]
    output: [frozenset(['bar'])]
    """
    filterSetList = [frozenset([x]) for x in whitelist]
    return filter(lambda x: x in filterSetList, wordList)

def removePairs(whitelist, pairList):
    return filter(lambda s: isSetItemInList(whitelist, s), pairList)

def flattenPairSet(pairSet):
    """
    input: frozenset([frozenset(['foo']), frozenset(['bar'])])
    output: frozenset(['foo', 'bar'])
    """
    return frozenset([y for x in pairSet for y in x])

def isSetItemInList(filterList, pairSet):
    """
    input: 
        pairSet: frozenset([frozenset(['foo']), frozenset(['bar'])])
        filterList = ['foo', 'baz']
    output: 
        true if an item in filterlist is in any subset of pairset
        false otherwise
    """
    flatPairs = flattenPairSet(pairSet)
    for item in flatPairs:
        if item in filterList:
            return True
    return False


