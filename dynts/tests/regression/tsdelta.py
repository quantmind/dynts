#
# NOT USED DIRECTLY
# TEMPLATE TEST CASE FOR Difference Operators
#
from dynts import test
from dynts.utils.populate import randomts 


class TestCase(test.TestCase):
    
    def getts(self):
        return randomts(100,2, backend = self.backend)
    
    def testSimpleDelta(self):
        '''Test mean function with zero parameters'''
        ts = self.getts()
        d = ts.delta()
        self.assertEqual(len(d),len(ts)-1)
        self.assertEqual(d.count(),ts.count())
        
    def testLaggedDelta(self):
        '''Test mean function with zero parameters'''
        ts = self.getts()
        d = ts.delta(lag = 5)
        self.assertEqual(len(d),len(ts)-5)
        self.assertEqual(d.count(),ts.count())
        