#!/usr/bin/env python

"""Module containing preprocessing stuff"""

__author__ = "Orn Gudjonsson"

from stemming.porter2 import stem
from nltk.corpus import stopwords

def stem_words(string):
    """
    Given a string returns a list of all the words, stemmed.
    """
    return [stem(x.lower()) for x in string.split()]

def remove_stopwords(words):
    """
    Given a list of english words returns the list with all stopwords removed.
    """
    swords = set(stopwords.words('english'))
    return [x for x in words if x not in swords]


