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
        items = [1,2,3,4]
        expected = set([
                    frozenset([1,2,3]),
                    frozenset([2,3,4]),
                    frozenset([1,3,4]),
                    frozenset([1,2,4]),
                ])
        subsets = bag.getSubsets(items, 3)
        self.assertEqual(expected, subsets)

    #TODO: isNewAtM

    def test_isNewAtM(self):
        x = frozenset(['dog'])
        bags = [set(['dog', 'cat']),
                set(['dog', 'chicken'])]
        bagDict = {
                    frozenset(['dog']): 1,
                    frozenset(['cat']): 1,
                    frozenset(['chicken']): 2,
                }
        result = bag.isNewAtM(x, bags, bagDict, 2)
        self.assertEqual(False, result)
        result2 = bag.isNewAtM(x, bags, bagDict, 1)
        self.assertEqual(True, result2)


    def test_f_onlyMemeber(self):
        """Test the case where the only previously seen item is the given set"""
        subset = frozenset(['dog', 'cat'])
        bags = [subset]
        result = bag.f(subset, bags)
        self.assertEqual(1, result)

    def test_f_seenTwice(self):
        """Test f for when the given item has been seen twice"""
        subset = frozenset(['dog'])
        bags = [set(['dog', 'cat']),
                set(['dog', 'chicken'])]
        result = bag.f(subset, bags)
        self.assertEqual(1, result)


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
        oldBags = [set([frozenset(['dog']), frozenset(['cat'])]), set([frozenset(['chicken']), frozenset(['cow'])])]
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

    def test_enumerateBag_oldPairOfPreviouslyNew(self):
        """Tests the case where words have appeared together previously with 
        one of them being new at that time and the other old"""
        words = ['dog', 'chicken']
        oldBags = [
                set([
                    frozenset(['dog']),
                    frozenset(['cat'])
                ]),
                set([
                    frozenset(['dog']),
                    frozenset(['chicken'])
                ]),
            ]
        oldDict = {frozenset(['dog']): 1, 
                   frozenset(['cat']): 1,
                   frozenset(['chicken']): 2,
                  }
        expectedEnum = set([])
        expectedDict = dict(oldDict)
        newSet = frozenset([
                        frozenset(['dog']),
                        frozenset(['chicken']),
                    ])
        expectedDict[newSet] = 2
        enumeration, bagDict = bag.enumerateBag(words, oldBags, oldDict)
        self.assertEqual(expectedEnum, enumeration)
        self.assertEqual(expectedDict, bagDict)

    def test_enumerateBag_oldPairBothPreviouslyNewTogether(self):
        words = ['dog', 'chicken']
        oldBags = [
                set([
                    frozenset(['dog']),
                    frozenset(['chicken']),
                ]),
            ]
        oldDict = {frozenset(['dog']): 1,
                   frozenset(['chicken']): 1,
               }
        expectedEnum = set([])
        expectedDict = {frozenset(['dog']): 1,
                        frozenset(['chicken']): 1,
                        frozenset([
                                frozenset(['dog']),
                                frozenset(['chicken'])
                            ]): 1,
                        }
                                    

        enumeration, bagDict = bag.enumerateBag(words, oldBags, oldDict)
        self.assertEqual(expectedEnum, enumeration)
        self.assertEqual(expectedDict, bagDict)


        

    def test_enumrationToGraph(self):
        """Tests the pairs to graph function which creates a graph where 
        words are vertices and edges indicate that they form pairs"""
        list1 = [1,2,3]
        list2 = [4,5,6]
        pairs = set([frozenset([a,b]) for (a,b) in zip(list1, list2)])
        enumeration = set(pairs) # copy of pairs
        enumeration.add(frozenset([10]))
        expectedNodes = set(list1+list2)
        expectedEdges = pairs
        nodes, nrOfEdges = bag.enumerationToGraph(enumeration)
        self.assertEqual(expectedNodes, nodes)
        self.assertEqual(expectedEdges, nrOfEdges)

    def test_nodeDegrees(self):
        nodes = set([
                    frozenset([
                        frozenset(['dog']),
                        frozenset(['chicken']),
                    ]),
                    frozenset([
                        frozenset(['dog']),
                        frozenset(['cat']),
                    ]),
                    frozenset([
                        frozenset(['cat']),
                        frozenset(['cow']),
                    ])
                ])
        expected = [('dog', 2), ('cat', 2), ('cow', 1), ('chicken', 1)]
        result = bag.nodeDegrees(nodes)
        self.assertEqual(set(expected), set(result))
        self.assertTrue(result[0][1] == result[1][1] == 2)
        self.assertTrue(result[2][1] == result[3][1] == 1)
        

