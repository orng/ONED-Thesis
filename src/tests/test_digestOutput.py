#!/usr/bin/env python

import unittest
from enumerator import digestOutput as digest

class DigestOutputTests(unittest.TestCase):

    def test_containsKeywords(self):
        keywords = ['dog', 'cat']
        e1 = [['cat'], [['cow'], ['chicken']],]
        e2 = [['cow'], ['dog']]
        e3 = [['cow'], [['chicken'], ['dog']]]
        for e in [e1, e2, e3]:
            self.assertTrue(digest.containsKeyWords(keywords, e))

        e4 = [['chicken'], ['cow']]
        e5 = [[['cow'], ['rat']], [['rat'], ['chicken']]]
        for e in [e4, e5]:
            self.assertFalse(digest.containsKeyWords(keywords, e))

    def test_listToFrozenset(self):
        lists = ['a', ['b', 'c'], [['d'], ['c']]]
        expected = frozenset([
            'a', 
            frozenset(['b', 'c']),
            frozenset([
                frozenset(['d']),
                frozenset(['c'])
            ]),
        ])
        self.assertEquals(expected, digest.listToFrozenset(lists))

