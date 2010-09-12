import unittest

import dynts


class TestDataProvider(unittest.TestCase):
    
    def testyahoo(self):
        ts = dynts.get('GOOG', provider = 'yahoo')
        self.assertTrue(ts)