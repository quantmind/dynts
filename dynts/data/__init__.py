from datetime import date, timedelta

from dynts.conf import settings
from dynts.exceptions import *

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
    '''Cordinates the loading of timeseries data into :class:`dynts.dsl.Symbol`.
This class can be replaced by a custom one if required.'''
    def load(self, providers, symbols, start, end, provider = None):
        '''Load symbols data.
        
* *providers* Dictionary of registered data providers.
* *symbols* list of symbols to load
* *start* start date
* *end* end date'''
        start, end = self.dates(start, end)
        data = {}
        for symbol in symbols:
            ticker, field, provider = self.parse_symbol(symbol)
            p  = providers.get(provider,None)
            if not p:
                raise MissingDataProvider('data provider %s not available' % provider)
            result = p.get(ticker, start, end, field)
            self.onresult(symbol,result)
            data[symbol] = result
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
    
    def parse_symbol(self, symbol):
        '''Parse a symbol to obtain information regarding ticker, field and provider.
Must return a tuple containing::

    (ticker,fied,provider)
'''
        symbol = str(symbol)
        bits = symbol.split(':')
        pnames = providers.keys()
        provider = settings.default_provider
        if len(bits) == 1:
            return symbol,None,provider
        elif len(bits) == 2:
            if bits[1] in pnames:
                return bits[0],None,bits[1]
            else:
                return bits[0],bits[1],provider
        elif len(bits) == 3:
            if bits[1] in pnames:
                return bits[0],bits[2],bits[1]
            elif bits[2] in pnames:
                return bits[0],bits[1],bits[2]
            else:
                raise BadSymbol('Could not parse %s. Unrecognized provider.' % symbol)
        else:
            raise BadSymbol('Could not parse %s.' % symbol)

    def onresult(self, symbol, result):
        '''Post-processing hook for result obtained from a data-provider.
By default do nothing.'''
        pass
        

class DataProviders(dict):
    proxies = {}
        
    def load(self, symbols, start = None, end = None, loader = None):
        loader = loader or settings.default_loader or TimeSerieLoader
        if isinstance(loader,type):
            loader = loader()
        return loader.load(self,symbols,start,end)
    
    def register(self, provider):
        '''Register a new data provider. *provider* must be an instance of
    DataProvider. If provider name is already available, it will be replaced.'''
        if isinstance(provider,type):
            provider = provider()
        self[provider.code] = provider
        
    def unregister(self, provider):
        '''Unregister an existing data provider. *provider* must be an instance of
    DataProvider. If provider name is already available, it will be replaced.'''
        if isinstance(provider,type):
            provider = provider()
        if isinstance(provider,DataProvider):
            provider = provider.code
        return self.pop(str(provider).upper(),None)
        

providers = DataProviders()
register = providers.register
unregister = providers.unregister

register(google)
register(yahoo)

