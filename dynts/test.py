import unittest
import numpy as np
from datetime import date
from itertools import izip

from dynts import timeseries, evaluate, tsname
from dynts.utils.populate import populate, datepopulate, randomts


class TestCase(unittest.TestCase):
    backend = None
    
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

        for a,b  in izip(v1,v2):
            if equal:
                self.assertEqual(a, b)
            else:
                self.assertAlmostEqual(a,b)
