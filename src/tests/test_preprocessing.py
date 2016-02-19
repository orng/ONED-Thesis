#!/usr/bin/env python

"""Tests for the preprocessing module"""

__author__ = "Orn Gudjonsson"

import unittest
import preprocessing as pre

class PreprocessingTests(unittest.TestCase):
        

    def test_remove_numbers(self):
        words = ['dog', 'cat', '999', '1234', '0001']
        expected = ['dog', 'cat']
        result = pre.remove_numbers(words)
        self.assertEqual(expected, result)

    def test_remove_punctuation(self):
        string = "Great... wtf? ffs!"
        expected = "Great wtf ffs"
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

