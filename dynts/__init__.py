'''Quantitative financial timeseries analysis'''

VERSION = (0, 2)
 
def get_version():
    if len(VERSION) == 3:
            v = '%s.%s.%s' % VERSION
    else:
        v = '%s.%s' % VERSION[:2]
    return v
 
__version__  = get_version()
__license__  = "BSD"
__author__   = "Luca Sbardella"
__contact__  = "luca@quantmind.com"
__homepage__ = "http://github.com/quantmind/dynts/"


from dynts.exceptions import *
from backends import timeseries, TimeSeries, istimeseries, Formatters, BACKENDS
from dsl import parse, dslresult, function_registry, functions
from data import providers
import formatters
Formatters['json'] = formatters.toflot
Formatters['csv'] = formatters.tocsv
Formatters['xls'] = formatters.toxls
Formatters['plot'] = formatters.toplot


def evaluate(expression, start = None, end = None, loader = None):
    '''Evaluate expression *e*. This and :func:`dynts.parse`
represent the main entry point of the library.
    
* *expression* string or an instance of :class:`dynts.dsl.Expr` obtained using
  the :func:`dynts.parse` function.
* *start* start date or ``None``.
* *end* end date or ``None``.
* *loader* Optional :class:`dynts.data.TimeSerieLoader` class or instance.

*expression* is parsed and the :class:`dynts.expr.Symbol` are sent to the
:class:`dynts.data.TimeSerieLoader` instance for retrieving actual timeseries data.
It returns an instance of :class:`dynts.dslresult`.

Typical usage::

    >>> import dynts
    >>> r = dynts.evaluate('min(GS,window=30)')
    >>> r
    min(GS,window=30)
    >>> ts = r.unwind()
    '''
    if isinstance(expression,basestring):
        expression = parse(expression)
    symbols = expression.symbols()
    data = providers.load(symbols, start, end, loader = loader)
    return dslresult(expression,data)
    


################### For testings
#    
def add2path():
    import os
    import sys
    path = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
    if path not in sys.path:
        sys.path.insert(0,path)
        
def runtests():
    import unittest
    add2path()
    from dynts import tests
    loader = unittest.TestLoader()
    suite  = loader.loadTestsFromModule(tests)
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
def runbench():
    add2path()
    from dynts.bench import runbench
    runbench()