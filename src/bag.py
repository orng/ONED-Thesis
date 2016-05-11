#!/usr/bin/env python

"""Functions for enumerating and working with bags"""

__author__ = "Orn Gudjonsson"

from collections import defaultdict

inf = float("+inf")

def getSubsets(x, n):
    """
    Given a set or a list returns all possible subsets of size n
    """
    if n == 1:
        return frozenset([frozenset([i]) for i in x])

    subsets = []
    for item in x:
        for y in getSubsets(x, n-1):
            subset = y | frozenset([item])
            if len(subset) == n:
                subsets.append(subset)
    return frozenset(subsets)

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

def isMultiSubset(a,b):
    for subbag in b:
        if a-subbag == set([]):
            return True
    return False

def enumerateBagHelper(newBag, bags, bagDict, n, i):
    newSets = []
    subsets = getSubsets(newBag, n)
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

def enumerateMultiBag(newBags, bags, bagDict):
    enumeration = set([])
    #Store the isSubset function in variable and replace it in module
    tempIsSubset = globals()['isSubset']
    globals()['isSubset'] = isMultiSubset
    try:
        for n in range(1,3):
            for subBag in newBags:
                enumeration = enumeration | enumerateBagHelper(subBag, bags, bagDict, n, len(bags) + 1)
            newBags = [getSubsets(x, n) - enumeration for x in newBags]
            if newBags == set([]):
                break
    finally:
        #Restore isSubset
        globals()['isSubset'] = tempIsSubset
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

def enumerationToGraph(pairs):
    """Given an enumeration (a set of frozensets with one or two elements)
    returns the set of nodes (words involved in pairs) and the set of edges
    (pairs)
    """
    #nodes are the words that are involved in pairs
    nodes = set([])
    for pair in pairs:
        for elem in pair:
            nodes.add(elem)
    return nodes, set(pairs)

def nodeDegrees(edges):
    """
    Given a set of eges, return a list of tuples where
    the first element is a node and the second is the degree of that node,
    that is the number of edges it is included in

    Input:
        edges: a set of edges on the form 
            frozenset([frozenset([a]), frozenset([b])])

    Ouput:
        a list of tuples [(word, degree)]
    """
    vertices = defaultdict(int)
    for edge in edges:
        for vertex in edge:
            vertices[list(vertex)[0]] += 1

    return sorted(zip(vertices.keys(), vertices.values()), key=lambda x: x[1], reverse=True)

