import unittest
from itertools import izip

from dynts import timeseries
from dynts.utils.populate import populate, datepopulate, randomts, date
from dynts.exceptions import *


class TestTS(unittest.TestCase):
    backend = None
    
    def getdata(self, size = 100, cols = 1, delta = 1, start = None):
        dates = datepopulate(size = size, delta = delta)
        data = populate(size = size, cols = cols)
        return dates,data
        
    def getts(self, returndata = False, delta = 1, cols = 1, size = 100):
        dates,data = self.getdata(size,cols,delta)
        ts   = timeseries(name = 'test', date = dates, data = data, backend = self.backend)
        self.assertEqual(ts.shape,(size,cols))
        self.assertEqual(len(ts),size)
        self.assertEqual(ts.count(),cols)
        if returndata:
            return ts,list(dates),list(data)
        else:
            return ts
    
    def testInit(self):
        ts,dates,data = self.getts(True)
        self.assertEqual(ts.type,self.backend)
        self.assertEqual(len(ts),len(dates))
        for dt,dt1 in izip(dates,ts.dates()):
            self.assertEqual(dt,dt1)
        
    def test_isregular(self):
        ts = self.getts()
        self.assertTrue(ts.isregular())
            
    def test_frequency(self):
        ts = self.getts()
        f = ts.frequency()
        self.assertAlmostEqual(f,1)
    
    def testMax(self):
        ts = self.getts()
        tsmax = ts.max()
        for v in ts.values():
            self.assertTrue(tsmax >= v)
    
    def testMin(self):
        ts = self.getts()
        tsmin = ts.min()
        for v in ts.values():
            self.assertTrue(tsmin <= v)
        
    def testDates(self):
        ts = self.getts()
        start = ts.start()
        end = ts.end()
        self.assertTrue(end > start)
        sts = ts.window(start,end)
        self.assertEqual(len(ts),len(sts))
        dates = ts.keys()
        
    def testMerge(self):
        ts = self.getts()
        ts2 = self.getts(delta = 2, cols = 2)
        ts3 = ts.merge(ts2)
        self.assertTrue(len(ts3)>0)
        self.assertEqual(ts3.count(),3)
        
    def testMultivariate(self):
        ts = self.getts(cols = 2)
        va = ts[0]
        self.assertEqual(len(va),2)
        #names = ts.colnames()
        #self.assertEqual(len(names),1)
        
    def testRollingMin(self):
        ts = self.getts(cols = 2)
        mts30 = ts.rollmin(window = 30)
        mts60 = ts.rollmin(window = 60)
        self.assertEqual(len(mts30),len(ts) - 29)
        self.assertEqual(len(mts60),len(ts) - 59)
        
    def testBinaryTreeWrapper(self):
        '''Test included in documentation'''
        ts = randomts(cols = 2, start = date(2010,1,1), size = 50)
        dts = ts.asbtree()
        self.assertEqual(dts.shape,ts.shape)
        values = ts.values()
        self.assertEqual(dts[ts.start()].all(),values[0].all())
        self.assertEqual(dts[ts.end()].all(),values[49].all())
        
    def testHashWrapper(self):
        ts = randomts(cols = 2, start = date(2010,1,1), size = 50)
        dts = ts.ashash()
        self.assertEqual(dts.shape,ts.shape)
        self.assertFalse(dts.modified)
        dts[date(2009,2,1)] = [56.4,78.6]
        self.assertTrue(dts.modified)
        self.assertEqual(len(dts),len(ts)+1)
        dts = dts.getts()
        self.assertEqual(ts.type,dts.type)
        self.assertEqual(len(dts),len(ts)+1)
        self.assertEqual(dts.count(),ts.count())
        self.assertTrue(dts.isconsistent())
        
    def testCSVformatter(self):
        ts = randomts(name = "serie1,serie2",
                      cols = 2, start = date(2010,1,1), size = 50)
        self.assertEqual(ts.names(),['serie1','serie2'])
        csv = ts.dump('csv')
        self.assertTrue(csv)
        
    def testXLSformatter(self):
        ts = randomts(name = "serie1,serie2",
                      cols = 2, start = date(2010,1,1), size = 50)
        try:
            import xlwt
        except ImportError:
            try:
                csv = ts.dump('xls')
            except FormattingException:
                pass
        else:
            xls = ts.dump('xls')
            self.assertTrue(xls)
            
    def testPlot(self):
        ts = randomts(name = "serie1,serie2",
                      cols = 2, start = date(2010,1,1), size = 50)
        try:
            import matpotlib
        except ImportError:
            try:
                csv = ts.dump('plot')
            except FormattingException:
                pass
        else:
            plot = ts.dump('plot')
            self.assertTrue(plot)
        