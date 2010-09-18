import unittest
import numpy as np
import random
from dynts.utils.populate import populate
from dynts.utils.populate import datepopulate
from dynts.backends.dev import TSWithOperators as TimeSeries

__all__ = ['TestOperators',
           ]

add = lambda x, y : x + y
sub = lambda x, y : x - y
mul = lambda x, y : x * y
div = lambda x, y : x / y

def isiterable(a):
    return hasattr(a,'__iter__')

class CommonTSUtils(unittest.TestCase):

    def getdata(self, size = 100, cols = 1,delta = 1):
        date = datepopulate(size = size, delta = delta)
        data = populate(size = size, cols = cols)
        return date,data

    def getts(self, returndata = False, cols = 1, delta = 1):
        date,data = self.getdata(100,cols = cols,delta = delta)

        ts   = TimeSeries(name = 'test', date = date, data = data)
        if returndata:
            return ts,list(date),list(data)
        else:
            return ts
        
    def assertAlmostEqual(self, a, b): #copied from pandas
        if isiterable(a):
            np.testing.assert_(isiterable(b))
            np.testing.assert_equal(len(a), len(b))
            for i in xrange(len(a)):
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

#    def assertAlmostEqual(self, exp, recv, tol = 2, msg = None):
#        if msg is None:
#            msg = "Values do not match expected %s, received %s" %(exp, recv)
#        unittest.TestCase.assertAlmostEqual(self, exp,recv, tol, msg)

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

class TestOperators(CommonTSUtils):

    ops = (add, sub, mul, div)
    def testTSArithOperators(self):
        ops = self.ops
        ts1, dates1, data1 = self.getts(returndata = True, cols = 2)
        ts2, dates2, data2 = self.getts(returndata = True, cols = 2)
        for op in ops:
           # print op
            ts3 = op(ts1,ts2)
            exp = map(op, data1, data2)
            self.check_dates(ts3, dates1) #the dates should be the same
            self.check_values(ts3, exp) #the values should be 

    def testScalarArithOperators(self):
        ops = self.ops
        delta = random.uniform(1.0,100.0)
        ts, dates, data = self.getts(returndata = True)
        for op in ops:
            new_ts = op(ts, delta)
            curry_op = lambda x : op(x, delta)

            exp = map(curry_op, data)
            self.check_dates(new_ts, dates)
            self.check_values(new_ts, exp)

