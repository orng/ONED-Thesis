#!/usr/bin/env python

#Reads a result file and prints the number of empty pairs/bags and both

import argparse

def isNoNewWords(line):
    return line.startswith('New Words: {}')

def isNoNewPairs(line):
    return line.startswith('New Pairs: {}')

def getStats(filename):
    previousLine = ""
    articles = 0
    noWords = 0
    noPairs = 0
    emptyEnumerations = 0

    with open(filename, 'r') as f:
        for line in f:
            if(isNoNewWords(line)):
                noWords += 1
            elif(isNoNewPairs(line)):
                noPairs += 1
                if(isNoNewWords(previousLine)):
                    emptyEnumerations += 1
            elif line.startswith('Url:'):
                articles += 1
            previousLine = line

    noWordsOnly = noWords - emptyEnumerations
    print "No Words: {noWords}/{total}, ({fraction:.2f})".format(
            noWords = noWordsOnly,
            total = articles,
            fraction = noWordsOnly/float(articles))
    print "No Pairs: {noPairs}/{total}, ({fraction:.2f})".format(
            noPairs = noPairs,
            total = articles,
            fraction = noPairs/float(articles))
    print "Empty enumerations: {empty}/{total} ({fraction:.2f})".format(
            empty = emptyEnumerations, 
            total = articles,
            fraction = emptyEnumerations/float(articles))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Print stats gathered from the results")
    parser.add_argument('resultfile')
    args = parser.parse_args()
    getStats(args.resultfile)

