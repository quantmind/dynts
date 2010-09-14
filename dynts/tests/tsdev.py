import unittest
import random
from dynts.utils.populate import populate
from dynts.utils.populate import datepopulate
from othello.impl.tseries import TimeSeries

__all__ = ['DevTestTS',
           ]

class CommonTSUtils(unittest.TestCase):

    def getdata(self, size = 100, delta = 1):
        date = datepopulate(size = size, delta = delta)
        data = populate(size = size)
        return date,data

    def getts(self, returndata = False, delta = 1):
        date,data = self.getdata(100,delta)

        ts   = TimeSeries(name = 'test', ts = zip(date, data))
        if returndata:
            return ts,list(date),list(data)
        else:
            return ts

    def assertAlmostEqual(self, exp, recv, tol = 2, msg = None):
        if msg is None:
            msg = "Values do not match expected %s, received %s" %(exp, recv)
        unittest.TestCase.assertAlmostEqual(self, exp,recv, tol, msg)

class DevTestTS(CommonTSUtils):

    def xtestAddTS(self):
        ts1, _, data1 = self.getts(returndata = True)
        ts2, _, data2 = self.getts(returndata = True)
        ts3 = ts2 + ts1

        exp = sum(data1) + sum(data2)
        recv = sum(ts3.values())
        self.assertAlmostEqual(exp, recv)

    def xtestAddScalar(self):
        delta = random.uniform(1.0,100.0)
        ts, dates, data = self.getts(returndata = True)
        new_ts = ts + delta
        for dt, val in zip(dates, data):
            exp = val + delta
            recv = new_ts[dt]
            self.assertAlmostEqual(exp, recv)
