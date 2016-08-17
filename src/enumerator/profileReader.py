#! /usr/bin/env python

#Profile reader

import sys
import pstats
import argparse

def main(proFile, output):
    isPrintToFile = output is not ''
    retcode = 0
    try:
        if isPrintToFile:
            f = open(output, 'w')
            p = pstats.Stats(proFile, stream=f)
        else:
            p = pstats.Stats(proFile)
        p.strip_dirs().sort_stats('time').print_stats()
    except Exception, m:
        sys.stderr.write("Error: {message}".format(m))
        sys.stder.flush()
        retcode = 1
    finally:
        if isPrintToFile:
            f.close()
        return retcode


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', default="")
    parser.add_argument('profile')
    args = parser.parse_args()
    ret = main(args.profile, args.output)
    sys.exit(ret)

