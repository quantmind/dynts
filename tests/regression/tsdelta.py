#
# NOT USED DIRECTLY
# TEMPLATE TEST CASE FOR Difference Operators
#
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
        
    def testLaggedDelta(self):
        '''Test mean function with zero parameters'''
        ts = self.getts(2)
        d = ts.delta(lag = 5)
        self.assertEqual(len(d),len(ts)-5)
        self.assertEqual(d.count(),ts.count())
        