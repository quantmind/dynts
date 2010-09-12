import unittest

import dynts

class TestDsl(unittest.TestCase):
    
    def testBinaryOperation(self):
        res = dynts.parse('2*GOOG')
        self.assertEqual(len(res.children),2)
        names = res.symbols()
        self.assertEqual(len(names),1)
        self.assertEqual(names[0],res.right)
        #ts = dynts.evaluate(res)
        #self.assertEqual(ts.count(),1)
        
    def testFunction(self):
        '''Test a function with one argument'''
        pass