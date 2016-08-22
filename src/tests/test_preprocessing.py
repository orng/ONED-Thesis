#!/usr/bin/env python

"""Tests for the preprocessing module"""

__author__ = "Orn Gudjonsson"

from collections import defaultdict
import unittest

from enumerator import preprocessing as pre

class PreprocessingTests(unittest.TestCase):
        
    def test_remove_numbers(self):
        words = ['dog', 'cat', '999', '1234', '0001']
        expected = ['dog', 'cat']
        result = pre.remove_numbers(words)
        self.assertEqual(expected, result)

    def test_remove_punctuation(self):
        string = u"Great... wtf? ffs! Don't hurt me \"Donald\""
        expected = ['Great', 'wtf', 'ffs', 'Don', 't', 'hurt', 'me', 'Donald']
        result = pre.remove_punctuation(string)
        self.assertEqual(expected, result.split())

    def test_stem_words(self):
        words = ['The', 'Horizontal', 'dogs', 'are', 'chewing', 'the', 'puppies']
        expected = ['The', 'Horizont', 'dog', 'are', 'chew', 'the', 'puppi']
        result = pre.stem_words(words)
        self.assertNotEqual(words, result)
        self.assertEqual(expected, result)

    def test_stopwords(self):
        words = ["the", "are", "what", "is", "philosopher", "not"]
        expected = ["philosopher"]
        result = pre.remove_stopwords(words)
        self.assertEqual(expected, result)

    def test_get_sentences(self):
        s1 = u"This is first."
        s2 = u"This is second."
        s3 = u"Third has A.B.B.A."
        text = " ".join([s1, s2, s3])
        expected = [s1, s2, s3]
        result = pre.get_sentences(text)
        self.assertEqual(expected, result)

    def test_to_wordlist(self):
        text = u"The word and the other thing."
        expected = ['word', 'thing']
        result = pre.to_wordlist(text)
        self.assertEqual(expected, result)

    def test_to_wordlist_multi(self):
        text = u"The cat and the dog. Dog cow."
        expected = [('cat', 'dog'), ('dog', 'cow')]
        result = pre.to_wordlist_multi(text)
        self.assertEqual(expected, result)
