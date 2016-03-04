#!/usr/bin/env python

import json
import re

def main():
    with open('longArticle.txt', 'r') as f:
        text = ''.join(f.readlines())
    sentences = re.split(r' *[\.\?!][\'"\)\]]*\s+', text)
    item = {}
    i = 0
    with open('processedLong.jl', 'a') as f:
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
