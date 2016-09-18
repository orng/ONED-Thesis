#!/user/bin/env python

import json

def checkJson(filename):
    articles = []
    with open(filename, 'r')  as f:
        for line in f:
            articles.append(json.loads(line))

    length = 0
    processed = {}
    res = []
    for article in articles:
        articleSet = frozenset(article['text'])
        articleName = article['url']
        if articleSet in processed.values():
            originalName = getKeyByValue(processed, articleSet)[0]
            print "{0} duplicate of {1}".format(articleName, originalName)
        else:
            length = length + len(articleSet)
            processed[articleName] = articleSet
            res.append(article)
    print "Average setlength: {0}".format(length/float(len(processed)))
    return res


def getKeyByValue(d, v):
    return filter(lambda k: d[k]==v, d.keys())
            
if __name__ == "__main__":
    res = []
    for filename in ['retures.jl', 'pbl.jl']:
        res = res + sorted(checkJson(filename), key=lambda d: d['date'])

    with open('processed.jl', 'w') as f:
        f.write(json.dumps(res))
        #f.write('\n'.join((str(i) for i in res)))
