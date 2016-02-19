#!/usr/bin/env python

__author__ = "Orn Gudjonsson"

import unittest
import bag

class BagTests(unittest.TestCase):
    def test_bagify_empty(self):
        """Test enumaration when there is no previous bag"""
        words = ['dog', 'cat', 'cow']
        expected = set([frozenset(['dog', 'cat']),
                    frozenset(['dog', 'cow']),
                    frozenset(['cat', 'cow'])])
        minSet, bags = bag.bagify(words, [])
        print bags
        self.assertEqual(expected, minSet)
        self.assertEqual(minSet, bags[0])

    def test_bagify_nonempty(self):
        """tests enumeration when there are previous bags"""
        words = ['dog', 'cat', 'cow']
        oldbags = [set([frozenset(['dog', 'cow'])]),
                   set([frozenset(['dog', 'chicken'])])]

        expectedMin = set([frozenset(['dog', 'cat']),
                    frozenset(['cat', 'cow'])])
        expectedBags = oldbags + [expectedMin]

        minSet, bags = bag.bagify(words, oldbags)

        self.assertEqual(expectedMin, minSet)
        self.assertEqual(expectedBags, bags)

    def test_bagify_duplicate(self):
        """tests enumaration of an already seen item"""
        words = ["dog"]
        oldbags = [{frozenset(['dog'])}]

        minSet, bags = bag.bagify(words, oldbags)

        self.assertEqual(set([]), minSet)
        self.assertEqual(oldbags, bags)


    def test_minimalNew_first(self):
        """Test enumeration of first article"""
        words = ['dog', 'cat', 'cow']
        minNews = bag.minimalNew(words, [[],[]])
        self.assertEqual(set(words), minNews[0])
        self.assertEqual(set(bag.getPairs(words)), minNews[1])
        self.assertEqual([set(words), set(bag.getPairs(words))], minNews)

    def test_minmalNew_newWord(self):
        """Tests enumeration when some words have been seen already"""
        words = ['dog', 'cow']
        oldbags = [['dog', 'cat'], [frozenset(['dog', 'cat'])]]
        minNews = bag.minimalNew(words, oldbags)
        expected = set(['cow'])
        self.assertEqual([expected, set([])], minNews)

    def test_minimalNew_newPair(self):
        """tests enumaration when there is no new word, but a new pair"""
        oldwords = [['dog', 'cat'], ['dog', 'cow']]
        oldPairs = [set([frozenset(['dog', 'cat'])]), set([frozenset(['dog', 'cow'])])]
        oldBags = [oldwords, oldPairs]
        words = ['dog', 'cat', 'cow']
        minNews = bag.minimalNew(words, oldBags)
        expectedPairs = set([frozenset(['cat', 'cow'])])
        self.assertEqual([set([]), expectedPairs], minNews)
        
    def test_getPairs(self):
        """Tests the getPairs function"""
        words = ['dog', 'cat', 'cow']
        expected = [frozenset(['dog', 'cat']),
                    frozenset(['dog', 'cow']),
                    frozenset(['cat', 'cow'])]
        result = bag.getPairs(words)
        self.assertEqual(set(expected), set(result))

