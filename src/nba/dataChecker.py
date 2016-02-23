#!/user/bin/env python

import json

def checkJson(filename):
    articles = []
    with open(filename, 'r')  as f:
        for line in f:
            articles.append(json.loads(line))

    length = 0
    processed = {}
    for article in articles:
        articleSet = frozenset(article['text'])
        articleName = article['url']
        if articleSet in processed.values():
            originalName = getKeyByValue(processed, articleSet)[0]
            print "{0} duplicate of {1}".format(articleName, originalName)
            print articleName == originalName
        else:
            length = length + len(articleSet)
            processed[articleName] = articleSet
    print "Average setlength: {0}".format(length/float(len(processed)))

def getKeyByValue(d, v):
    return filter(lambda k: d[k]==v, d.keys())
            
if __name__ == "__main__":
    for filename in ['nba.json', 'fox.json']:
        checkJson(filename)
