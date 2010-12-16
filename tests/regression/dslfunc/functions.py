#
# NOT USED DIRECTLY
#
import unittest
import dynts


class SimpleFunctionTest(unittest.TestCase):
    function = None
    
    def testNoParameters(self):
        '''Test mean function with zero parameters'''
        expression = '%s(GOOG)' % self.function
        result = dynts.evaluate(expression)
        self.assertEqual(str(result),expression)
        self.assertEqual(len(result.data),1)
        data = result.ts()
        self.assertTrue(dynts.istimeseries(data))
        self.assertEqual(data.count(),1)
        
    def testWindowParameter(self):
        '''Test mean function with one parameter'''
        e = '%(f)s(GOOG,window=30),%(f)s(GOOG,window=60)' % {'f':self.function}
        result = dynts.evaluate(e)
        symbols = result.expression.symbols()
        self.assertEqual(len(symbols),1)
        self.assertEqual(len(result.data),1)
        data = result.ts()
        self.assertTrue(dynts.istimeseries(data))
        self.assertEqual(data.count(),2)
        
    def testTwoSeries(self):
        e = '%s(GOOG,YHOO)' % self.function
        result = dynts.evaluate(e)
        symbols = result.expression.symbols()
        self.assertEqual(len(symbols),2)
        self.assertEqual(len(result.data),2)
        data = result.ts()
        self.assertTrue(dynts.istimeseries(data))
        self.assertEqual(data.count(),2)
        