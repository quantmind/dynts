import logging
from datetime import date, timedelta

from dynts.conf import settings
from dynts.exceptions import *

from ccy import todate

from gy import DataProvider, google, yahoo


class Silence(logging.Handler):
    def emit(self, record):
        pass

class MissingDataProvider(Exception):
    '''Data provider is not available'''
    pass


def safetodate(dte):
    try:
        return todate(end)
    except:
        return None


class PreProcessData(object):
    '''data preprocess holder'''
    def __init__(self, intervals = None, result = None):
        self.intervals = intervals
        self.result    = result
        

class TimeSerieLoader(object):
    '''Cordinates the loading of timeseries data into :class:`dynts.dsl.Symbol`.
This class can be overritten by a custom one if required. There are three **hooks**
which can be used to customized its behaviour:

* :func:`dynts.data.TimeSerieLoader.preprocess`
* :func:`dynts.data.TimeSerieLoader.onresult`
* :func:`dynts.data.TimeSerieLoader.onfinishload`

.. attribute:: separator
    
    character for separating ticker, field and vendor. Default ``:``'''

    separator = ':'
    preprocessdata = PreProcessData
    '''Class holding data returned by the :meth:`dynts.data.TimeSerieLoader.preprocess` method.
    It contains two attributes:
    
    * ``intervals`` ``None`` or a tuple of two-elements tuples.
    * ``result`` ``None`` or any intermediate result.
    
    If ``intervals`` is ``None`` or an empty container, the
    :func:`dynts.data.DataProvider.load` method won't be called, and the ``result``
    attribute will be passed to the :meth:`dynts.data.TimeSerieLoader.onresult` method.
    '''
    
    def load(self, providers, symbols, start, end, logger):
        '''Load symbols data.
        
* *providers* Dictionary of registered data providers.
* *symbols* list of symbols to load
* *start* start date
* *end* end date.
* *logger* instance of :class:`logging.Logger`.

There is no need to override this function, just use one the three hooks
available.
'''
        # Preconditioning on dates
        start, end = self.dates(start, end)
        data = {}
        for symbol in symbols:
            # Get ticker, field and provider
            ticker, field, provider = self.parse_symbol(symbol)
            p  = providers.get(provider,None)
            if not p:
                raise MissingDataProvider('data provider %s not available' % provider)
            pre = self.preprocess(ticker, start, end, field, p, logger)
            if pre.intervals:
                result = None
                for st,en in pre.intervals:
                    logger.debug('Loading %s from %s. From %s to %s' % (ticker,provider,st,en))
                    res = p.load(ticker, st, en, field, logger)
                    if result is None:
                        result = res
                    else:
                        result.update(res)
            else:
                result = pre.result
            # onresult hook
            result = self.onresult(ticker, field, p, result, logger)
            data[symbol] = result
        # last hook
        return self.onfinishload(data, logger)
    
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
    
    def getsymbol(self, ticker, field, provider):
        '''Convert *ticker*, *field* and *provider* to symbol code.
The inverse of :meth:`dynts.data.TimeSerieLoader.parse_symbol`.'''
        c = self.separator
        f = '' if not field else '%s%s' % (c,field)
        d = provider == self.default_provider_for_ticker(ticker, field)
        p = '' if d else '%s%s' % (c,provider)
        return '%s%s%s' % (ticker,f,p)
    
    def preprocess(self, ticker, start, end, field, provider, logger):
        '''Preprocess **hook**. This is first loading hook and it is
**called before requesting data** from a dataprovider.
It must return an instance of :attr:`TimeSerieLoader.preprocessdata`.
By default it returns::

    self.preprocessdata(intervals = ((start,end),))
    
It could be overritten to modify the intervals. If the intervals is ``None`` or 
an empty container, the :func:`dynts.data.DataProvider.load` method won't be called,
otherwise it will be called as many times as the number of intervals in the return tuple
(by default once).
'''
        return self.preprocessdata(intervals = ((start, end),))
    
    def onresult(self, ticker, field, provider, result, logger):
        '''Post-processing **hook** for results returned by
calls to :func:`dynts.data.DataProvider.load`, or obtained
from the :meth:`dynts.data.TimeSerieLoader.preprocess` method.
By default return ``result``::
    
    return result
    
It could be used to store data into a cache or database.'''
        return result
    
    def onfinishload(self, data, logger):
        '''Another post-processing **hook** invoked when the loading is finished.
By default retun *data*.'''
        return data


class DataProviders(dict):
    proxies = {}
        
    def load(self, symbols, start = None, end = None, loader = None, logger = None):
        loader = loader or settings.default_loader or TimeSerieLoader
        logger = self.get_logger(logger)
        if isinstance(loader,type):
            loader = loader()
        return loader.load(self,symbols,start,end,logger)
    
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
        
    def get_logger(self, logger):
        if logger:
            return logger
        logger = logging.getLogger('dynts.data')
        if not logger.handlers:
            logger.addHandler(Silence())
        return logger

providers = DataProviders()
register = providers.register
unregister = providers.unregister

register(google)
register(yahoo)

