from datetime import date, timedelta

from dynts.conf import settings

from ccy import todate

from gy import DataProvider, google, yahoo


class MissingDataProvider(Exception):
    '''Data provider is not available'''
    pass


def safetodate(dte):
    try:
        return todate(end)
    except:
        return None


class TimeSerieLoader(object):
    '''Load timeseries. This class can be replaced by a custom one.'''
    
    def load(self, providers, symbols, start, end, provider = None):
        '''Load symbols data.
        
* *providers* Dictionary of registered data providers.
* *symbols* list of symbols to load
* *start* start date
* *end* end date'''
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
    
    def dates(self, start, end):
        '''Preconditioning on dates. This function makes sure the *start*
and *end* date are consistent. It never fails and always return a two-element tuple
containing *start*,*end* with *start* less or equal *end*
and *end* never after today.
There should be no reason to override this function.'''
        td    = date.today()
        end   = safetodate(end) or td
        end   = end if end <= td else td
        start = safetodate(start)
        if not start or start > end:
            start = end - timedelta(days=int(round(30.4*settings.months_history)))
        return start,end
    
    def parse_symbol(self, symbol, provider =None):
        provider = provider or settings.default_provider
        return str(symbol), None, provider


class DataProviders(dict):
    proxies = {}
        
    def load(self, symbols, start = None, end = None, provider = None, loader = None):
        loader = loader or TimeSerieLoader()
        if isinstance(loader,type):
            loader = loader()
        return loader.load(self,symbols,start,end, provider = provider)
    
    def register(self, provider):
        '''Register a new data provider. *provider* must be an instance of
    DataProvider. If provider name is already available, it will be replaced.'''
        name = provider.code.lower()
        self[name] = provider
        

dynts_providers = DataProviders()

dynts_providers.register(google())
dynts_providers.register(yahoo())
