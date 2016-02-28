#!/usr/bin/env python

import bag
import json
import sys

from pprint import pprint

def loadJson(filename, texts):
    with open(filename, 'r') as f:
        for line in f:
            texts.append(json.loads(line))
    return texts
    

def main():
    texts = list()
    for item in reversed(['nba/fox.json', 'nba/nba.json']):
        texts = loadJson(item, texts)

    words = []
    enumeratedBags = []
    bagDict = {}
    old = []
    i = 0
    for text in reversed(texts):
        i = i+1
        sys.stdout.write("Processing: {0}/{1}".format(i, len(texts)))
        sys.stdout.flush()
        sys.stdout.write("\r")

        words = text['text']
        enumeration, bagDict = bag.enumerateBag(words, enumeratedBags, bagDict)
        enumeratedBags.append(set(words))
        if enumeration == set([]):
            old.append(text['url'])

    sys.stdout.write("Processing: {0}/{1}\n".format(i, len(texts)))
    sys.stdout.write("Done!\n")

    pprint(old)


if __name__ == '__main__':
    main()
