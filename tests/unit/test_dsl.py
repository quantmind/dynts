from dynts.utils import test
from dynts import api
from dynts.dsl import ast


class TestDsl(test.TestCase):
    names = ['eur', '1eur', 'eu3r', 'eur4567']

    def testName(self):
        for name in self.names:
            res = api.parse(name)
            self.assertTrue(isinstance(res, ast.Symbol))
            self.assertEqual(name.upper(), str(res))

    def testBinaryOperation(self):
        res = api.parse('2*GOOG')
        self.assertEqual(len(res.children), 2)
        names = res.symbols()
        self.assertEqual(len(names), 1)
        self.assertEqual(names[0], str(res.right))

    def testOperationOrder(self):
        res = api.parse('2*GOOG+4*YHOO')
        self.assertEqual(len(res.children), 2)
        self.assertTrue(isinstance(res, ast.PlusOp))
        res1 = res.children[0]
        self.assertTrue(isinstance(res1, ast.MultiplyOp))
        res2 = res.children[1]
        self.assertTrue(isinstance(res2, ast.MultiplyOp))

    def testAdditionOperation(self):
        res = api.parse('YHOO+GOOG')
        self.assertEqual(len(res.children), 2)
        names = res.symbols()
        self.assertEqual(len(names), 2)
        self.assertEqual(names[0], str(res.left))
        self.assertEqual(names[1], str(res.right))

    def testQuote(self):
        res = api.parse('"FX-15"+amzn')
        self.assertEqual(len(res.children), 2)
        names = res.symbols()
        self.assertEqual(len(names), 1)
        self.assertEqual(names[0], str(res.right))

    def testSpecialSymbol(self):
        '''Symbol can be included by character'''
        res = api.parse('`FX-15`+amzn')
        self.assertEqual(len(res.children), 2)
        names = res.symbols()
        self.assertEqual(len(names), 2)
        self.assertEqual(names[0], 'FX-15')
        self.assertEqual(names[1], 'AMZN')

    def testSpecialSymbol2(self):
        '''Symbol can be included by character'''
        res = api.parse('`EURSW6M2YR_2.2`')
        names = res.symbols()
        self.assertEqual(len(names), 1)
        self.assertEqual(str(res), '`EURSW6M2YR_2.2`')
        self.assertEqual(names[0], 'EURSW6M2YR_2.2')

    def testSpecialSymbol3(self):
        '''Symbol can be included by character'''
        res = api.parse('`EURSW6M2YR_2.2:RM@all`')
        names = res.symbols()
        self.assertEqual(len(names), 1)
        self.assertEqual(names[0], 'EURSW6M2YR_2.2:RM@ALL')

    def testSyntaxError(self):
        '''Symbol can be included by character'''
        res = api.parse('delta(goog')
        self.assertTrue(res.malformed())

    def testSyntaxError2(self):
        '''Symbol can be included by character'''
        res = api.parse('yahoo, delta(goog')
        self.assertTrue(res.malformed())

    def testTwoTimeSeries(self):
        '''Get a timeseries and a function and check for consistency'''
        res = api.parse('gs:yahoo, min(gs:yahoo, window=30)')
        self.assertEqual(res.symbols(), ['GS:YAHOO'])
        self.assertEqual(len(res), 2)
        self.assertEqual(str(res[0]), 'GS:YAHOO')
        self.assertEqual(str(res[1]), 'min(GS:YAHOO, window=30)')

    def testBinOpSerieFunction(self):
        '''Get a timeseries and a function and check for consistency'''
        res = api.parse('goog:yahoo-ma(goog:yahoo, window=30)')
        self.assertEqual(res.symbols(), ['GOOG:YAHOO'])
        self.assertEqual(len(res), 2)
        self.assertEqual(str(res[0]), 'GOOG:YAHOO')
        self.assertEqual(str(res[1]), 'ma(GOOG:YAHOO, window=30)')
        result = api.evaluate(res)
        self.assertEqual(len(result.data), 1)
        data = result.ts()
        self.assertTrue(api.is_timeseries(data))
        self.assertEqual(data.count(), 1)

    def testDataProvider(self):
        result = api.evaluate('2*GOOG, GOOG')
        self.assertEqual(len(result.data), 1)
        self.assertEqual(result.expression, api.parse('2*GOOG, GOOG'))
        data = result.ts()
        self.assertTrue(api.is_timeseries(data))
        self.assertEqual(data.count(), 2)
        ts1 = data.serie(0)
        ts2 = data.serie(1)
        for v1, v2 in zip(ts1, ts2):
            self.assertAlmostEqual(v1, 2.*v2)

    def testQuotedLinearSuperimposition(self):
        res = api.parse("4*`eur:rm@bla`-8*`abc:56`+4*`a-b-c:-20`")
        self.assertEqual(len(res), 2)

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
                       'GOOG, YHOO',
                       ]
        for expr in expressions:
            result = api.evaluate(expr)
            ts = result.ts()
            name = ts.name

            expected_name = '__'.join(expr.split(','))
            self.assertEqual(name, expected_name)

    def testTimesMinus(self):
        result = api.parse('EUR*-3')
        self.assertEqual(result.symbols(), ['EUR'])
        self.assertEqual(len(result), 2)
        self.assertEqual(str(result[0]), 'EUR')
        self.assertEqual(str(result[1]), '-3')
