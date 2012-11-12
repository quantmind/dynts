#!/usr/bin/env python
import os
import sys

import dynts
from environment import pulsar
    
try:
    import nose
    from nose import plugins
        
    def noseoption(argv,*vals,**kwargs):
        if vals:
            for val in vals:
                if val in argv:
                    return
            argv.append(vals[0])
            value = kwargs.get('value')
            if value is not None:
                argv.append(value)
                    
except ImportError:
    nose = None

    
def start():
    global pulsar
    argv = sys.argv
    if len(argv) > 1 and argv[1] == 'nose':
        pulsar = None
        sys.argv.pop(1)
    
    if pulsar:
        from pulsar.apps.test import TestSuite
        from pulsar.apps.test.plugins import bench, profile
        
        os.environ['stdnet_test_suite'] = 'pulsar'
        suite = TestSuite(
                description='Dynts Asynchronous test suite',
                    plugins=(profile.Profile(),
                             bench.BenchMark(),)
                  )
        suite.start()
    elif nose:
        os.environ['stdnet_test_suite'] = 'nose'
        argv = list(sys.argv)
        noseoption(argv, '-w', value = 'tests/regression')
        noseoption(argv, '--all-modules')
        nose.main(argv=argv, addplugins=[NoseHttpProxy()])
    else:
        print('To run tests you need either pulsar or nose.')
        exit(0)

if __name__ == '__main__':
    start()