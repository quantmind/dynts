from datetime import date, timedelta
import numpy as np

from dynts import test, timeseries


class TestFunctionTS(test.TestCase):
    
    def get(self):
        ts = timeseries(dtype = object)
        self.assertTrue(ts.is_object)
        self.assertEqual(ts.dtype, np.dtype(object))
        
    def testSimple(self):
        self.get()
    
    def testHashEmpty(self):
        ts = timeseries(dtype = object)
        h = ts.ashash()
        self.assertFalse(h)
        dt1 = date.today()
        dt0 = date.today()-timedelta(days=1)
        h[dt1] = [56,48]
        h[dt0] = 'this is a string'
        self.assertEqual(len(h),2)
        ts = h.getts()
        self.assertEqual(len(ts),2)
        self.assertEqual(ts[0][0], 'this is a string')
        self.assertEqual(ts[1][0], [56,48])