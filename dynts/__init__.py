import os
import sys
 
VERSION = (0, 1, 'alpha')
 
def get_version():
    if len(VERSION) == 3:
        try:
            int(VERSION[2])
            v  = '%s.%s.%s' % VERSION
        except:
            v = '%s.%s_%s' % VERSION
    else:
        v = '%s.%s' % VERSION[:2]
    return v
 
__version__ = get_version()


from backends import timeserie, BACKENDS
from data import providers, TimeSerieLoader
from dsl import parse


def get(symbols, start = None, end = None, provider = None):
    if not hasattr(symbols,'__iter__'):
        symbols = [symbols]
    res = providers.load(symbols, start, end, provider = provider)
    return res

def evaluate(e, start = None, end = None, variables = None):
    '''Evaluate expression *e*.
     * *e* instance of :ref:`Expr <expr>' obtained using the parse function.
     * *start* start date
     * *end* end date
     * *variables* dictionary of variables to replace strings
    '''
    variables = variables or {}
    symbols = e.symbols()
    data = providers.load(symbols, start, end)
    