#!/usr/bin/env python

import bag
import json
import sys

from pprint import pprint

def loadJson(filename, texts):
    with open(filename, 'r') as f:
        return(texts + json.loads(f.read()))
    

def main():
    texts = list()
    for item in ['nba/fox.json', 'nba/nba.json']:
        texts = loadJson(item, texts)

    i = 0
    l = len(texts)
    thebag = []
    progress = 0
    old = list()
    oldBags = [[],[]]
    words = []
    for text in reversed(texts):
        i = i+1
        currentProgress = i/float(l) * 100
        if currentProgress - progress > 1.0:
            progress = currentProgress
            #sys.stdout.write("{0:03d}%".format(int(progress)))
            sys.stdout.write("Processing: {0}/{1}".format(i, len(texts)))
            sys.stdout.flush()
            sys.stdout.write("\r")

        words = text['text']
        minimalNew = bag.minimalNew(words, oldBags)
        if minimalNew != [set([]), set([])]:
            oldBags[0].append(minimalNew[0])
            oldBags[1].append(minimalNew[1])
        else:
            old.append(text['url'])

    sys.stdout.write("Processing: {0}/{1}\n".format(i, len(texts)))
    sys.stdout.write("Done!\n")

    pprint(old)


if __name__ == '__main__':
    main()
