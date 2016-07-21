#!/usr/bin/env python

import argparse

from wordcloud import WordCloud
import  matplotlib.pyplot as plt

from main import loadJson


def plotWordCloud(filenames):
    texts = list()
    for filename in filenames:
        texts = loadJson(filename, texts)
    textString = ""
    for text in texts:
        textString += " " + text['text']
    wordcloud = WordCloud().generate(textString)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process the provided data")
    parser.add_argument('articles', nargs='+')
    args = parser.parse_args()
    plotWordCloud(args.articles)
