#!/usr/bin/env python
import os
import sys
import argparse

import dynts
from dynts.conf import settings

try:
    import pulsar
    from pulsar.apps.test import TestOptionPlugin
    
    class HttpProxy(TestOptionPlugin):
        name = "http_proxy"
        flags = ["--proxy"]
        desc = 'Set the HTTP_PROXY environment variable.'
        
        def configure(self, cfg):
            settings.proxies['http'] = cfg.http_proxy
            
except ImportError:
    pulsar = None
    
try:
    import nose
    from nose import plugins
    
    class NoseHttpProxy(plugins.Plugin):
    
        def options(self, parser, env=os.environ):
            parser.add_option('--http_proxy',
                          dest='http_proxy',
                          default='',
                          help="Set the HTTP_PROXY environment variable.")
    
        def configure(self, options, conf):
            self.enabled = True
            settings.proxies['http'] = options.http_proxy
    
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
                description = 'Dynts Asynchronous test suite',
                    modules = ('tests',),
                    plugins = (HttpProxy(),
                               profile.Profile(),
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