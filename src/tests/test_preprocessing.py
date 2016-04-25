#!/usr/bin/env python

"""Tests for the preprocessing module"""

__author__ = "Orn Gudjonsson"

import unittest
import preprocessing as pre
from collections import defaultdict

class PreprocessingTests(unittest.TestCase):
        

    def test_remove_numbers(self):
        words = ['dog', 'cat', '999', '1234', '0001']
        expected = ['dog', 'cat']
        result = pre.remove_numbers(words)
        self.assertEqual(expected, result)

    def test_remove_punctuation(self):
        string = "Great... wtf? ffs!"
        expected = "Great  wtf  ffs "
        result = pre.remove_punctuation(string)
        self.assertEqual(expected, result)

    def test_stem_words(self):
        string = "The horizontal dogs are chewing the puppies"
        expected = ['the', 'horizont', 'dog', 'are', 'chew', 'the', 'puppi']
        result = pre.stem_words(string)
        self.assertNotEqual(string.lower(), " ".join(result))
        self.assertEqual(expected, result)

    def test_stopwords(self):
        words = ["the", "are", "what", "is", "philosopher", "not"]
        expected = ["philosopher"]
        result = pre.remove_stopwords(words)
        self.assertEqual(expected, result)

    def test_term_frequency(self):
        words = ['dog', 'cat', 'cow', 'dog', 'cat', 'dog']
        expected = {
                'dog': 3,
                'cat': 2,
                'cow': 1,
                }
        result = pre.term_frequency(words)
        self.assertEqual(expected, result)

    def test_document_frequency(self):
        d1 = ['dog', 'cow', 'dog']
        d2 = ['cat', 'dog', 'cat']
        expected = {
                'dog': 2,
                'cat': 1,
                'cow': 1,
                }
        r1 = pre.document_frequency(d1, defaultdict(int))
        r2 = pre.document_frequency(d2, r1)
        self.assertEqual(expected, r2)

    def test_collection_frequency(self):
        d1 = ['dog', 'cow', 'dog']
        d2 = ['cat', 'dog', 'cat']
        expected = {
                'dog': 3,
                'cat': 2,
                'cow': 1,
                }
        r1 = pre.collection_frequency(d1, defaultdict(int))
        r2 = pre.collection_frequency(d2, r1)
        self.assertEqual(expected, r2)

    def test_filter_tfidf(self):
        d1 = ['dog']
        d2 = ['dog', 'cat', 'cat', 'cat']
        df = pre.document_frequency(d1, defaultdict(int))
        #df = pre.document_frequency(d2, df)
        #expected = ['cat', 'cat', 'cat']
        expected = ['dog']
        result = pre.filter_tfidf(d2, df, 0.9, 2)
        self.assertEqual(expected, result)


    def test_filter_common(self):
        dogs = ['dog' for i in range(10)]
        cats = ['cat' for i in range(5)]
        rest = ['cow', 'chicken', 'pig']
        animals = dogs + cats + rest
        expected = ['dog']
        wordFreq = pre.collection_frequency(animals, defaultdict(int))
        result = pre.filter_common(animals, wordFreq, 0.25)
        self.assertEqual(expected, result)

    def test_filter_overThreshold_firstItem(self):
        df = defaultdict(int)
        words = ['dog', 'cat']
        expected = []
        result = pre.filter_overThreshold(words, df, 0.5, 0)
        self.assertEqual(expected, result)

    def test_filter_overThreshold(self):
        d1 = ['dog', 'cat']
        d2 = ['dog', 'cow', 'dog']
        d3 = ['cat', 'dog']
        d4 = ['dog', 'dog', 'chicken']
        df = pre.document_frequency(d1, defaultdict(int))
        df = pre.document_frequency(d2, df)
        df = pre.document_frequency(d3, df)
        df = pre.document_frequency(d4, df)
        newBag = ['dog', 'cat', 'cow']
        expectedDf = {'dog': 4, 'cat': 2, 'cow':1, 'chicken': 1}
        self.assertEqual(expectedDf, df)
        expected = ['dog', 'cat']
        result = pre.filter_overThreshold(newBag, df, 0.49, 4)
        self.assertEqual(expected, result)
        expected = ['dog']
        result = pre.filter_overThreshold(newBag, df, 0.5, 4)
        self.assertEqual(expected, result)
        

    def test_get_sentences(self):
        s1 = "This is first"
        s2 = "This is second"
        s3 = "Third has A.B.B.A"
        text = ". ".join([s1, s2, s3])
        expected = [s1, s2, s3]
        result = pre.get_sentences(text)
        self.assertEqual(expected, result)
    
    def test_to_wordlist_multi(self):
        text = "Cat dog. Dog cow."
        expected = [('cat', 'dog'), ('dog', 'cow')]
        result = pre.to_wordlist_multi(text)
        self.assertEqual(expected, result)

    def test_removeListFromList(self):
        source = [1,2,3,4,5,6,7,8]
        targets = [2,4,6,8]
        expected = [1,3,5,7]
        result = pre.removeListFromList(targets, source)
        self.assertEqual(expected, result)

    def test_flattenPairSet(self):
        pairSet = frozenset([frozenset([2]), frozenset([3])])
        expected = frozenset([2, 3])
        result = pre.flattenPairSet(pairSet)
        self.assertEqual(expected, result)

    def test_isSetItemInList_false(self):
        pairSet = frozenset([frozenset([2]), frozenset([4])])
        filterList = [1, 3, 5, 7]
        result = pre.isSetItemInList(filterList, pairSet)
        self.assertFalse(result)

    def test_isSetItemInList_trueFirst(self):
        pairSet = frozenset([frozenset([3]), frozenset([2])])
        filterList = [1, 3, 5, 7]
        result = pre.isSetItemInList(filterList, pairSet)
        self.assertTrue(result)

    def test_isSetItemInList_trueSecond(self):
        pairSet = frozenset([frozenset([2]), frozenset([3])])
        filterList = [1, 3, 5, 7]
        result = pre.isSetItemInList(filterList, pairSet)
        self.assertTrue(result)

    def test_removePairs(self):
        source = [frozenset([frozenset([1]), frozenset([2])]),
                  frozenset([frozenset([2]), frozenset([3])]),
                  frozenset([frozenset([3]), frozenset([1])]),
                  frozenset([frozenset([5]), frozenset([4])]),
                ]
        expected = [
            frozenset([frozenset([3]), frozenset([1])]),
        ]
        targets = [2, 4]
        result = pre.removePairs(targets, source)
        self.assertEqual(expected, result)



