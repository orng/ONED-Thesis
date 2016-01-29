#!/usr/bin/env python

"""Tests for the preprocessing module"""

__author__ = "Orn Gudjonsson"

import unittest
import preprocessing as pre

class PreprocessingTests(unittest.TestCase):
        
    def test_stem_words(self):
        string = "The horizontal dogs are chewing the puppies"
        result = pre.stem_words(string)
        self.assertNotEqual(string.lower(), " ".join(result))

    def test_stopwords(self):
        words = ["the", "are", "what", "is", "philosopher", "not"]
        expected = ["philosopher"]
        result = pre.remove_stopwords(words)
        self.assertEqual(expected, result)

