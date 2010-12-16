from itertools import izip

from dynts.test import TestCase
from dynts import BasicStatistics, pivottable


class StatisticsTest(TestCase):
    
    def testSimpleStatistics(self):
        ts = self.getts(cols = 4)
        b = BasicStatistics(ts)
        self.assertEqual(b.count(), 4)
        data = b.calculate()
        names = data['names']
        self.assertEqual(len(names), 4)
        data = b.calculate()
        self.assertEqual(data['names'],names)
        
    def testSimplePivot(self):
        ts = self.getts(cols = 4)
        b = BasicStatistics(ts)
        p = pivottable(b.calculate())
        d = p.defaultname
        self.assertEqual(len(p.names),ts.count())
        for field in p.fields:
            self.assertEqual(p.get(field),p.get(field,d))
            
    def testFullPivot(self):
        ts = self.getts(cols = 4)
        b = BasicStatistics(ts)
        p = pivottable(b.calculate())
        for field in p.fields:
            for name in p.names:
                val = p.get(field,name)
                dt  = dict(izip(p.data['names'],p.data[field]))
                self.assertEqual(val,dt[name])
            
    def testPrangeFunction(self):
        ts = self.getts(cols = 4)
        b = BasicStatistics(ts)
        p = pivottable(b.calculate())
        range = p.get('prange')
        min   = p.get('min')
        max   = p.get('max')
        lat   = p.get('latest')
        self.assertEqual(range,100.*(lat-min)/(max-min))
        
    def testRangeFunction(self):
        ts = self.getts(cols = 4)
        b = BasicStatistics(ts)
        p = pivottable(b.calculate())
        range = p.get('range')
        min   = p.get('min')
        max   = p.get('max')
        self.assertEqual(range,[min,max])
        
    def __testFunctions(self):
        '''Not working yet'''
        ts = self.getts(cols = 4)
        b = BasicStatistics(ts, functions=['min','max','mean','zscore'])
        d = b.calculate()
        self.assertEqual(len(d),6)
        p = pivottable(d)
        self.assertEqual(len(p.fields),5)
        