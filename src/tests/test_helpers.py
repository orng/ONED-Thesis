#!/usr/bin/env python

__author__ = "Orn Gudjonsson"

import unittest
import helpers

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
