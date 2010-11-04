
import unittest
import dynts
import itertools

__all__ = ['FunctionTest',
           ]
class FunctionTest(unittest.TestCase):
    '''
    This is a dynamic unittest function generating class
    The idea is that all functions should be tested against all the backends
    The list of functions is stored as a constant in the dsl module, while the 
    
    '''
    
    _initialised = False
    
    
    @classmethod
    def initialise(cls, backends, functions):
        initiated = cls._initialised
        if initiated:
            return None
        else:
            for backend, function in itertools.product(backends, functions):
                cls.create_test(function, backend)
        
        cls._initialised = True
            
    
    @classmethod    
    def create_test(cls, function, backend):
        fn = lambda self: self.allchecks(function, backend)
        test_name = 'test_%s_%s' %(function, backend)
        setattr(cls, test_name, fn)
            
        
    def allchecks(self, function, backend):
        self.checkNoParameters(function, backend)
        self.checkTwoSeries(function, backend)
        self.checkWindowParameter(function, backend)
        
    def assertTimeSeries(self, data, msg = None):
        if msg is None:
            msg = "Expected a timeseries received %s instead" %data.__class__
        self.assertTrue(dynts.istimeseries(data), msg)
    
    def checkNoParameters(self, function, backend):
        '''Test function with zero parameters against a given backend'''
        expression = '%s(GOOG)' % function
        result = dynts.evaluate(expression, backend = backend)
        self.assertEqual(str(result),expression)
        self.assertEqual(len(result.data),1)
        data = result.ts()
        self.assertTimeSeries(data)
        self.assertEqual(data.count(),1)
        
    def checkWindowParameter(self, function, backend):
        '''Test mean function with one parameter'''
        e = '%(f)s(GOOG,window=30),%(f)s(GOOG,window=60)' % {'f':function}
        result = dynts.evaluate(e, backend = backend)
        symbols = result.expression.symbols()
        self.assertEqual(len(symbols),1)
        self.assertEqual(len(result.data),1)
        data = result.ts()
        self.assertTimeSeries(data)
        self.assertEqual(data.count(),2)
        
    def checkTwoSeries(self, function, backend):
        e = '%s(GOOG,YHOO)' % function
        result = dynts.evaluate(e, backend = backend)
        symbols = result.expression.symbols()
        self.assertEqual(len(symbols),2)
        self.assertEqual(len(result.data),2)
        data = result.ts()
        self.assertTimeSeries(data)
        self.assertEqual(data.count(),2)
        
FunctionTest.initialise(dynts.backends.BACKENDS.keys(),
                        functions = dynts.dsl.functions.FUNCTIONS
                        )



#import unittest
#import random
#from dynts.utils.populate import populate
#from dynts.utils.populate import datepopulate
#
#__all__ = ['DevTestTS',
#           ]

#class CommonTSUtils(unittest.TestCase):
#
#    def getdata(self, size = 100, delta = 1):
#        date = datepopulate(size = size, delta = delta)
#        data = populate(size = size)
#        return date,data
#
#    def getts(self, returndata = False, delta = 1):
#        date,data = self.getdata(100,delta)
#
#        ts   = TimeSeries(name = 'test', ts = zip(date, data))
#        if returndata:
#            return ts,list(date),list(data)
#        else:
#            return ts
#
#    def assertAlmostEqual(self, exp, recv, tol = 2, msg = None):
#        if msg is None:
#            msg = "Values do not match expected %s, received %s" %(exp, recv)
#        unittest.TestCase.assertAlmostEqual(self, exp,recv, tol, msg)
#
#class DevTestTS(CommonTSUtils):
#
#    def xtestAddTS(self):
#        ts1, _, data1 = self.getts(returndata = True)
#        ts2, _, data2 = self.getts(returndata = True)
#        ts3 = ts2 + ts1
#
#        exp = sum(data1) + sum(data2)
#        recv = sum(ts3.values())
#        self.assertAlmostEqual(exp, recv)
#
#    def xtestAddScalar(self):
#        delta = random.uniform(1.0,100.0)
#        ts, dates, data = self.getts(returndata = True)
#        new_ts = ts + delta
#        for dt, val in zip(dates, data):
#            exp = val + delta
#            recv = new_ts[dt]
#            self.assertAlmostEqual(exp, recv)


################==============

#
# NOT USED DIRECTLY - THIS MODULE IS IMPORTED BY dynts.tests
#