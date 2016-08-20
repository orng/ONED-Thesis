#!/usr/bin/env python

import argparse
import json

import helpers
import preprocessing as pre
import  filters

def diffEnumerations(dataset1, dataset2):
    assert len(dataset1) == len(dataset2)

    datasets = zip(dateset1, dataset2)
    diffs = []
    diffObj = {}
    for data in datasets:
        d1 = data[0]
        d2 = data[1]
        e1 = d1['enumeration']
        e2 = d2['enumeration']
        diffObj['text'] = d1['text']
        diffObj['url'] = d1['url']
        diffObj['common'] = e1 & e2
        diffObj['inFirst'] = e1 - e2
        diffObj['inSecond'] = e2 - e1
        diffs.appen(diff)
    return diffs

def containsKeyWords(keywords, enumeration):
    """
    Returns True if any of the given keywords is within the
    given enumeration. False otherwise.
    Input:
        keywords: ['some', 'key', 'words']
        enumeration: ['word', ['word', 'pairs']]
    Output:
        True/False
    """
    #flatten the enumeration, we only care about words
    words = []
    for i in enumeration:
        if len(i) > 1:
            for j in i:
                words += j
        else:
            words +=  i

    wordSet = set(words)

    for k in keywords:
        if (u""+k) in wordSet:
            return True
    return False


def listToFrozenset(lst):
    """
    Input:
        lst: [['word'], [['some'], ['pair']]]
    Ouput:
        set([frozenset(['word']), 'frozenset([frozenset['some'], 'frozenset(['pair'])])])
    """
    #TODO: this is retarded: how many of these do we have already?
    #do something more sensible, perhaps try to update the bag code
    #to not produce this kind of stuff
    if type(lst) != type([]):
        return lst
    else:
        return frozenset([listToFrozenset(x) for x in lst])


def digest(inputFile, outputFile, keywords):
    """
    Digest the given json file
    """
    enumerations = helpers.loadJson(inputFile, [])
    keywords = pre.stem_words(keywords)
    outputBuffer = open(outputFile, 'w')
    for e in enumerations:
        enumeration = e['enumeration']
        #if containsKeyWords(keywords, enumeration):
        if True:
            words = e['text']
            url = e['url']
            frozenEnum = listToFrozenset(enumeration)

            words = [x for x in frozenEnum if len(x) == 1]
            pairs = [x for x in frozenEnum if len(x) > 1]
            #newWords = filters.removeWords(keywords, words)
            #newPairs = filters.removePairs(keywords, pairs)
            #newWords = [y for x in frozenEnum for y in x if len(x)==1 and y in keywords]
            #newPairs = [x for x in frozenEnum if len(x) >1 and isSetItemInList(x, keywords)]
            postFilterEnum = newWords + newPairs
            tfidfList = [(x, 1) for x in keywords]

            #filter stuff not containing keywords
            helpers.printEnumerationToFileObject(url, words, postFilterEnum, outputBuffer, tfidfList)
    outputBuffer.close()

DIFF_FORMAT = "{Url: {url}\nCommon: {common}\nIn First: {inFirst}\nInSecond: {inSecond}\n\n\n"
def diffToString(diff):
    url = diff['url']
    common = diff['common']
    inFirst = diff['inFirst']
    inSecond = diff['inSecond']
    return DIFF_FORMAT.format(
        url = url,
        common=common,
        inFirst = inFirst, 
        inSecond = inSecond
    )

def diff(inFile1, inFile2, outputFile):
    enumerations1 = helpers.loadJson(inFile1)
    enumerations2 = helpers.loadJson(inFile2)
    diffs = diffEnumerations(enumerations1, enumerations2)
    with open(outputFile, w) as f:
        for d in diffs:
            diffString = diffToString(d)
            f.write(diffString)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Processes the given outputfile")
    parser.add_argument('-o', '--output', default='queryRes.txt')
    parser.add_argument('-d', '--diff', nargs='*')
    parser.add_argument('-i', '--input', default='result.txt')
    parser.add_argument('-k', '--keywords', nargs='*')
    args = parser.parse_args()
    if(len(args.diff) > 0):
        diff(args.diff[0], args.diff[1], args.output)
    else:
        digest(args.input, args.output, args.keywords)

