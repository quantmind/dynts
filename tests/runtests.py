import logging
import os
import sys
import dynts
from dynts.test import TestSuiteRunner
from dynts.utils.importlib import import_module 

logger = logging.getLogger('dynts')

# directories for testing
LIBRARY        = 'dynts'
TEST_FOLDERS   = ('regression',)

CUR_DIR        = os.path.split(os.path.abspath(__file__))[0]
ALL_TEST_PATHS = [os.path.join(CUR_DIR,td) for td in TEST_FOLDERS]
if CUR_DIR not in sys.path:
    sys.path.insert(0,CUR_DIR)

LOGGING_MAP = {1: logging.CRITICAL,
               2: logging.INFO,
               3: logging.DEBUG}


class Silence(logging.Handler):
    def emit(self, record):
        pass 


def get_tests():
    tests = []
    join  = os.path.join
    for dirpath in ALL_TEST_PATHS:
        loc = os.path.split(dirpath)[1]
        for d in os.listdir(dirpath):
            if os.path.isdir(join(dirpath,d)):
                tests.append((loc,d))
    return tests


def import_tests(tags):
    apptests = {}
    for loc,app in get_tests():
        if tags and app not in tags:
            logger.debug("Skipping tests for %s" % app)
            continue
        logger.debug("Try to import tests for %s" % app)
        test_module = '{0}.{1}.tests'.format(loc,app)
        if loc == 'contrib':
            test_module = '{0}.{1}'.format(LIBRARY,test_module)
            
        try:
            mod = import_module(test_module)
        except ImportError, e:
            logger.debug("Could not import tests for %s: %s" % (test_module,e))
            raise
        
        logger.debug("Adding tests for %s" % app)
        apptests[app] = mod
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
        print('{0} : {1}'.format(name,mod.__doc__))
        

def run_regression(tags, verbosity, show_list):
    '''Run regression tests'''
    modules = import_tests(tags)
    if show_list:
        dynts.showtestlist(modules)
    else:
        runner  = TestSuiteRunner(verbosity = verbosity)
        runner.run_tests(modules.values())
        

def run_bench(tags, verbosity, show_list):
    '''Run benchmark tests'''
    modules = import_tests(tags)
    if show_list:
        dynts.showtestlist(modules)
    else:
        runner  = TestSuiteRunner(verbosity = verbosity)
        runner.run_tests(modules.values())
        

def run_profile(tags, verbosity, show_list):
    '''Run profile tests'''
    modules = import_tests(tags)
    if show_list:
        dynts.showtestlist(modules)
    else:
        runner  = TestSuiteRunner(verbosity = verbosity)
        runner.run_tests(modules.values())
        

TEST_TYPES = {'regression': run_regression,
              'bench': run_bench,
              'profile': run_profile}

def test_names():
    return ', '.join(TEST_TYPES)

    
def run(tags, test_type,
        verbosity = 1,
        show_list = False):
    runner = TEST_TYPES.get(test_type,None)
    if not runner:
        print('Unknow test type {0}. Choose one from {1}'.format(test_type,test_names()))
    setup_logging(verbosity)
    runner(tags,verbosity,show_list)

