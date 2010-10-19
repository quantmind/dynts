#
# NOT USED DIRECTLY - THIS CLASS IS IMPORTED IN dynts.tests.timeseries
#
from dynts.test import TestCase
from datetime import date
from itertools import izip

from dynts.utils import cross, asarray
from dynts.exceptions import *


class TestTS(TestCase):
            
    def _rollingTest(self, func):
        ts = self.getts(cols = 2)
        rollfun = 'roll%s' % func
        mts30 = getattr(ts,rollfun)(window = 30)
        mts60 = getattr(ts,rollfun)(window = 60)
        self.assertEqual(len(mts30),len(ts) - 29)
        self.assertEqual(len(mts60),len(ts) - 59)
        self.assertEqual(mts30.count(),2)
        self.assertEqual(mts60.count(),2)
        values = ts.values()
        v30 = mts30.values()
        date   = asarray(ts.dates())
        c = 0
        for dt,v in mts30.items():
            tst = ts.clone(date[c:c+30],values[c:c+30])
            self.assertEqual(dt,tst.end())
            tv = getattr(tst,func)()
            c += 1
            for a,b in izip(v,tv):
                self.assertAlmostEqual(a,b)
    
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
        ts  = self.getts()
        val = cross(ts.max())
        for v in ts.values():
            self.assertTrue(val >= v)
        ts = self.getts(cols = 2)
        val = cross(ts.max())
        for v in ts.values():
            self.assertTrue(val >= v)
    
    def testMin(self):
        ts  = self.getts()
        val = cross(ts.min())
        for v in ts.values():
            self.assertTrue(val <= v)
        ts = self.getts(cols = 2)
        val = cross(ts.min())
        for v in ts.values():
            self.assertTrue(val <= v)
        
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
        self._rollingTest('min')
        
    def testRollingMax(self):
        self._rollingTest('max')
            
    def testBinaryTreeWrapper(self):
        '''Test included in documentation'''
        ts = self.randomts(cols = 2, start = date(2010,1,1), size = 50)
        dts = ts.asbtree()
        self.assertEqual(dts.shape,ts.shape)
        values = ts.values()
        self.assertEqual(dts[ts.start()].all(),values[0].all())
        self.assertEqual(dts[ts.end()].all(),values[49].all())
        
    def testHashWrapper(self):
        ts = self.randomts(cols = 2, start = date(2010,1,1), size = 50)
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
        ts = self.randomts(name = self.tsname("serie1","serie2"),
                           cols = 2, start = date(2010,1,1), size = 50)
        self.assertEqual(ts.names(),['serie1','serie2'])
        csv = ts.dump('csv')
        self.assertTrue(csv)
        
    def testXLSformatter(self):
        ts = self.randomts(name = "serie1,serie2",
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
        ts = self.randomts(name = "serie1,serie2",
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
        
    def testDslNames(self):
        res = self.evaluate('amzn:yahoo,min(amzn:yahoo)', backend = self.backend)
        self.assertEqual(str(res.expression),'AMZN:YAHOO,min(AMZN:YAHOO)')
        self.assertEqual(len(res.data),1)
        ts = res.ts()
        self.assertEqual(ts.count(),2)
        self.assertEqual(ts.names(),['AMZN:YAHOO','min(AMZN:YAHOO,window=20)'])
        