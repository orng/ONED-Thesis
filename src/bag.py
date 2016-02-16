#!/usr/bin/env python

"""Functions for enumerating and working with bags"""

__author__ = "Orn Gudjonsson"

from preprocessing import preprocess

def bagify(string, oldbags):
    words = list(set(preprocess(string))) #remove duplicates
    unique = []
    for i in range(0, len(words)):
        for j in range(i+1, len(words)):
            current = frozenset([words[i], words[j]])
            if not inOldBags(current,oldbags):
                unique.append(current)
    minSet = set(unique)
    if minSet is not set([]):
        oldbags.append(minSet)
    return (minSet, oldbags)

def inOldBags(item, oldbags):
    for bag in oldbags:
        if item in bag:
            return True
    return False
