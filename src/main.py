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
    return sorted(texts, key=lambda d: d['date'])#[:600]#TODO: remove 300 limit

def textWithTitle(textItem):
    """
    Combines the title and text of textItem
    """
    return u"{title}\n{text}".format(title=textItem['title'], text=textItem['text'])

def enumerateTexts(texts, threshold, filterType, resultFile, useSubBags=False):
    """
    Enumerate the texts and print the results to resultFile.
    """
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

        if useSubBags:
            subBagList = pre.to_wordlist_multi(textWithTitle(text))
            flatWords = [y for x in subBagList for y in x]
            wordsToFilter, wordFrequency, tfidfList = filters.filterWordList(flatWords, wordFrequency, filterType, threshold, i)
            flatWords = set(flatWords)
            words = [set(x) for x in subBagList]
        else:
            words = pre.preprocess(textWithTitle(text))
            wordsToFilter, wordFrequency, tfidfList = filters.filterWordList(words, wordFrequency, filterType, threshold, i)
            flatWords = set(words)

        if useSubBags:
            enumeration, bagDict = bag.enumerateMultiBag(words, enumeratedBags, bagDict)
            #enumeration, bagDict = bag.enumerateMultiBagWithNeighbours(words, enumeratedBags, bagDict)
        else:
            enumeration, bagDict = bag.enumerateBag(flatWords, enumeratedBags, bagDict)
            #filtering before enumeration:
            #enumeration, bagDict = bag.enumerateBag(wordsToFilter, enumeratedBags, bagDict)

        filteredEnumeration = filters.filter_enumeration(enumeration, wordsToFilter, tfidfList)
        textCopy = dict(text)
        textCopy['enumeration'] = filteredEnumeration

        enumerations.append(textCopy)

        """
        printEnumerationToFileObject(
            text['url'],
            textWithTitle(text),
            filteredEnumeration,
            resultFileObject,
            tfidfList
        )
        """

        enumeratedBags.append(bag.getSubsets(flatWords, 1))
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

    #replace result file contents with header
    #with open(resultFile, 'w') as f:
        #s = "Initializing run\nInputFiles: {input}\nFilter: {filter}\nThreshold: {threshold}\n=======================================\n"
        #f.write(s.format(s, input=wordbanks, filter=filterType, threshold=threshold))


    enumerations, old = enumerateTexts(texts, threshold, filterType, resultFile, useSubBags)
    #print as json
    printEnumerationJson(enumerations, resultFile)


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
    parser.add_argument('-t', '--threshold', type=float, default=10)
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
