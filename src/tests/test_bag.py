#!/usr/bin/env python

__author__ = "Orn Gudjonsson"

import unittest
import bag

class BagTests(unittest.TestCase):

    def test_getSubsets_sizeOne(self):
        items = [1,2,3,4]
        expected = set([frozenset([1]),frozenset([2]),frozenset([3]),frozenset([4])])
        subsets = bag.getSubsets(items, 1)
        self.assertEqual(expected, subsets)

    def test_getSubsets_sizeThree(self):
        items = [1,2,3, 4]
        expected = set([
                    frozenset([1,2,3]),
                    frozenset([2,3,4]),
                    frozenset([1,3,4]),
                    frozenset([1,3,4]),
                    frozenset([1,2,4]),
                ])
        subsets = bag.getSubsets(items, 3)
        self.assertEqual(expected, subsets)

    #TODO: test f and isNewAtM

    def test_enumerateBag_empty(self):
        """Test bag enumaration when there is no previous bag"""
        words = ['dog', 'cat']
        expectedEnum = set([frozenset(['dog']),
                    frozenset(['cat'])])
        expectedDict = {frozenset(['dog']): 1, 
                        frozenset(['cat']): 1}
        enumeration, bagDict = bag.enumerateBag(words, [], {})
        self.assertEqual(expectedEnum, enumeration)
        self.assertEqual(expectedDict, bagDict)

    def test_enumerateBag_nonempty(self):
        """tests bag enumeration when there are previous bags"""
        words = ['dog', 'chicken']
        oldBags = [set([frozenset(['dog']),
                    frozenset(['cat'])])]
        oldDict = {frozenset(['dog']): 1, 
                        frozenset(['cat']): 1}
        expectedEnum = set([frozenset(['chicken'])])
        expectedDict = {frozenset(['dog']): 1, 
                        frozenset(['cat']): 1,
                        frozenset(['chicken']): 2}
        enumeration, bagDict = bag.enumerateBag(words, oldBags, oldDict)
        self.assertEqual(expectedEnum, enumeration)
        self.assertEqual(expectedDict, bagDict)

    def test_enumerateBag_duplicate(self):
        """tests enumaration of an already seen item"""
        words = ["dog"]
        oldBags = [set([frozenset(['dog'])])]
        oldDict = {frozenset(['dog']): 1}
        expectedEnum = set([])
        expectedDict = {frozenset(['dog']): 1}
        enumeration, bagDict = bag.enumerateBag(words, oldBags, oldDict)
        self.assertEqual(expectedEnum, enumeration)
        self.assertEqual(expectedDict, bagDict)

    def test_enumerateBag_newPair(self):
        words = ['dog', 'chicken']
        oldBags = [set(['dog', 'cat']), set(['chicken', 'cow'])]
        oldDict = {frozenset(['dog']): 1, 
                   frozenset(['cat']): 1,
                   frozenset(['cow']): 2,
                   frozenset(['chicken']): 2,
                  }
        expectedEnum = set([frozenset([frozenset(['dog']),
                                       frozenset(['chicken'])
                                     ])
                        ])
        expectedDict = {frozenset(['dog']): 1, 
                        frozenset(['cat']): 1,
                        frozenset(['cow']): 2,
                        frozenset(['chicken']): 2,
                        frozenset([frozenset(['dog']), frozenset(['chicken'])]): 3
                       }
        enumeration, bagDict = bag.enumerateBag(words, oldBags, oldDict)
        self.assertEqual(expectedEnum, enumeration)
        self.assertEqual(expectedDict, bagDict)
