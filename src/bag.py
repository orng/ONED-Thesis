#!/usr/bin/env python

"""Functions for enumerating and working with bags"""

__author__ = "Orn Gudjonsson"

from preprocessing import preprocess

def bagify(string, oldbags):
    words = list(set(preprocess(string))) #remove duplicates
    retval = []
    for i in range(0, len(words)):
        for j in range(i+1, len(words)):
            current = frozenset([words[i], words[j]])
            if current not in oldbags:
                retval.append(current)
    return set(retval)

        


