import unittest

import dynts

class TestFlot(unittest.TestCase):
    
    def testFlot1(self):
        ts = dynts.evaluate('YHOO,GOOG').unwind('flot')
        dts = ts.todict()