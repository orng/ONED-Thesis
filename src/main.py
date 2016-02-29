#!/usr/bin/env python

import json
import sys
from pprint import pprint

import bag

def loadJson(filename, texts):
    with open(filename, 'r') as f:
        for line in f:
            texts.append(json.loads(line))
    return texts
    

def main():
    texts = list()
    #for item in ['nba/fox.jl', 'nba/nba.jl']:
        #texts = loadJson(item, texts)
    #texts = sorted(texts, key=lambda d: d['date'])
    with open('nba/processed.jl', 'r') as f:
        texts = json.loads(f.read())

    words = []
    enumeratedBags = []
    bagDict = {}
    old = []
    enum = []
    i = 0
    for text in texts:
        i = i+1
        sys.stdout.write("Processing: {0}/{1}".format(i, len(texts)))
        sys.stdout.flush()
        sys.stdout.write("\r")

        words = text['text']
        enumeration, bagDict = bag.enumerateBag(words, enumeratedBags, bagDict)
        enumeratedBags.append(set(words))
        enum.append(enumeration)
        if enumeration == set([]):
            old.append(text['url'])

    sys.stdout.write("Processing: {0}/{1}\n".format(i, len(texts)))
    sys.stdout.write("Done!\n")

    pprint(old)

    with open('dict.result', 'w') as f:
        pprint(bagDict, f)
    with open('enumeration.result', 'w') as f:
        pprint(enum, f)


if __name__ == '__main__':
    main()
