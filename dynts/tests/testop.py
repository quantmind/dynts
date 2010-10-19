import random
from dynts.test import TestCase
from dynts.backends import ops

__all__ = ['TestOperators',
           ]


class TestOperators(TestCase):

    def testTSArithOperators(self):
        ts1, dates1, data1 = self.getts(returndata = True, cols = 2)
        ts2, dates2, data2 = self.getts(returndata = True, cols = 2)
        for op in ops.values():
           # print op
            ts3 = op(ts1,ts2)
            exp = map(op, data1, data2)
            self.check_dates(ts3, dates1) #the dates should be the same
            self.check_values(ts3, exp) #the values should be 

    def testScalarArithOperators(self):
        delta = random.uniform(1.0,100.0)
        ts, dates, data = self.getts(returndata = True)
        for op in ops.values():
            new_ts = op(ts, delta)
            curry_op = lambda x : op(x, delta)

            exp = map(curry_op, data)
            self.check_dates(new_ts, dates)
            self.check_values(new_ts, exp)

