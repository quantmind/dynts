import unittest
from itertools import izip

import dynts

class TestDsl(unittest.TestCase):
    
    def testBinaryOperation(self):
        res = dynts.parse('2*GOOG')
        self.assertEqual(len(res.children),2)
        names = res.symbols()
        self.assertEqual(len(names),1)
        self.assertEqual(names[0],str(res.right))
        #ts = dynts.evaluate(res)
        #self.assertEqual(ts.count(),1)
    
    def testAdditionOperation(self):
        res = dynts.parse('YHOO+GOOG')
        self.assertEqual(len(res.children),2)
        names = res.symbols()
        self.assertEqual(len(names),2)
        self.assertEqual(names[0],str(res.left))
        self.assertEqual(names[1],str(res.right))
        
    def testDataProvider(self):
        result = dynts.evaluate('2*GOOG,GOOG')
        self.assertEqual(len(result.data),1)
        self.assertEqual(result.expression,dynts.parse('2*GOOG,GOOG'))
        data = result.ts()
        self.assertTrue(dynts.istimeseries(data))
        self.assertEqual(data.count(),2)
        ts1 = data.serie(0)
        ts2 = data.serie(1)
        for v1,v2 in izip(ts1,ts2):
            self.assertAlmostEqual(v1,2.*v2)
        

        
