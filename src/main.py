#!/usr/bin/env python

import sys
import argparse
import time
from pprint import pprint
from collections import defaultdict
import pdb
import regex as re
from Queue import Queue 
from threading import Thread

import bag
import filters
import preprocessing as pre
from helpers import *

RESULTFILE = 'result.txt'

def loadWordbanks(wordbanks):
    """
        Input:
            wordbanks: [filepath]
        Output:
            texts: [{'text': string, 'url': string', 'date': datetime}]
            sorted in descending order by date
    """
    texts = list()
    for item in wordbanks:
        texts = loadJson(item, texts)
    return sorted(texts, key=lambda d: d['date'])[:300]#TODO: remove 300 limit

def textWithTitle(textItem):
    return u"{title}\n{text}".format(title=textItem['title'], text=textItem['text'])

def enumerateTexts(texts, threshold, filterType, resultFile,useSubBags=False):
    words = []
    enumeratedBags = []
    bagDict = {}
    old = []
    i = 0
    nodes = set([])
    edges = set([])
    wordFrequency = defaultdict(int)
    enumerations = []

    resultFileObject = open(resultFile, 'a')

    for text in texts:
        i = i+1
        sys.stdout.write("Processing: {0}/{1}".format(i, len(texts)))
        sys.stdout.flush()
        sys.stdout.write("\r")

        words = pre.preprocess(textWithTitle(text))
        wordsToFilter, wordFrequency = filters.filterWordList(words, wordFrequency, filterType, threshold, i)

        if useSubBags:
            words = pre.to_wordlist_multi(text['text'])
        words = set(words)
        if useSubBags:
            enumeration, bagDict = bag.enumerateMultiBag(words, enumeratedBags, bagDict)
        else:
            enumeration, bagDict = bag.enumerateBag(words, enumeratedBags, bagDict)

        filteredEnumeration = filters.filter_enumeration(enumeration, wordsToFilter)
        textCopy = dict(text)
        textCopy['enumeration'] = filteredEnumeration
        #enumerations.append(textCopy)
        printEnumerationThreaded(
            text['url'],
            textWithTitle(text),
            filteredEnumeration,
            resultFileObject
        )

        enumeratedBags.append(bag.getSubsets(words, 1))
        if filteredEnumeration == set([]):
            old.append(text['url'])

    sys.stdout.write("Processing: {0}/{1}\n".format(i, len(texts)))
    sys.stdout.write("Done!\n")

    resultFileObject.close()

    return enumerations, old


def main(threshold, filterType, wordbanks, resultFile=RESULTFILE, useSubBags=False):
    """
    Driver of the main stuff:
    load the wordbanks, enumerate the bags, print the results
    """
    texts = loadWordbanks(wordbanks)

    #empty result file
    with open(resultFile, 'w'):
        pass

    enumerations, old = enumerateTexts(texts, threshold, filterType, resultFile, useSubBags)
    #printEnumerationJson(enumerations, resultFile)


"""
def printEnumeration(url, words, enumeration, wordsToFilter, filename):
    lineString = u'Url: {url}\nWords: {words}\nNew Words: {newWords}\nNew Pairs: {pairs}\nNodes: {nodes}\nFiltered:{filtered}\n\n\n'
    newWords = [x for x in enumeration if len(x) < 2]
    newWords = pre.removeFilterWords(wordsToFilter, newWords)
    pairs = [x for x in enumeration if len(x) == 2]
    pairs = pre.removePairs(wordsToFilter, pairs)
    newWordStr = outputToString(newWords)
    textList = pre.to_wordlist(words)
    #distanceDict = distanceDictFromPairs(pairs, textList)
    #pairStr = distanceDictToString(distanceDict)
    pairStr = outputToString(pairs)
    nodes, edges = bag.enumerationToGraph(pairs)
    nodeStr = outputToString(list(nodes))
    nodeDegrees = bag.nodeDegrees(edges)
    nodeDegreeStr = nodeDegreesToString(nodeDegrees)
    with open(filename, 'a') as f:
        lineString = lineString.format(
                url=url,
                words=words,
                #output=outputStr,
                newWords=newWordStr,
                pairs=pairStr,
                #nodes=nodeStr,
                nodes=nodeDegreeStr,
                #edges=len(edges),
                filtered=wordsToFilter,
            )
        f.write(lineString.encode('UTF-8'))

    '''
    with open('edges.csv', 'a') as f:
        edges = [tuple(edge) for edge in edges]
        for edge in edges:
            f.write(list(edge[0])[0] + "," +list(edge[1])[0] +"\n")
    '''
"""


def massRun():
    thresholds = [x*0.1+0.05 for x in range(0,10)]
    filters = ['cf', 'df', 'tfidf', 'none']
    articles = [
                '../data/ww2.jl'
            ]
    useSubBags = [True, False]
    filenameForm = "results/ww2-{filter}-{threshold}.txt"
    for f in filters:
        for t in thresholds:
            #for s in useSubBags:
                #subBagStr = '-sub' if s else ''
                filename = filenameForm.format(filter=f, threshold=t)
                main(t, f, articles, filename, False)
                if f=='none':
                    break

    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process the provided data")
    parser.add_argument('-m', '--massRun', action='store_true')
    parser.add_argument('-s', '--subBags', action='store_true')
    parser.add_argument('-t', '--threshold', type=float, default=0.10)
    parser.add_argument('-f', '--filter', default='none')
    parser.add_argument('-o', '--output', default=RESULTFILE)
    parser.add_argument('articles', nargs='*')
    args = parser.parse_args()
    if args.massRun:
        massRun()
    else:
        startTime = time.time()
        main(
                args.threshold,
                args.filter,
                args.articles,
                resultFile=args.output,
                useSubBags=args.subBags
            )
        endTime = time.time()
        print "Completed in {time}s.".format(time=endTime-startTime)
