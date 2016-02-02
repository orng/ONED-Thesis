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
        result = bag.bagify(string, {})
        self.assertEqual(expected, result)

    def test_bagify_nonempty(self):
        """tests enumeration when there are previous bags"""
        string = "dog cat cow"
        oldbags = set([frozenset(['dog', 'cow']),
                    frozenset(['dog', 'chicken']),])
        expected = set([frozenset(['dog', 'cat']),
                    frozenset(['cat', 'cow'])])
        result = bag.bagify(string, oldbags)
        self.assertEqual(expected, result)


