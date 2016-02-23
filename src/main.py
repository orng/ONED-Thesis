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
    for item in ['nba/fox.json', 'nba/nba.json']:
        texts = loadJson(item, texts)

    i = 0
    l = len(texts)
    thebag = []
    old = list()
    oldBags = [[],[]]
    words = []
    for text in reversed(texts):
        i = i+1
        #sys.stdout.write("{0:03d}%".format(int(progress)))
        sys.stdout.write("Processing: {0}/{1}".format(i, len(texts)))
        sys.stdout.flush()
        sys.stdout.write("\r")

        words = text['text']
        minimalNew = bag.minimalNew(words, oldBags)
        if minimalNew != [set([]), set([]), set([])]:
            oldBags[0].append(minimalNew[0])
            #oldBags[1].append(minimalNew[1])
            oldBags[1].append(minimalNew[1] | minimalNew[2])
            #oldBags[1].append(bag.getPairs(words))
        else:
            old.append(text['url'])

    sys.stdout.write("Processing: {0}/{1}\n".format(i, len(texts)))
    sys.stdout.write("Done!\n")

    pprint(old)


if __name__ == '__main__':
    main()
