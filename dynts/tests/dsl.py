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
        data = result.unwind()
        self.assertEqual(len(data),2)
        ts1 = data[0]
        ts2 = data[1]
        for v1,v2 in izip(ts1.values(),ts2.values()):
            self.assertAlmostEqual(v1,2.*v2)
        

        
