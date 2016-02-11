#!/usr/bin/env python

"""Module containing preprocessing stuff"""

__author__ = "Orn Gudjonsson"

from stemming.porter2 import stem
from nltk.corpus import stopwords
import regex as re

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

def remove_duplicates(words):
    return list(set(words))

def remove_punctuation(text):
        return re.sub(ur"\p{P}+", "", text)

def preprocess(string):
    return remove_duplicates(
            remove_stopwords(
                stem_words(
                    remove_punctuation(
                        string))))
