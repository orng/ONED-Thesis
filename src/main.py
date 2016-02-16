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
    for item in ['nba/espn.json', 'nba/fox.json', 'nba/nba.json']:
        texts = loadJson(item, texts)

    i = 0
    l = len(texts)
    thebag = []
    progress = 0
    old = list()
    for text in reversed(texts):
        i = i+1
        currentProgress = i/float(l) * 100
        if currentProgress - progress > 1.0:
            progress = currentProgress
            sys.stdout.write("{0:03d}%".format(int(progress)))
            sys.stdout.flush()
            sys.stdout.write("\r")

        unique, theBag = bag.bagify(text['text'], thebag)
        if len(unique) == 0:
            old.append(text['url'])
            #print "Old article: " + text['url']
    sys.stdout.write("\n")

    pprint(old)


if __name__ == '__main__':
    main()
