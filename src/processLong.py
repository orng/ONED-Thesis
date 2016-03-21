#!/usr/bin/env python

import json
import re

def main():
    sentences = []
    #article = 'history'
    #article = 'longArticle'
    #article = 'ww2'
    article = 'timeline'
    with open(article+'.txt', 'r') as f:
        paragraphs = filter(lambda x: x != "\n", f.readlines())
    #sentences = paragraphs
    text = ''.join(paragraphs)
    sentences = re.split(r' *[\.\?!\n][\'"\)\]]*\s+', text)

    item = {}
    i = 0
    with open(article+'.jl', 'a') as f:
        for sentence in sentences:
            if sentence == u"" or re.match(r'\s+', sentence):
                #skip whitespace only sentences
                continue

            item['date'] = i
            item['url'] = i
            item['text'] = sentence
            i += 1
            f.write(json.dumps(item) + '\n')


if __name__=="__main__":
    main()
