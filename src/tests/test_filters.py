#!/usr/bin/env python

"""Tests for the filters module"""

__author__ = "Orn Gudjonsson"

import unittest
from collections import defaultdict

from enumerator import filters

class FiltersTests(unittest.TestCase):
    def test_term_frequency(self):
        words = ['dog', 'cat', 'cow', 'dog', 'cat', 'dog']
        expected = {
                'dog': 3/6.0,
                'cat': 2/6.0,
                'cow': 1/6.0,
                }
        result = filters.term_frequency(words)
        self.assertEqual(expected, result)

    def test_document_frequency(self):
        d1 = ['dog', 'cow', 'dog']
        d2 = ['cat', 'dog', 'cat']
        expected = {
                'dog': 2,
                'cat': 1,
                'cow': 1,
                }
        r1 = filters.document_frequency(d1, defaultdict(int))
        r2 = filters.document_frequency(d2, r1)
        self.assertEqual(expected, r2)

    def test_collection_frequency(self):
        d1 = ['dog', 'cow', 'dog']
        d2 = ['cat', 'dog', 'cat']
        expected = {
                'dog': 3,
                'cat': 2,
                'cow': 1,
                }
        r1 = filters.collection_frequency(d1, defaultdict(int))
        r2 = filters.collection_frequency(d2, r1)
        self.assertEqual(expected, r2)

    def test_tfidf(self):
        d1 = ['dog']
        d2 = ['dog', 'cat', 'cat', 'cat']
        df = filters.document_frequency(d1, defaultdict(int))
        tf = filters.collection_frequency(d2, defaultdict(int))
        expected = 3.295836866004329
        result = filters.tfidf('cat', tf, df, 2)
        self.assertEqual(expected, result)

    def test_filter_tfidf(self):
        d1 = ['dog']
        d2 = ['dog', 'cat', 'cat', 'cat']
        df = filters.document_frequency(d1, defaultdict(int))
        expected = ['cat']
        result, tfidfList = filters.filter_tfidf(d2, df, 1, 2)
        self.assertEqual(expected, result)


    def test_filter_common(self):
        dogs = ['dog' for i in range(10)]
        cats = ['cat' for i in range(5)]
        rest = ['cow', 'chicken', 'pig']
        animals = dogs + cats + rest
        expected = ['dog', 'cat']
        expectedFreqList = [('dog', 10), ('cat', 5), ('cow', 1), ('chicken', 1), ('pig', 1)]
        wordFreq = filters.collection_frequency(animals, defaultdict(int))
        result, freqList = filters.filter_common(animals, wordFreq, 2)
        self.assertEqual(expected, result)
        self.assertEqual(set(expectedFreqList), set(freqList))

    def test_filter_documentFrequency(self):
        words = ['dog', 'cat', 'chicken']
        freqDict = defaultdict(int)
        freqDict['dog'] = 1
        freqDict['cat'] = 6
        freqDict['cow'] = 4
        freqDict['chicken'] = 2
        expected = ['dog', 'chicken']
        wordFreq = filters.document_frequency(words, freqDict)
        result, freqList = filters.filter_documentFrequency(words, wordFreq, 2)
        self.assertEqual(expected, result)

    def test_filter_overThreshold_firstItem(self):
        df = defaultdict(int)
        words = ['dog', 'cat']
        expected = []
        result = filters.filter_overThreshold(words, df, 0.5, 0)
        self.assertEqual(expected, result)

    def test_filter_overThreshold(self):
        d1 = ['dog', 'cat']
        d2 = ['dog', 'cow', 'dog']
        d3 = ['cat', 'dog']
        d4 = ['dog', 'dog', 'chicken']
        df = filters.document_frequency(d1, defaultdict(int))
        df = filters.document_frequency(d2, df)
        df = filters.document_frequency(d3, df)
        df = filters.document_frequency(d4, df)
        newBag = ['dog', 'cat', 'cow']
        expectedDf = {'dog': 4, 'cat': 2, 'cow':1, 'chicken': 1}
        self.assertEqual(expectedDf, df)
        expected = ['dog', 'cat']
        result = filters.filter_overThreshold(newBag, df, 0.49, 4)
        self.assertEqual(expected, result)
        expected = ['dog']
        result = filters.filter_overThreshold(newBag, df, 0.5, 4)
        self.assertEqual(expected, result)

    def test_removeListFromList(self):
        source = [1,2,3,4,5,6,7,8]
        targets = [2,4,6,8]
        expected = [1,3,5,7]
        result = filters.removeListFromList(targets, source)
        self.assertEqual(expected, result)

    def test_removeFilterWords(self):
        source = [frozenset([1]), frozenset([2]), frozenset([3])]
        targets = [1,3]
        expected = [2]
        result = filters.removeFilterWords(targets, source)
        self.assertEqual(expected, result)

    def test_removeWords(self):
        source = [frozenset([1]), frozenset([2]), frozenset([3])]
        whitelist = [1,3,5,7]
        expected = [frozenset([1]), frozenset([3])]
        result = filters.removeWords(whitelist, source)
        self.assertEqual(expected, result)

    def test_flattenPairSet(self):
        pairSet = frozenset([frozenset([2]), frozenset([3])])
        expected = frozenset([2, 3])
        result = filters.flattenPairSet(pairSet)
        self.assertEqual(expected, result)

    def test_isSetItemInList_false(self):
        pairSet = frozenset([frozenset([2]), frozenset([4])])
        filterList = [1, 3, 5, 7]
        result = filters.isSetItemInList(filterList, pairSet)
        self.assertFalse(result)

    def test_isSetItemInList_trueFirst(self):
        pairSet = frozenset([frozenset([3]), frozenset([2])])
        filterList = [1, 3, 5, 7]
        result = filters.isSetItemInList(filterList, pairSet)
        self.assertTrue(result)

    def test_isSetItemInList_trueSecond(self):
        pairSet = frozenset([frozenset([2]), frozenset([3])])
        filterList = [1, 3, 5, 7]
        result = filters.isSetItemInList(filterList, pairSet)
        self.assertTrue(result)

    def test_removePairs(self):
        source = [frozenset([frozenset([1]), frozenset([2])]),
                  frozenset([frozenset([2]), frozenset([3])]),
                  frozenset([frozenset([3]), frozenset([1])]),
                  frozenset([frozenset([5]), frozenset([4])]),
                ]
        expected = [
            frozenset([frozenset([3]), frozenset([1])]),
            frozenset([frozenset([2]), frozenset([3])]),
            frozenset([frozenset([5]), frozenset([4])]),
        ]
        whitelist = [3,5,6]
        result = filters.removePairs(whitelist, source)
        self.assertEqual(set(expected), set(result))

    def test_filter_enumeration_nonEmptyFilter(self):
        pairs = [frozenset([frozenset([1]), frozenset([2])]),
                  frozenset([frozenset([2]), frozenset([3])]),
                  frozenset([frozenset([3]), frozenset([1])]),
                  frozenset([frozenset([5]), frozenset([4])]),
                ]
        words = [frozenset([1]), frozenset([2]), frozenset([3])]
        expected = [frozenset([1]),
                frozenset([frozenset([1]), frozenset([2])]),
                frozenset([frozenset([3]), frozenset([1])]),
                frozenset([frozenset([5]), frozenset([4])]),
            ]
        whitelist = [1,5]
        tfidfList = [(x, 0.6) for x in range(1,6)]
        result = filters.filter_enumeration(words+pairs, whitelist, tfidfList)
        self.assertEqual(expected, result)

    def test_filter_enumeration_emptyFilter(self):
        pairs = [frozenset([frozenset([1]), frozenset([2])]),
                  frozenset([frozenset([2]), frozenset([3])]),
                  frozenset([frozenset([3]), frozenset([1])]),
                  frozenset([frozenset([5]), frozenset([4])]),
                ]
        words = [frozenset([1]), frozenset([2]), frozenset([3])]
        enumeration = words + pairs
        expected = []
        wordsToFilter = []
        tfidfList = [(x, 0.6) for x in range(1,6)]
        result = filters.filter_enumeration(enumeration, wordsToFilter, tfidfList)
        self.assertEqual(expected, result)

