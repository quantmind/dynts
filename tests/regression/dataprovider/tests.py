
import dynts
from dynts.test import TestCase
from dynts.data import DataProvider, TimeSerieLoader
from dynts.data import providers, register, unregister


class CustomProvider(DataProvider):
    pass

class CustomLoader(TimeSerieLoader):
    data = {}
    
    def onresult(self, symbol, result, logger, backend, **kwargs):
        '''Store result in the class data dictionary'''
        ticker = self.getsymbol(symbol.ticker, symbol.field, symbol.provider.code)
        self.data[ticker] = result
        return result
        


class TestDataProvider(TestCase):
    
    def testyahoo(self):
        ts = dynts.evaluate('GOOG:yahoo')
        self.assertTrue(ts)
        
    def testProviderRegistration(self):
        register(CustomProvider)
        self.assertEqual(len(providers),3)
        p = providers['CUSTOMPROVIDER']
        self.assertTrue(isinstance(p,CustomProvider))
        unregister('CUSTOMPROVIDER')
        self.assertEqual(len(providers),2)
        p = providers.get('CUSTOMPROVIDER',None)
        self.assertEqual(p,None)
        
    def testCustomLoader(self):
        from dynts.conf import settings
        settings.default_loader = CustomLoader
        dynts.evaluate('BLT:google').unwind()
        data = CustomLoader.data
        self.assertTrue(data)
        self.assertTrue('BLT:GOOGLE' in data)
        
        
        