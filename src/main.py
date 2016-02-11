#!/usr/bin/env python

import bag
import json

def main():
    with open('nba/espn.json', 'r') as f:
        texts = json.loads(f.read())
        thebag = set({})
        for text in texts:
            unique = bag.bagify(text['text'], thebag)
            if len(unique) > 0:
                print "New article: " + text['url']
                thebag = thebag | unique

if __name__ == '__main__':
    main()
