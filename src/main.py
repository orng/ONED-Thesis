#!/usr/bin/env python

import bag
import json

def main():
    with open('nba/espn.json', 'r') as f:
        texts = json.loads(f.read())
    with open('nba/fox.json', 'r') as f:
        texts = texts + json.loads(f.read())

    thebag = set({})
    for text in texts:
        unique = bag.bagify(text['text'], thebag)
        if len(unique) == 0:
            print "Old article: " + text['url']
        else:
            thebag = thebag | unique

if __name__ == '__main__':
    main()
