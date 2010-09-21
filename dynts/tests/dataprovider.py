import unittest

import dynts
from dynts.data import DataProvider, providers, register, unregister


class CustomProvider(DataProvider):
    pass

class TestDataProvider(unittest.TestCase):
    
    def testyahoo(self):
        ts = dynts.evaluate('GOOG:yahoo')
        self.assertTrue(ts)
        
    def testregistration(self):
        register(CustomProvider)
        self.assertEqual(len(providers),3)
        p = providers['customprovider']
        self.assertTrue(isinstance(p,CustomProvider))
        unregister('customprovider')
        self.assertEqual(len(providers),2)
        p = providers.get('customprovider',None)
        self.assertEqual(p,None)