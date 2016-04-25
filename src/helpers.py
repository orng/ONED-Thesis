#!/usr/bin/env python

import json
import sys

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
    fmtStr = '{pair}: {distance}'
    output = ""
    if distanceDict == {}:
        return ""
    valueList = sorted(distanceDict.items(), key=lambda x: x[1])
    for (k,v) in valueList[:-1]:
        output += fmtStr.format(pair=stringify(k), distance=v)
        output += ", "
    output += fmtStr.format(pair=stringify(valueList[-1][0]), distance=valueList[-1][1])
    return output


def nodeDegreesToString(nodeDegrees):
    res = ""
    formatString = "{node}: {degree}, "
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
