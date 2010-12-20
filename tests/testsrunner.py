import logging
import os
import sys
import pstats

import dynts
from dynts.test import TestSuiteRunner, runbench
from dynts.utils.importlib import import_module 

logger = logging.getLogger('dynts')

LOGGING_MAP = {1: logging.CRITICAL,
               2: logging.INFO,
               3: logging.DEBUG}


class Silence(logging.Handler):
    def emit(self, record):
        pass 


def showtestlist(ld):
    print('')
    print(('There are a total of {0} tests.'.format(len(ld))))
    print('')
    for name in sorted(ld.keys()):
        mod = ld[name]
        print(('{0} :    {1}'.format(name,mod.__doc__)))


def get_tests(paths, dirs = False, filename = None):
    tests = []
    join  = os.path.join
    filename = filename or 'tests'
    for dirpath in paths:
        loc = os.path.split(dirpath)[1]
        for d in os.listdir(dirpath):
            if d.startswith('_'):
                continue
            modname = None  
            elem = join(dirpath,d)
            if dirs and os.path.isdir(elem):
                name = d
                modname = '{0}.{1}.{2}'.format(loc,d,filename)
            elif not dirs and os.path.isfile(elem):
                name,ext = d.split('.')
                if ext == 'pyc':
                    continue
                modname = '{0}.{1}'.format(loc,name)
            
            if name and modname:
                tests.append((name,modname))
                
    return tests


def import_tests(tags, paths, dirs = False, filename = None):
    apptests = {}
    for name,modname in get_tests(paths, dirs = dirs, filename = filename):
        if tags and name not in tags:
            logger.debug("Skipping tests for %s" % name)
            continue
        logger.debug("Try to import tests for %s" % name)
            
        try:
            mod = import_module(modname)
        except ImportError as e:
            logger.critical("Could not import tests for %s: %s" % (modname,e))
            continue
        
        logger.debug("Adding tests for %s" % name)
        apptests[name] = mod
    return apptests


def setup_logging(verbosity):
    level = LOGGING_MAP.get(verbosity,None)
    if level is None:
        logger.addHandler(Silence())
    else:
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(level)
        

def showlist(modules):
    for name in sorted(modules.keys()):
        mod = modules[name]
        print(('{0} : {1}'.format(name,mod.__doc__)))
        

def run_regression(tags, paths, verbosity, show_list):
    '''Run regression tests'''
    modules = import_tests(tags, paths, dirs=True, filename='tests')
    if show_list:
        showtestlist(modules)
    else:
        runner  = TestSuiteRunner(verbosity = verbosity)
        runner.run_tests(list(modules.values()))
        

def run_bench(tags, paths, verbosity, show_list):
    '''Run benchmark tests'''
    modules = import_tests(tags, paths)
    if show_list:
        showtestlist(modules)
    else:
        runbench(list(modules.values()), tags, verbosity)
        

def run_profile(tags, paths, verbosity, show_list):
    '''Run profile tests'''
    modules = import_tests(tags, paths)
    if show_list:
        showtestlist(modules)
    else:
        if not tags:
            print('You need to pass a profile test name to profile.')
            print('Check the list by typing runprofile --list.')
        else:
            name = tags[0]
            mod = modules.get(name,None)
            if mod:
                mod.run()
                s = pstats.Stats("Profile.prof")
                s.strip_dirs().sort_stats("time").print_stats()
            else:
                print(('Unknonw test {0}.'.format(name)))
        

TEST_TYPES = {'regression': run_regression,
              'bench': run_bench,
              'profile': run_profile}

def test_names():
    return ', '.join(TEST_TYPES)

    
def run(tags,
        test_type,
        path,
        verbosity = 1,
        show_list = False):
    runner = TEST_TYPES.get(test_type,None)
    if not runner:
        print(('Unknow test type {0}. Choose one from {1}'.format(test_type,test_names())))
    setup_logging(verbosity)
    tpath = os.path.join(path,test_type)
    runner(tags,[tpath],verbosity,show_list)

