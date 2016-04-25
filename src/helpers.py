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

def stringify(s, textList):
    """Converts a set to string"""
    if type(s) not in map(type, [set([]), frozenset([])]):
        return unicode(s)
    l = list(s)
    isMultiSet = len(l) > 1
    if isMultiSet:
        retStr = "("
        for item in l[:-1]:
            retStr += stringify(item, textList) + ', '
        retStr += stringify(l[-1], textList)
        retStr += ")"
        if len(l) == 2:
            #TODO: deal with larger tuples than pairs?
            distance = calculateWordDistance(l[0], l[1], textList)
            retStr += ": " + str(distance)
    else:
        retStr = ""
        retStr += stringify(l[0], textList)
    return retStr

def outputToString(output, textList):
    """Converts a list of sets to string"""
    if output == []:
        return "{}"
    retStr = ''
    for item in output[:-1]:
        retStr += stringify(item, textList) + ', '
    retStr += stringify(output[-1], textList)
    return '{' + retStr + '}'

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
