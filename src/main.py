#!/usr/bin/env python

import json
import sys
import argparse
from pprint import pprint
from collections import defaultdict

import bag
import preprocessing as pre

RESULTFILE = 'result.txt'

def loadJson(filename, texts):
    with open(filename, 'r') as f:
        for line in f:
            texts.append(json.loads(line))
    return texts
    

def main(threshold, filterType, wordbanks):
    texts = list()
    #wordbanks = ['articles/fox.jl', 'articles/articles.jl']
    """wordbanks = [
            'articles/reuters.jl', 
            'articles/cbs.jl', 
            'articles/pbs.jl',
            #'articles/politico.jl',
            #'processedLong.jl',
            #'history.jl',
            #'ww2.jl',
        ]"""
    for item in wordbanks:
        texts = loadJson(item, texts)
    texts = sorted(texts, key=lambda d: d['date'])

    #empty result file
    with open(RESULTFILE, 'w'):
        pass

    words = []
    enumeratedBags = []
    bagDict = {}
    old = []
    i = 0
    nodes = set([])
    edges = set([])
    wordFrequency = defaultdict(int)
    for text in texts:
        i = i+1
        sys.stdout.write("Processing: {0}/{1}".format(i, len(texts)))
        sys.stdout.flush()
        sys.stdout.write("\r")

        words = pre.preprocess(text['text'])
        if filterType == 'cf':
            uncommonWords = pre.filter_common(words, wordFrequency, threshold)
            wordFrequency  = pre.collection_frequency(words, wordFrequency)
        elif filterType == 'df':
            uncommonWords = pre.filter_common(words, wordFrequency, threshold)
            wordFrequency = pre.document_frequency(words, wordFrequency)
        elif filterType == 'tfidf':
            wordFrequency = pre.document_frequency(words, wordFrequency)
            uncommonWords = pre.filter_tfidf(words, wordFrequency, threshold, i)
        else:
            raise Exception("Invalid filter type" + filterType)

        #wordFrequency = pre.collection_frequency(words, wordFrequency)
        #uncommonWords = pre.filter_tfidf(words, wordFrequency, 0.5, i)
        #uncommonWords = pre.filter_common(words, wordFrequency, threshold)
        #wordFrequency = pre.document_frequency(words, wordFrequency)
        words = set(words)
        uncommonWords = set(uncommonWords)
        filteredWords = [x for x in words if x not in uncommonWords]
        enumeration, bagDict = bag.enumerateBag(uncommonWords, enumeratedBags, bagDict)

        printEnumeration(text['url'], text['text'], enumeration, filteredWords)

        enumeratedBags.append(bag.getSubsets(words, 1))
        if enumeration == set([]):
            old.append(text['url'])

    sys.stdout.write("Processing: {0}/{1}\n".format(i, len(texts)))
    sys.stdout.write("Done!\n")
    print(old)
    #totalCount = sum([x[1] for x in wordFrequency.items()])
    #frequencyTuples = sorted([(x, y/float(totalCount)) for (x,y) in wordFrequency.items()], key = lambda x: x[1], reverse=True)
    #pprint(frequencyTuples[:30])


def stringify(s):
    """Converts a set to string"""
    if type(s) not in map(type, [set([]), frozenset([])]):
        return unicode(s)
    l = list(s)
    isMultiSet = len(l) > 1
    if isMultiSet:
        retStr = "("
        for item in l[:-1]:
            retStr += stringify(item) + ', '
        retStr += stringify(l[-1])
        retStr += ")"
    else:
        retStr = ""
        retStr += stringify(l[0])
    return retStr


def outputToString(output):
    """Converts a list of sets to string"""
    if output == []:
        return "{}"
    retStr = ''
    for item in output[:-1]:
        retStr += stringify(item) + ', '
    retStr += stringify(output[-1])
    return '{' + retStr + '}'

def nodeDegreesToString(nodeDegrees):
    res = ""
    formatString = "{node}: {degree}, "
    for nodeTuple in nodeDegrees:
        res += formatString.format(node=nodeTuple[0], degree=nodeTuple[1])
    return res


def printEnumeration(url, words, enumeration, filteredWords):
    #lineString = u'Url: {url}\nWords: {words}\nOutput: {output}\n\n'
    lineString = u'Url: {url}\nWords: {words}\nNew Words: {newWords}\nNew Pairs: {pairs}\nNodes: {nodes}\nFiltered:{filtered}\n\n\n'
    #outputStr = outputToString(list(enumeration))
    newWords = [x for x in enumeration if len(x) < 2]
    pairs = [x for x in enumeration if len(x) == 2]
    newWordStr = outputToString(newWords)
    pairStr = outputToString(pairs)
    nodes, edges = bag.enumerationToGraph(enumeration)
    nodeStr = outputToString(list(nodes))
    nodeDegrees = bag.nodeDegrees(edges)
    nodeDegreeStr = nodeDegreesToString(nodeDegrees)
    with open(RESULTFILE, 'a') as f:
        lineString = lineString.format(
                url=url,
                words=words,
                #output=outputStr,
                newWords=newWordStr,
                pairs=pairStr,
                #nodes=nodeStr,
                nodes=nodeDegreeStr,
                #edges=len(edges),
                filtered=filteredWords,
            )
        f.write(lineString.encode('UTF-8'))

    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process the provided data")
    parser.add_argument('-t', '--threshold', type=float, default=0.10)
    parser.add_argument('-f', '--filter', default='cf')
    parser.add_argument('articles', nargs='+')
    args = parser.parse_args()
    main(args.threshold, args.filter, args.articles)
