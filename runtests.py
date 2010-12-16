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
    parser.add_option("-t", "--type",
                      action="store",
                      dest="test_type",
                      default='regression',
                      help="Test type, possible choices are: regression, bench and profile")
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
    parser.add_option("-d", "--docs",
                      action="store_true",
                      dest="docs",
                      default=False,
                      help="Dump function documentation.")
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
    
    if options.docs:
        dynts.dump_docs()
    else:
        # add the tests directory to the Python Path
        p = os.path
        path = p.join(p.split(p.abspath(__file__))[0],'tests')
        sys.path.insert(0, path)
        from testsrunner import run
            
        run(tags,
            options.test_type,
            path,
            verbosity=options.verbosity,
            show_list=options.show_list)
        