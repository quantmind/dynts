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
This class can be overritten by a custom one if required. There are three **hooks**
which can be used to customized its behaviour:
:func:`dynts.data.TimeSerieLoader.preprocess`,
:func:`dynts.data.TimeSerieLoader.onresult` and
:func:`dynts.data.TimeSerieLoader.onfinishload`.

.. attribute:: separator
    
    character for separating ticker, field and vendor. Default ``:``'''

    separator = ':'
    
    def load(self, providers, symbols, start, end, provider = None):
        '''Load symbols data.
        
* *providers* Dictionary of registered data providers.
* *symbols* list of symbols to load
* *start* start date
* *end* end date.

There is no need to override this function, just use one the three hooks
available.'''
        start, end = self.dates(start, end)
        data = {}
        for symbol in symbols:
            # Get ticker, field and provider
            ticker, field, provider = self.parse_symbol(symbol)
            p  = providers.get(provider,None)
            if not p:
                raise MissingDataProvider('data provider %s not available' % provider)
            intervals = self.preprocess(ticker, start, end, field)
            if intervals:
                result = p.get(ticker, start, end, field)
            else:
                result = None
            result = self.onresult(symbol,result)
            data[symbol] = result
        return self.onfinishload(data)
    
    def dates(self, start, end):
        '''Pre-conditioning on dates. This function makes sure the *start*
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
    
For example::

    intc
    intc:open
    intc:volume:google
    intc:google
    
are all valid inputs returning::

    intc,None,yahoo
    intc,open,yahoo
    intc,volume,google
    intc,None,google
    
assuming ``yahoo`` is the provider in :attr:`dynts.conf.Settings.default_provider`.

This function is called before retrieving data. As with previous functions there should be no reason to
override this method. One could use the
:func:`dynts.data.TimeSerieLoader.default_provider_for_ticker` to twick
the behaviour when the provider is not available.
'''
        if not symbol:
            raise BadSymbol("symbol not provided")
        symbol = str(symbol)
        bits = symbol.split(self.separator)
        pnames = providers.keys()
        ticker = symbol
        provider = None
        field = None
        if len(bits) == 2:
            ticker = bits[0]
            if bits[1] in pnames:
                provider = bits[1]
            else:
                field = bits[1]
        elif len(bits) == 3:
            ticker = bits[0]
            if bits[1] in pnames:
                provider = bits[1]
                field = bits[2]
            elif bits[2] in pnames:
                provider = bits[2]
                field = bits[1]
            else:
                raise BadSymbol('Could not parse %s. Unrecognized provider.' % symbol)
        elif len(bits) > 3:
            raise BadSymbol('Could not parse %s.' % symbol)
        
        if provider is None:
            provider = self.default_provider_for_ticker(ticker, field)
        return ticker,field,provider
 
    def default_provider_for_ticker(self, ticker, field):
        '''Calculate the provider when not available in the symbol. By default it returns
:attr:`dynts.conf.Settings.default_provider`.'''
        return settings.default_provider
    
    def preprocess(self, ticker, start, end, field):
        '''Preprocess **hook**. This is **called before requesting data** to
a dataprovider. Return a tuple of date intervals. By default return::

    ([start,end],)
    
It could be overritten to modify the intervals. If the return is ``None`` or 
an empty container, the :func:`dynts.data.DataProvider.get` method won't be called,
otherwise it will be called as many times as the number of intervals in the return tuple
(by default once).
'''
        return [start, end],
    
    def onresult(self, symbol, result):
        '''Post-processing **hook** for result obtained from a data-provider.
By default return result. It could be used to store data into a cache or database.'''
        return result
    
    def onfinishload(self, data):
        '''Another post-processing **hook** invoked when the loading is finished.
By default retun *data*.'''
        return data


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

