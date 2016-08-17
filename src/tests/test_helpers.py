#!/usr/bin/env python

__author__ = "Orn Gudjonsson"

import unittest
from enumerator import helpers

class HelpersTests(unittest.TestCase):

    def test_extractString(self):
        expected = 'string'
        st = frozenset([frozenset([frozenset([expected])])])
        result = helpers.extractString(st)
        self.assertEquals(expected, result)

    def test_find(self):
        words = ['dog', 'cat', 'cow', 'dog', 'cat', 'dog']
        expected = [0, 3, 5]
        result = helpers.find(words, 'dog')
        self.assertEquals(expected, result)
        
    def test_calculateWordDistance(self):
        words = ['cow', 'cat', 'cat', 'dog', 'chicken', 'cow']
        expected = 2
        r1 = helpers.calculateWordDistance('cow', 'dog', words)
        r2 = helpers.calculateWordDistance('dog', 'cow', words)
        self.assertEquals(expected, r1)
        self.assertEquals(expected, r2)

    def test_distanceDictToString(self):
        distDict = {
                frozenset([frozenset(['cow']), frozenset(['cat'])]): 3,
                frozenset([frozenset(['dog']), frozenset(['cat'])]): 10,
                frozenset([frozenset(['chicken']), frozenset(['cow'])]): 1,
                frozenset([frozenset(['cow']), frozenset(['dog'])]): 8,
            }
        expected = "(cow, chicken): 1, (cow, cat): 3, (cow, dog): 8, (cat, dog): 10"
        result = helpers.distanceDictToString(distDict)
        self.assertEquals(expected, result)
        
    def test_distanceDictFromPairs(self):
        words = ['cow', 'cat', 'cat', 'dog', 'chicken', 'cow']
        p1 = frozenset([frozenset(['cow']), frozenset(['cat'])])
        p2 = frozenset([frozenset(['dog']), frozenset(['cow'])])
        pairs = [p1, p2]
        expected = {p1: 1, p2: 2}
        result = helpers.distanceDictFromPairs(pairs, words)
        self.assertEquals(expected, result)

