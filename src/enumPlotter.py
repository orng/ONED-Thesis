#!/usr/bin/env python

#Plots the amount of new pairs and the amount of new words over time

import os
import matplotlib.pyplot as plt
import numpy

WORDS = 'New Words: {'
PAIRS = 'New Pairs: {'
WORDLEN = len(WORDS)
PAIRLEN = len(PAIRS)


def gatherData(filename):
    words = []
    pairs = []
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith(WORDS):
                wordString = line[WORDLEN:-2]
                words.append(len(wordString.split()))
            elif line.startswith(PAIRS):
                pairString = line[PAIRLEN :-2]
                pairs.append(len(pairString.split()))
    return words, pairs

def plotDataPoints(words, pairs):
    xaxis = range(1, len(words)+1)
    plt.plot(xaxis, words, 'rs', xaxis, pairs, 'g^', markersize=8)
    #plt.axis([0, xaxis[-1]+1, -1, max(words + pairs)+1])
    plt.margins(0.1)
    addTrendline(xaxis, words, 'r')
    addTrendline(xaxis, pairs, 'g')



def grouper(iterable, n):
    args = [iter(iterable)] * n
    return zip(*args)


def clusterPoints(words, pairs):
    groupedWords = [numpy.mean(x) for x in grouper(words, len(words)/40)]
    groupedPairs = [numpy.mean(x) for x in grouper(pairs, len(words)/40)]
    return groupedWords, groupedPairs

def addTrendline(xaxis, yaxis, color):
    z = numpy.polyfit(xaxis, yaxis, 1)
    p = numpy.poly1d(z)
    plt.plot(xaxis, p(xaxis), color+'-')


if __name__ == "__main__":
    basePath = os.path.join('..', 'results')
    outputFormat = "{dataset}-plot.png"
    outputPathFormat = os.path.join(basePath, outputFormat)

    dataSources = [os.path.join(basePath,'d'+str(x)) for x in range(1,5)]
    dataFiles = ['c1-none-None-postFilter-normal-.txt',
            'c3-tfidf-15-postFilter-normal-.txt',
            'c5-tfidf-15-preFilter-normal-.txt',
            'c6-none-15-postFilter-subBags-.txt']

    #dataFiles = [os.listdir(os.path.join(basePath, x)) for x in dataSources]
    datasourceCounter = 0
    dataTitles= ['D1', 'D2', 'D3', 'D4']
    configTitles = [
        'Configuration-1', 
        'Configuration-2 (TF-IFD: 15)',
        'Configuration-3 (TF-IDF: 15)',
        'Configuration-4 (TF-IDF: 15)'
    ] #TODO: add unfiltered sub-bags and neighbours

    for dataSource in dataSources:
        subplotCounter = 1
        for f in dataFiles:
            plt.subplot(2, 2, subplotCounter)
            plt.title(configTitles[subplotCounter -1])
            plt.ylabel('Avg. set count/2.5% articles')
            plt.xlabel('Article batch')
            plt.tight_layout()
            filePath = os.path.join(dataSource, f)
            words, pairs = gatherData(filePath)
            words, pairs = clusterPoints(words, pairs)
            plotDataPoints(words, pairs)
            subplotCounter += 1

        plt.suptitle('Dataset {data}'.format(data=dataTitles[datasourceCounter]))

        outputFile = outputPathFormat.format(dataset=dataTitles[datasourceCounter])
        plt.savefig(outputFile, bbox_inches='tight')
        datasourceCounter += 1
        plt.clf()
