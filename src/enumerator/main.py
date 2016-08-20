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
    return sorted(texts, key=lambda d: d['date'])#[:600]#TODO: remove limit

def textWithTitle(textItem):
    """
    Combines the title and text of textItem if a title exists
    """
    if 'title' in textItem:
        return u"{title}\n{text}".format(title=textItem['title'], text=textItem['text'])
    else:
        return textItem['text']

def enumerateTexts(
        texts,
        threshold,
        filterType,
        resultFile,
        useSubBags=False,
        printToJson=False,
        preFilter=False,
        useNeighbours=False):
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

    startTime = time.time()
    for text in texts:
        i = i+1
        sys.stdout.write("Processing: {0}/{1}".format(i, len(texts)))
        sys.stdout.flush()
        sys.stdout.write("\r")

        if useSubBags:
            subBagList = pre.to_wordlist_multi(textWithTitle(text))
            flatWords = [y for x in subBagList for y in x]
            wordsToFilter, wordFrequency, tfidfList = filters.filterWordList(flatWords, wordFrequency, filterType, threshold, i)
            words = [set(x) for x in subBagList]
        else:
            words = pre.preprocess(textWithTitle(text))
            wordsToFilter, wordFrequency, tfidfList = filters.filterWordList(words, wordFrequency, filterType, threshold, i)
            words = set(words)

        if useSubBags:
            if useNeighbours:
                enumeration, bagDict = bag.enumerateMultiBagWithNeighbours(words, enumeratedBags, bagDict)
            else:
                enumeration, bagDict = bag.enumerateMultiBag(words, enumeratedBags, bagDict)
        else:
            if preFilter:
                enumeration, bagDict = bag.enumerateBag(wordsToFilter, enumeratedBags, bagDict)
            else:
                enumeration, bagDict = bag.enumerateBag(words, enumeratedBags, bagDict)

        filteredEnumeration = filters.filter_enumeration(enumeration, wordsToFilter, tfidfList)
        textCopy = dict(text)
        textCopy['enumeration'] = filteredEnumeration

        if printToJson:
            enumerations.append(textCopy)

        printEnumerationToFileObject(
            text['url'],
            textWithTitle(text),
            filteredEnumeration,
            resultFileObject,
            tfidfList
        )

        if useSubBags:
            enumeratedBags.append([bag.getSubsets(x, 1) for x in words])
        else:
            enumeratedBags.append(bag.getSubsets(words, 1))

        if filteredEnumeration == set([]):
            old.append(text['url'])

    endTime = time.time()
    sys.stdout.write("Processing: {0}/{1}\n".format(i, len(texts)))
    sys.stdout.write("Done!\n")
    sys.stdout.write("Completed in {time}s.".format(time=endTime-startTime))

    resultFileObject.close()

    return enumerations, old


def main(threshold,
        filterType,
        wordbanks,
        resultFile=RESULTFILE,
        useSubBags=False,
        printJson=False,
        useNeighbours=False,
        preFilter=False):
    """
    Driver of the main stuff:
    load the wordbanks, enumerate the bags, print the results
    """
    texts = loadWordbanks(wordbanks)

    #replace result-file contents with header
    with open(resultFile, 'w') as f:
        s = "Initializing run\nInputFiles: {input}\nFilter: {filter}\nThreshold: {threshold}\nPre-filter: {preFilter}\nSubBags: {useSubBags}\nNeighbours: {useNeighbours}\n=======================================\n"
        f.write(
            s.format(
                input=wordbanks,
                filter=filterType,
                threshold=threshold,
                preFilter = preFilter,
                useSubBags = useSubBags,
                useNeighbours = useNeighbours,
            )
        )


    enumerations, old = enumerateTexts(
            texts,
            threshold,
            filterType,
            resultFile,
            useSubBags,
            printJson,
            preFilter,
            useNeighbours)

    #print as json
    if printJson:
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
    parser.add_argument('-n', '--neighbours', action='store_true')
    parser.add_argument('-t', '--threshold', type=float, default=10)
    parser.add_argument('-f', '--filter', default='none')
    parser.add_argument('-p', '--preFilter', default='none')
    parser.add_argument('-j', '--printToJson', default='none')
    parser.add_argument('-o', '--output', default=RESULTFILE)
    parser.add_argument('articles', nargs='*')
    args = parser.parse_args()

    if args.massRun:
        massRun()
    else:
        main(
                args.threshold,
                args.filter,
                args.articles,
                resultFile=args.output,
                useSubBags=args.subBags,
                useNeighbours=args.neighbours,
                printToJson=args.printToJson,
                preFilter=args.preFilter
            )
