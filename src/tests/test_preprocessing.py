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
                'cow': 1
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
        df = pre.document_frequency(d2, df)
        expected = ['cat', 'cat', 'cat']
        result = pre.filter_tfidf(d2, df, 0.9, 2)
        self.assertEqual(expected, result)


    def test_filter_common(self):
        dogs = ['dog' for i in range(10)]
        cats = ['cat' for i in range(5)]
        rest = ['cow', 'chicken', 'pig']
        animals = dogs + cats + rest
        expected = cats + rest
        wordFreq = pre.term_frequency(animals)
        result = pre.filter_common(animals, wordFreq, 0.10)
        self.assertEqual(expected, result)
