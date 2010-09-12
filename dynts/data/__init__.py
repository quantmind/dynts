from datetime import date, timedelta

from dynts.conf import settings

from gy import DataProvider, google, yahoo


class MissingDataProvider(Exception):
    '''Data provider is not available'''
    pass


class TimeSerieLoader(object):
    '''Load timeseries. This class can be replaced by a custom one.'''
    
    def dates(self, start, end):
        end   = end or date.today()
        start = start
        if not start:
            start = end - timedelta(days=int(round(30.4*settings.months_history)))
        return start,end
            
    def parse_symbol(self, symbol, provider =None):
        provider = provider or settings.default_provider
        return str(symbol), None, provider
        
    def __call__(self, providers, symbols, start, end, provider = None):
        '''Load data symbols'''
        start, end = self.dates(start, end)
        data = {}
        for symbol in symbols:
            ticker, field, provider = self.parse_symbol(symbol, provider = provider)
            p  = providers.get(provider,None)
            if not p:
                raise MissingDataProvider('data provider %s not available' % provider)
            ts = p.get(ticker, start, end, field) 
            data[symbol] = ts
        return data


class DataProviders(dict):
    loader = TimeSerieLoader()
    proxies = {}
        
    def load(self, symbols, start = None, end = None, provider = None):
        return self.loader(self,symbols,start,end, provider = provider)
    
    def register(self, provider):
        '''Register a new data provider. *provider* must be an instance of
    DataProvider. If provider name is already available, it will be replaced.'''
        name = provider.code.lower()
        self[name] = provider
        

dynts_providers = DataProviders()

dynts_providers.register(google())
dynts_providers.register(yahoo())
