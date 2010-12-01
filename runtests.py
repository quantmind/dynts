#!/usr/bin/env python

import os
import sys
from optparse import OptionParser

import dynts


def makeoptions():
    parser = OptionParser()
    parser.add_option("-v", "--verbosity",
                      type = int,
                      action="store",
                      dest="verbosity",
                      default=1,
                      help="Tests verbosity level, one of 0, 1, 2 or 3")
    return parser

    
if __name__ == '__main__':
    options, tags = makeoptions().parse_args()
    dynts.runtests(tags, verbosity=options.verbosity)