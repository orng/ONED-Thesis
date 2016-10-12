#!usr/bin/env python

import os
from enumerator import main

class Config:
    def __init__(self):
        self.filters = []
        self.thresholds = []
        self.name = ""
        self.useSubBags = False
        self.useNeighbours = False
        self.preFilter =False


class Config1(Config):
    def __init__(self):
        Config.__init__(self)
        self.filters = ['none']
        self.thresholds = [None]
        self.name = "c1"

class Config3(Config):
    def __init__(self):
        Config.__init__(self)
        self.filters = ['tfidf']#, 'cf', 'df']
        self.thresholds = [15]#[5, 10, 15]
        self.name = "c3"

class Config5(Config3):
    def __init__(self):
        Config3.__init__(self)
        self.preFilter = True
        self.name = 'c5'

class Config6(Config):
    def __init__(self):
        Config.__init__(self)
        self.filters = ['none', 'tfidf']
        self.thresholds = [15] #[5, 10, 15]
        self.name = "c6"
        self.useSubBags = True
        self.useNeighbours = False

class Config6b(Config6):
    def __init__(self):
        Config6.__init__(self)
        self.useNeighbours = True

def runExperiments(outputBaseFolder, printToJson):
    dataDir = os.path.join(os.getcwd(), '..', 'data')
    d1 = ('d1', ['reuters.jl', 'cbs.jl', 'pbs.jl'])
    d2 = ('d2', ['obama09.jl', 'obama10.jl', 'obama11.jl'])
    d3 = ('d3', ['ww2.jl'])
    d4 = ('d4', ['reutersNews0308.jl'])
    datasets = []
    for d in [d1, d2, d3, d4]:
        paths = [os.path.join(dataDir, x) for x in d[1]]
        newD = (d[0], paths)
        datasets.append(newD)


    c1 = Config1()
    c3 = Config3()
    c5 = Config5()
    c6 = Config6()
    c6b = Config6b()
    configs = [c1, c3, c5, c6]#6b TODO: more configs

    filenameFormat = "{config}-{filter}-{threshold}-{preFilter}-{subBags}-{neighbours}.txt"
    for dataset in datasets:
        for config in configs:
            for f in config.filters:
                for threshold in config.thresholds:
                    outputFile = os.path.join(
                            outputBaseFolder,
                            dataset[0],
                            filenameFormat.format(
                                config = config.name,
                                filter = f,
                                preFilter = 'preFilter' if config.preFilter else 'postFilter',
                                threshold = threshold,
                                subBags = 'subBags' if config.useSubBags else "normal",
                                neighbours = 'useNeighbours' if config.useNeighbours else '',
                                )
                            )


                    print "Running: " + outputFile
                    main.main(
                            threshold,
                            f,
                            dataset[1],
                            outputFile,
                            config.useSubBags,
                            printToJson,
                            config.useNeighbours,
                            config.preFilter)

                    if f == 'none':
                        break

if __name__ == "__main__":
    resultPath = os.path.join(os.getcwd(), '..', 'moreResults')
    printToJson = False
    runExperiments(resultPath, printToJson)

