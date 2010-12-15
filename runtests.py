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
    parser.add_option("-b", "--bench",
                      action="store_true",
                      dest="bench",
                      default=False,
                      help="Run benchmarks")
    parser.add_option("-l", "--list",
                      action="store_true",
                      dest="show_list",
                      default=False,
                      help="Show the list of available profiling tests")
    parser.add_option("-p", "--proxy",
                      action="store",
                      dest="proxy",
                      default='',
                      help="Set the HTTP_PROXY environment variable")
    return parser

    
if __name__ == '__main__':
    try:
        import _dep
    except ImportError:
        pass
    options, tags = makeoptions().parse_args()
    if options.proxy:
        from dynts.conf import settings
        settings.proxies['http'] = options.proxy
    if options.bench:
        runner = dynts.runbench
    else:
        runner = dynts.runtests
        
    runner(tags,
           verbosity=options.verbosity,
           show_list=options.show_list)
    