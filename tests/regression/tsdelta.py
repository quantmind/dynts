#
# NOT USED DIRECTLY
# TEMPLATE TEST CASE FOR Difference Operators
#
try:
    from itertools import izip as zip
except ImportError:
    pass
from dynts import test
from dynts.utils.populate import randomts, polygen


class TestCase(test.TestCase):
    
    def getts(self, cols, *coefs):
        return randomts(100, cols, backend = self.backend, generator = polygen(*coefs))
    
    def testp0Delta(self):
        '''Test mean function with zero parameters'''
        ts = self.getts(2, 5.)
        d = ts.delta()
        self.assertEqual(len(d),len(ts)-1)
        self.assertEqual(d.count(),ts.count())
        for vs in d.values():
            for v in vs:
                self.assertAlmostEqual(v,0.)
                
    def testp1Delta(self):
        '''Test mean function with zero parameters'''
        ts = self.getts(2, 5., -2.)
        d = ts.delta()
        self.assertEqual(len(d),len(ts)-1)
        self.assertEqual(d.count(),ts.count())
        for vs in d.values():
            for v in vs:
                self.assertAlmostEqual(v,-2.)
                
    def testp1DeltaLag(self):
        '''Test delta with a quadratic polinomial'''
        lag = 5
        ts = self.getts(2, 5., 3.5)
        d = ts.delta(lag = lag)
        self.assertEqual(len(d),len(ts)-5)
        self.assertEqual(d.count(),ts.count())
        
        dv = 3.5 * lag
        for vs in d.values():
            for v in vs:
                self.assertAlmostEqual(v,dv)
    
    def testDelta2(self):
        ts = self.getts(2, 5., 3.5, 0.2)
        d = ts.delta2()
        self.assertEqual(len(d),len(ts)-2)
        self.assertEqual(d.count(),ts.count())
        for vs in d.values():
            for v in vs:
                self.assertAlmostEqual(v,0.4)
        
    def testDelta2Lag(self):
        lag = 5
        ts = self.getts(2, 5., 3.5, 0.2)
        d = ts.delta2(lag = lag)
        self.assertEqual(len(d),len(ts)-2*lag)
        self.assertEqual(d.count(),ts.count())
        dv = 0.4 * lag * lag
        for vs in d.values():
            for v in vs:
                self.assertAlmostEqual(v,dv)
                
    def testComplexDelta(self):
        '''Test for a lagged Delta2 against a double Delta'''
        lag = 5
        ts = self.getts(2, 5., 3.5, 0.2)
        d = ts.delta2(lag = lag)
        dd = ts.delta(lag = lag).delta(lag = lag)
        self.assertEqual(len(d),len(dd))
        self.assertEqual(d.count(),dd.count())
        for dv,ddv in zip(d.values(),dd.values()):
            for v,vv in zip(dv,ddv):
                self.assertAlmostEqual(v,vv)
        