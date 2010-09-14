import unittest
from itertools import izip

from dynts import timeseries
from dynts.utils.populate import populate, datepopulate, randomts, date


class TestTS(unittest.TestCase):
    backend = None
    
    def getdata(self, size = 100, cols = 1, delta = 1, start = None):
        dates = datepopulate(size = size, delta = delta)
        data = populate(size = size, cols = cols)
        return dates,data
        
    def getts(self, returndata = False, delta = 1, cols = 1):
        dates,data = self.getdata(100,cols,delta)
        ts   = timeseries(name = 'test', date = dates, data = data, backend = self.backend)
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
            
        self.assertTrue(ts.isregular())
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
        ts2 = self.getts(delta = 2)
        ts3 = ts.merge(ts2)
        self.assertTrue(len(ts3)>0)
        
    def testMultivariate(self):
        ts = self.getts(cols = 2)
        va = ts[0]
        self.assertEqual(len(va),2)
        #names = ts.colnames()
        #self.assertEqual(len(names),1)
        
    def testDictionary(self):
        '''Test included in documentation'''
        ts = randomts(cols = 2, start = date(2010,1,1), size = 50)
        dts = ts.asdict()
        values = ts.values()
        self.assertEqual(dts[ts.start()].all(),values[0].all())
        self.assertEqual(dts[ts.end()].all(),values[49].all())
        
    def testCSVformatter(self):
        ts = randomts(name = "serie1,serie2",
                      cols = 2, start = date(2010,1,1), size = 50)
        self.assertEqual(ts.names(),['serie1','serie2'])
        csv = ts.dump('csv')
        self.assertTrue(csv)
        