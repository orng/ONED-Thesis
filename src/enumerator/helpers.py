#!/usr/bin/env python

import json
import sys

import preprocessing as pre
import bag

def loadJson(filename, texts):
    """
    load the given json lines file and return an array of whatever the lines 
    contain
    """
    with open(filename, 'r') as f:
        for line in f:
            texts.append(json.loads(line))
    return texts

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

def distanceDictToString(distanceDict):
    fmtStr = u'{pair}: {distance}'
    output = ""
    if distanceDict == {}:
        return ""
    valueList = sorted(distanceDict.items(), key=lambda x: x[1])
    for (k,v) in valueList[:-1]:
        output += fmtStr.format(pair=stringify(k), distance=v)
        output += ", "
    output += fmtStr.format(pair=stringify(valueList[-1][0]), distance=valueList[-1][1])
    return output

def frozenPairToTuple(pair):
    pairList = list(pair)
    first = list(pairList[0])[0]
    second = list(pairList[1])[0]
    return (first, second)


def tfidfPairsToString(pairs, tfidfDict):
    if len(pairs) == 0:
        return "{}"
    retString = ""
    fmtString = u"{pair}: {tfidf}, "
    for pair in sorted(pairs, key=lambda x: list(x)[1]):
        p = frozenPairToTuple(pair)
        tfidf = tfidfDict[p[0]] + tfidfDict[p[1]]
        retString += fmtString.format(pair=stringify(pair), tfidf=tfidf)
    return retString


def nodeDegreesToString(nodeDegrees):
    res = ""
    formatString = u"{node}: {degree}, "
    for nodeTuple in nodeDegrees:
        res += formatString.format(node=nodeTuple[0], degree=nodeTuple[1])
    return res

def find(lst, item):
    """
    returns list of indices where item is within list
    empty list if not precent in list
    """
    return [i for i, x in enumerate(lst) if x==item]

def distanceDictFromPairs(pairList, textList):
    distDict = {}
    for pair in pairList:
        p = list(pair)
        distDict[pair] = calculateWordDistance(p[0], p[1], textList)
    return distDict

def extractString(s):
    """
    input: frozenset([frozenset([...frozenset(['somestring'])...)
    output: somestring
    """
    if type(s) in map(type, [u'', '']):
        return s
    if len(s) == 0:
        return ""
    return extractString(list(s)[0])

def calculateWordDistance(word1, word2, textList):
    word1 = extractString(word1)
    word2 = extractString(word2)
    indexes1 = find(textList, word1)
    indexes2 = find(textList, word2)
    minDist = sys.maxint 
    for i1 in indexes1:
        for i2 in indexes2:
            dist = abs(i1-i2)
            minDist = min(dist, minDist)
    return minDist

def enumerationToJsonable(enumeration):
    """
    Turns an enumeration set into datatypes that can be serialized
    Input:
        enumeration: set([frozenset['newWord'], frozenset([frozenset(['new']), frozenset(['pair'])])])
    Output:
        [(newWord,), ('new', 'pair')]
    """
    retval = []
    for item in enumeration:
        if len(item) > 1:
            newItem = [tuple(x) for x in item]
        else:
            newItem = tuple(item)
        retval.append(newItem)
    return retval


def printEnumerationJson(enumList, filename):
    """
    Input: 
        enumList: [{k:v, },]
        filename: /some/file.txt
    Output: None, prints each item as jsonline to filename
    """
    with open(filename, 'w') as f:
        for enumeration in enumList:
            enum = list(enumeration['enumeration'])
            enum = enumerationToJsonable(enum)
            enumeration['enumeration'] = enum
            jsonString = json.dumps(enumeration)
            f.write(jsonString+'\n')

def printEnumeration(url, words, enumeration, filename):
    enumerationString = enumerationToString(url, words, enumeration)
    with open(filename, 'a') as f:
        f.write(enumerationString)

def printEnumerationToFileObject(url, words, enumeration, fileobject, tfidfList):
    enumerationString = enumerationToString(url, words, enumeration, tfidfList)
    fileobject.write(enumerationString)


def enumerationToString(url, words, enumeration, tfidfList):
    lineString = u'Url: {url}\nWords: {words}\nNew Words: {newWords}\nNew Pairs: {pairs}\nNodes: {nodes}\n\n\n'#TF-IDF: {tfidf}\n\n\n================================\n'
    newWords = [x for x in enumeration if len(x) < 2]
    pairs = [x for x in enumeration if len(x) >= 2]
    tfidfDict = {x: y for (x,y) in tfidfList}
    newWords = sorted(newWords, key=lambda frozenWord: -tfidfDict[list(frozenWord)[0]])
    pairs = sorted(pairs, key=lambda frozenPair: -sum(tfidfDict[x] for x in frozenPairToTuple(frozenPair)))
    newWordStr = outputToString(newWords)
    textList = pre.to_wordlist(words)
    pairStr = outputToString(pairs)
    nodes, edges = bag.enumerationToGraph(pairs)
    nodeDegrees = bag.nodeDegrees(edges)
    nodeDegreeStr = nodeDegreesToString(nodeDegrees)
    #tfidfPairs = tfidfPairsToString(pairs, tfidfDict)
    lineString = lineString.format(
            url=url,
            words=words,
            newWords=newWordStr,
            pairs=pairStr,
            nodes=nodeDegreeStr,
            #tfidf=tfidfPairs
        )
    return lineString.encode('UTF-8')

