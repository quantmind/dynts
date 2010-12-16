import os
import unittest
from datetime import date

import types

import numpy as np

from dynts import timeseries, evaluate, tsname
from dynts.utils.importlib import import_modules
from dynts.utils.populate import populate, datepopulate, randomts


TextTestRunner = unittest.TextTestRunner


class TestCase(unittest.TestCase):
    backend = None
    fallback = False
    
    def __init__(self,*args,**kwargs):
        super(TestCase,self).__init__(*args,**kwargs)
        self.np = np
        self.timeseries = timeseries
        self.evaluate = evaluate
        self.tsname = tsname
        self.datepopulate = datepopulate
        self.populate = populate
        self.randomts = randomts
        
    def getdata(self, size = 100, cols = 1, delta = 1, start = None):
        dates = self.datepopulate(size = size, delta = delta)
        data = self.populate(size = size, cols = cols)
        return dates,data
        
    def getts(self, returndata = False, delta = 1, cols = 1, size = 100):
        '''Return a timeseries filled with random data'''
        dates,data = self.getdata(size,cols,delta)
        ts   = self.timeseries(name = 'test', date = dates, data = data, backend = self.backend)
        self.assertEqual(ts.shape,(size,cols))
        self.assertEqual(len(ts),size)
        self.assertEqual(ts.count(),cols)
        if returndata:
            return ts,list(dates),list(data)
        else:
            return ts
        
    def isiterable(self, a):
        return hasattr(a,'__iter__')

    def assertAlmostEqual(self, a, b): #copied from pandas
        if self.isiterable(a):
            np.testing.assert_(self.isiterable(b))
            np.testing.assert_equal(len(a), len(b))
            for i in range(len(a)):
                self.assertAlmostEqual(a[i], b[i])
            return True

        err_msg = lambda a, b: 'expected %.5f but got %.5f' % (a, b)

        if np.isnan(a):
            np.testing.assert_(np.isnan(b))
            return

        # case for zero
        if abs(a) < 1e-5:
            np.testing.assert_almost_equal(a, b, decimal=5, err_msg=err_msg(a, b), verbose=False)
        else:
            np.testing.assert_almost_equal(1, a/b, decimal=5, err_msg=err_msg(a, b), verbose=False)
            
    def assertEqual(self, exp, recv, msg = None):
        if msg is None:
            msg = "Values do not match expected %s, received %s" %(exp, recv)
        unittest.TestCase.assertEqual(self, exp,recv,msg)

    def check_dates(self, ts, dts):
        ts_dts = list(ts.dates())
        self._check_vectors(ts_dts, dts, equal=True)
        
    def check_values(self, ts, vals):
        ts_vals = list(ts.values())
        self._check_vectors(ts_vals, vals, equal=False)

    def _check_vectors(self, v1, v2, equal=True):
        lv1 = len(v1)
        lv2 = len(v2)
        self.assertEqual(lv1, lv2, "Vectors are of different lengths %s, %s" %(lv1, lv2))

        for a,b  in zip(v1,v2):
            if equal:
                self.assertEqual(a, b)
            else:
                self.assertAlmostEqual(a,b)


        

class TestSuite(unittest.TestSuite):
    pass


class TestSuiteRunner(object):
    '''A suite runner with twisted if available.'''
    
    def __init__(self, verbosity = 1):
        self.verbosity = verbosity
        
    def setup_test_environment(self):
        pass
    
    def teardown_test_environment(self):
        pass
    
    def run_tests(self, modules):
        self.setup_test_environment()
        suite = self.build_suite(modules)
        self.run_suite(suite)
    
    def close_tests(self, result):
        self.teardown_test_environment()
        return self.suite_result(suite, result)
    
    def build_suite(self, modules):
        loader = TestLoader()
        return loader.loadTestsFromModules(modules)
        
    def run_suite(self, suite):
        return TextTestRunner(verbosity = self.verbosity).run(suite)
    
    def suite_result(self, suite, result, **kwargs):
        return len(result.failures) + len(result.errors) 
     

class TestLoader(unittest.TestLoader):
    suiteClass = TestSuite
    
    def loadTestsFromModules(self, modules):
        """Return a suite of all tests cases contained in the given module"""
        tests = []
        for module in modules:
            for name in dir(module):
                obj = getattr(module, name)
                if (isinstance(obj, type) and
                    issubclass(obj, unittest.TestCase)):
                    tests.append(self.loadTestsFromTestCase(obj))
        return self.suiteClass(tests)
        

        
class BenchMark(object):
            
    def __str__(self):
        return self.__class__.__name__
        
    def setUp(self):
        pass
    
    
class BenchLoader(TestLoader):
    bclass = BenchMark
    
    def loadTestsFromModule(self, module):
        """Return a suite of all tests cases contained in the given module"""
        tests = self.tests
        for name in dir(module):
            cls = getattr(module, name)
            if (isinstance(cls, type) and
                issubclass(cls, self.bclass)):
                tests.append(cls())
    
    def loadBenchFromModules(self, modules): 
        modules = import_modules(modules)
        self.tests = []
        for mod in modules:
            self.loadTestsFromModule(mod)
        return self.tests

    
def runbench(benchs, tags, verbosity, bclass = BenchMark):
    from timeit import Timer
    t = Timer("test()", "from __main__ import test")
    for mod in benchs:
        for name in dir(mod):
            cls = getattr(mod, name)
            if (isinstance(cls, type) and issubclass(cls, bclass)):
                name = cls.__name__
                path = cls.__module__
                t = Timer("b.run()",
                          'from %s import %s\nb = %s()\nb.setUp()' % (path,name,name))
                t = t.timeit(cls.number)
                nice_name = name.replace('_',' ')
                print(('Run %15s --> %s' % (nice_name,t)))
        