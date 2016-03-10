#!/usr/bin/env python

import json
import sys
from pprint import pprint

import bag
from preprocessing import preprocess

RESULTFILE = 'result.txt'

def loadJson(filename, texts):
    with open(filename, 'r') as f:
        for line in f:
            texts.append(json.loads(line))
    return texts
    

def main():
    texts = list()
    #wordbanks = ['nba/fox.jl', 'nba/nba.jl']
    wordbanks = [
            'nba/reuters.jl', 
            'nba/cbs.jl', 
            'nba/pbs.jl',
            #'nba/politico.jl',
            #'processedLong.jl',
        ]
    for item in wordbanks:
        texts = loadJson(item, texts)
    texts = sorted(texts, key=lambda d: d['date'])

    #empty result file
    with open(RESULTFILE, 'w'):
        pass

    #with open('nba/processed.jl', 'r') as f:
        #texts = json.loads(f.read())

    words = []
    enumeratedBags = []
    bagDict = {}
    old = []
    i = 0
    nodes = set([])
    edges = set([])
    for text in texts:
        i = i+1
        sys.stdout.write("Processing: {0}/{1}".format(i, len(texts)))
        sys.stdout.flush()
        sys.stdout.write("\r")

        words = preprocess(text['text'])
        enumeration, bagDict = bag.enumerateBag(words, enumeratedBags, bagDict)

        printEnumeration(text['url'], text['text'], enumeration)

        enumeratedBags.append(bag.getSubsets(words, 1))
        if enumeration == set([]):
            old.append(text['url'])

    sys.stdout.write("Processing: {0}/{1}\n".format(i, len(texts)))
    sys.stdout.write("Done!\n")

    pprint(old)


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


def printEnumeration(url, words, enumeration):
    #lineString = u'Url: {url}\nWords: {words}\nOutput: {output}\n\n'
    lineString = u'Url: {url}\nWords: {words}\nNew Words: {newWords}\nNew Pairs: {pairs}\nNodes: {nodes}\nNr. of Edges: {edges}\n\n\n'
    #outputStr = outputToString(list(enumeration))
    newWords = [x for x in enumeration if len(x) < 2]
    pairs = [x for x in enumeration if len(x) == 2]
    newWordStr = outputToString(newWords)
    pairStr = outputToString(pairs)
    nodes, edges = bag.enumerationToGraph(enumeration)
    nodeStr = outputToString(list(nodes))
    with open(RESULTFILE, 'a') as f:
        lineString = lineString.format(
                url=url,
                words=words,
                #output=outputStr,
                newWords=newWordStr,
                pairs=pairStr,
                nodes=nodeStr,
                edges=len(edges),
            )
        f.write(lineString.encode('UTF-8'))

    

if __name__ == '__main__':
    main()
