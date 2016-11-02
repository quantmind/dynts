import sys
import unittest
from io import BytesIO
from itertools import zip_longest

import numpy as np

from ..conf import settings
from ..api import timeseries, randomts, evaluate, tsname

from .populate import populate, datepopulate

skipUnless = unittest.skipUnless


def haszoo():
    try:
        from dynts.backends.zoo import TimeSeries
    except ImportError:
        return False
    try:
        st = sys.stdout
        sys.stdout = BytesIO()
        t = TimeSeries()
        sys.stdout = st
        return True
    except dynts.MissingPackage:
        return False


class TestCase(unittest.TestCase):
    backend = 'numpy'
    fallback = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.evaluate = evaluate
        self.tsname = tsname
        self.datepopulate = datepopulate
        self.populate = populate

    def setUp(self):
        if self.backend:
            self._oldbe = settings.backend
            settings.backend = self.backend

    def tearDown(self):
        if self.backend:
            settings.backend = self._oldbe

    def randomts(self, **kwargs):
        return randomts(backend=self.backend, **kwargs)

    def getdata(self, size=100, cols=1, delta=1, start=None):
        dates = self.datepopulate(size=size, delta=delta)
        data = self.populate(size=size, cols=cols)
        return dates, data

    def getts(self, returndata=False, delta=1, cols=1, size=100):
        '''Return a timeseries filled with random data'''
        dates, data = self.getdata(size, cols, delta)
        ts = self.timeseries(name='test', date=dates, data=data)
        self.assertEqual(ts.shape, (size, cols))
        self.assertEqual(len(ts), size)
        self.assertEqual(ts.count(), cols)
        if returndata:
            return ts, list(dates), list(data)
        else:
            return ts

    def timeseries(self, name='', date=None, data=None):
        return timeseries(name=name, date=date, data=data,
                          backend=self.backend)

    def isiterable(self, a):
        return hasattr(a, '__iter__')

    def assertAlmostEqual(self, a, b, places=7, msg=None):
        if isinstance(a, np.ndarray) and isinstance(b, np.ndarray):
            self.assertEqual(a.shape, b.shape)
            a = a.flat
            b = b.flat
        if self.isiterable(a):
            self.assertTrue(self.isiterable(b))
            for x, y in zip_longest(a, b):
                self.assertAlmostEqual(x, y, places=places, msg=msg)
            return True
        else:
            return super().assertAlmostEqual(a, b, places=places, msg=msg)

    def assertEqual(self, exp, recv, msg = None):
        if msg is None:
            msg = "Values do not match expected %s, received %s" % (exp, recv)
        unittest.TestCase.assertEqual(self, exp, recv, msg)

    def check_dates(self, ts, dts):
        ts_dts = list(ts.dates())
        self._check_vectors(ts_dts, dts, equal=True)

    def check_values(self, ts, vals):
        ts_vals = list(ts.values())
        self._check_vectors(ts_vals, vals, equal=False)

    def _check_vectors(self, v1, v2, equal=True):
        lv1 = len(v1)
        lv2 = len(v2)
        self.assertEqual(lv1, lv2, "Vectors are of different lengths %s, %s"
                         % (lv1, lv2))

        for a, b  in zip(v1, v2):
            if equal:
                self.assertEqual(a, b)
            else:
                self.assertAlmostEqual(a, b)
