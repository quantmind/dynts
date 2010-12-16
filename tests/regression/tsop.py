import random
from dynts.test import TestCase
from dynts.backends import ops
from dynts import exceptions 


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
    
    def testArithOpWithDiffNumberCols(self):
        '''
        you can't perform arithmetic on timeseries that each have a different number of columns
        '''
        ts1 = self.getts(cols = 2)
        ts2 = self.getts(cols = 1)
        
        op = ops.values()[0]
        
        curry_fn = lambda : op(ts1, ts2)
        self.assertRaises(exceptions.ExpressionError, curry_fn)
    
    def testArithOpWithMissingDates(self):
        ts1, dates1, data1 = self.getts(returndata = True, cols = 2)
        ts2, dates2, data2 = self.getts(returndata = True, cols = 2, delta = 2)
        
        all_dates = list(set(dates1).union(set(dates2)))
        all_dates.sort()
        op = ops.values()[0]
        ts3 = op(ts1,ts2)
        self.check_dates(ts3, all_dates) ##Check that all the dates are in the return series by default
        
        btree = ts3.asbtree()
        not_in_dates2 = set(dates1) - set(dates2)
        self._check_missing_dts(not_in_dates2, btree)
        
        not_in_dates1 = set(dates2) - set(dates1)
        self._check_missing_dts(not_in_dates1, btree)
        
    def _check_missing_dts(self, dts, btree):
        from dynts.conf import settings
        ismissing = settings.ismissing
        
        for dt in  dts:
            vals = btree[dt]
            for val in vals:
                self.assertTrue(ismissing(val))
        