import unittest
from itertools import izip

import dynts
from dynts import dsl

class TestDsl(unittest.TestCase):
    names = ['eur','1eur','eu3r','eur4567']
    
    def testName(self):
        for name in self.names:
            res = dynts.parse(name)
            self.assertTrue(isinstance(res,dsl.Symbol))
            self.assertEqual(name.upper(),str(res))
        
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
        
    def testTwoTimeSeries(self):
        '''Get a timeseries and a function and check for consistency'''
        res = dynts.parse('gs:yahoo,min(gs:yahoo,window=30)')
        self.assertEqual(res.symbols(),['GS:YAHOO'])
        self.assertEqual(len(res),2)
        self.assertEqual(str(res[0]),'GS:YAHOO')
        self.assertEqual(str(res[1]),'min(GS:YAHOO,window=30)')
        
    def testBinOpSerieFunction(self):
        '''Get a timeseries and a function and check for consistency'''
        res = dynts.parse('goog:yahoo-ma(goog:yahoo,window=30)')
        self.assertEqual(res.symbols(),['GOOG:YAHOO'])
        self.assertEqual(len(res),2)
        self.assertEqual(str(res[0]),'GOOG:YAHOO')
        self.assertEqual(str(res[1]),'ma(GOOG:YAHOO,window=30)')
        result = dynts.evaluate(res)
        self.assertEqual(len(result.data),1)
        data = result.ts()
        self.assertTrue(dynts.istimeseries(data))
        self.assertEqual(data.count(),1)
        
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
        
    def testTSName(self):
        '''
        The dslresult should include an attribute 'name' 
        which is the equivalent to the expression passed.
        In situations where multiple timeseries are returned 
        the name should be the concatenation of all the names 
        joined by "__".
        '''
        expressions = ['GOOG+YHOO',
                       '2*GOOG',
                       'GOOG,YHOO',
                       ]
        for expr in expressions:
            result = dynts.evaluate(expr)
            ts = result.ts()
            name = ts.name
            
            expected_name = '__'.join(expr.split(','))
            self.assertEqual(name, expected_name)
            
        

        
