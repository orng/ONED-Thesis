#!/usr/bin/env python

"""Module containing preprocessing stuff"""

__author__ = "Orn Gudjonsson"

from stemming.porter2 import stem
import nltk
from nltk.corpus import stopwords
#import regex as re
import string


def stem_words(wordlist):
    """
    Given a string returns a list of all the words, stemmed.
    """
    return [stem(x).lower() for x in wordlist]
    #return [stem(x.lower()) for x in string.split()]
    #return [x.lower() for x in string.split()]

def remove_stopwords(words):
    """
    Given a list of english words returns the list with all stopwords removed.
    """
    swords = set(stopwords.words('english'))
    return [x for x in words if x not in swords]

def remove_duplicates(words):
    return list(set(words))

def remove_punctuation(text):
    """
    Input:
        unicode text
    Ouput:
        unicode text with removed punctuation
    """
    table = {ord(c): u'' for c in string.punctuation}
    return text.translate(table)
    #return text.translate(None, string.punctuation)
    #return re.sub(ur"\p{P}+", " ", text)

def remove_numbers(words):
    return filter(lambda x: not x.isdigit(), words)

def tokenize(text):
    """
    Given a string outputs a list of words
    """
    return nltk.word_tokenize(text)
    

def to_wordlist(text):
    return remove_stopwords(
            stem_words(
                tokenize(
                #remove_numbers(
                    remove_punctuation(
                        text))))#)

def get_sentences(text):
    return nltk.sent_tokenize(text)

def to_wordlist_multi(text):
    sentences = get_sentences(text)
    return [tuple(to_wordlist(sentence)) for sentence in sentences]


def preprocess(string):
    #return remove_duplicates(to_wordlist(string))
    return to_wordlist(string)
