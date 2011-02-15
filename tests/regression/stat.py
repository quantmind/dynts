#
from datetime import date

from dynts import test, timeseries
from dynts.utils.populate import datepopulate
from dynts.utils.py2py3 import range
from dynts.exceptions import *


class TestStat(test.TestCase):
    
    def testVar(self):
        '''Calculate the biased variance of a series'''
        ts = timeseries(date = datepopulate(10), data = range(1,11), backend = self.backend)
        self.assertAlmostEqual(ts.var()[0],8.25)
        self.assertAlmostEqual(ts.var(ddof=1)[0],9.166667)