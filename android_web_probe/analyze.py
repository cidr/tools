#! /usr/bin/env python

import os
import sys
import logging
import argparse
import numpy

sys.path.append('../myplot')
import myplot

sys.path.append('pt4utils')
from pt4_filereader import Pt4FileReader


def main():
    for smpl in Pt4FileReader.readAsVector(args.pt4file):
        print(smpl[2])



if __name__ == "__main__":
    # set up command line args
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,\
                                     description='Analyze power monitor logs.')
    parser.add_argument('pt4file', help='pt4 power monitor file to analyze.')
    parser.add_argument('-q', '--quiet', action='store_true', default=False, help='only print errors')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='print debug info. --quiet wins if both are present')
    args = parser.parse_args()

    # set up logging
    if args.quiet:
        level = logging.WARNING
    elif args.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(
        format = "%(levelname) -10s %(asctime)s %(module)s:%(lineno) -7s %(message)s",
        level = level
    )

    main()
