#!/usr/bin/env python

"""Functions for enumerating and working with bags"""

__author__ = "Orn Gudjonsson"

def bagify(words, oldbags):
    unique = []
    i = 1
    for word in words[:-1]:
        #we can skip the last word
        for otherword in words[i:]:
            current = frozenset([word, otherword])
            if not inOldBags(current, oldbags):
                unique.append(current)
        i = i+1

    minSet = set(unique)
    if minSet is not set([]):
        oldbags.append(minSet)
    return (minSet, oldbags)

def bagify2(words, oldbags):
    """
    Does the same as bagify only here oldbags is a set of pairs instead of a list of sets
    """
    newWords = set([])
    oldWords = []
    newPairs = []
    i = 1
    for word in words:
        if word in oldbags[0]:
            oldWords.append(word)
        else:
            newWords.add(word)
            
    for word in oldWords[:-1]:
        #we can skip the last word
        for otherword in words[i:]:
            current = frozenset([word, otherword])
            if current not in  oldbags:
                newPairs.append(current)
        i = i+1

    minSet = set(unique)
    if minSet is not set([]):
        oldbags = oldbags | minSet
    return (minSet, oldbags)
    

def inOldBags(item, oldbags):
    for bag in oldbags:
        if item in bag:
            return True
    return False
