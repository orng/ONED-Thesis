#!/usr/bin/env python

__author__ = "Orn Gudjonsson"

import unittest
import bag

class BagTests(unittest.TestCase):
    def test_bagify_empty(self):
        """Test enumaration when there is no previous bag"""
        string = "dog cat cow"
        expected = set([frozenset(['dog', 'cat']),
                    frozenset(['dog', 'cow']),
                    frozenset(['cat', 'cow'])])
        minSet, bags = bag.bagify(string, [])
        print bags
        self.assertEqual(expected, minSet)
        self.assertEqual(minSet, bags[0])

    def test_bagify_nonempty(self):
        """tests enumeration when there are previous bags"""
        string = "dog cat cow"
        oldbags = [set([frozenset(['dog', 'cow'])]),
                   set([frozenset(['dog', 'chicken'])])]

        expectedMin = set([frozenset(['dog', 'cat']),
                    frozenset(['cat', 'cow'])])
        expectedBags = oldbags + [expectedMin]

        minSet, bags = bag.bagify(string, oldbags)

        self.assertEqual(expectedMin, minSet)
        self.assertEqual(expectedBags, bags)

    def test_bagify_duplicate(self):
        """tests enumaration of an already seen item"""
        string = "dog"
        oldbags = [{frozenset(['dog'])}]

        minSet, bags = bag.bagify(string, oldbags)

        self.assertEqual(set([]), minSet)
        self.assertEqual(oldbags, bags)



