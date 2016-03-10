#!/usr/bin/env python

"""Functions for enumerating and working with bags"""

__author__ = "Orn Gudjonsson"

inf = float("+inf")

def getSubsets(x, n):
    """
    Given a set or a list returns all possible subsets of size n
    """
    if n == 1:
        return set([frozenset([i]) for i in x])

    subsets = []
    for item in x:
        for y in getSubsets(x, n-1):
            subset = y | frozenset([item])
            if len(subset) == n:
                subsets.append(subset)
    return set(subsets)

def f(x, bags):
    i = 1
    for bag in bags:
        if isSubset(x, bag):
            return i
        i = i+1

def isNewAtM(x, bags, bagDict, m):
    if bagDict.get(x, inf) < m:
        return False

    retval = True
    fval = f(x, bags)
    if fval is not None:
        yvalMin = inf
        for y in x:
            yval = bagDict.get(y, inf)
            if yval < inf and isSubset(x, bags[yval-1]):
                retval =  False
                yvalMin = min(yvalMin, yval)
        #store f(X) which equals the smallest f(y)
        bagDict[x] = yvalMin
    return retval 

    
def isSubset(a,b):
    return a-b == set([])

def enumerateBagHelper(x, bags, bagDict, n, i):
    newSets = []
    subsets = getSubsets(x, n)
    for subset in subsets:
        if isNewAtM(subset, bags, bagDict, i):
            newSets.append(subset)
            #i = f(subset, enumeratedBags) if i is not None
            bagDict[subset] = i
    return set(newSets)

def enumerateBag(newBag, bags, bagDict):
    """
    Performs enumeration using the algorithm described in section 2.2

    Args: 
        newBag: a list of words to enumerate 
            :: [string]
        bags:  a list of previously seen bags. Each bag is a set of frozensets
            :: [set([frozenset([string])]]
        bagDict: a dictionary mapping previously seen sets to the bag nr
                (1-indexed) where they were first seen.
            :: dict(frozenset([string])) | dict(frozenset([frozenset([string])))
    """
    enumeration = set([])
    #TODO: do the "stop as soon as all further X would be supersets.." thing
    for n in range(1, 3):
        enumeration = enumeration | enumerateBagHelper(newBag, bags, bagDict, n, len(bags) + 1)
        newBag = getSubsets(newBag, n) - enumeration
        if newBag == set([]):
            break
    return (enumeration, bagDict)

def enumerate(bags):
    """
    Enumerates a list of 'bags'
    """
    enumeratedBags = []
    bagDict = {}
    i = 1
    for bag in bags:
        newEnumeration, bagDict = enumerateBag(bag, enumeratedBags, bagDict, i)
        enumeratedBags.append(newEnumeration)
        i = i+1
    return enumeratedBags, bagDict

def enumerationToGraph(enumeration):
    """Given an enumeration (a set of frozensets with one or two elements)
    returns the set of nodes (words involved in pairs) and the set of edges
    (pairs)
    """
    pairs = [x for x in enumeration if len(x) > 1];
    #nodes are the words that are involved in pairs
    nodes = set([])
    for pair in pairs:
        for elem in pair:
            nodes.add(elem)
    return nodes, set(pairs)


