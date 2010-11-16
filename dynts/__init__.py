'''Quantitative financial timeseries analysis'''

VERSION = (0, 3, 3)
 
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
from backends import timeseries, xydata, TimeSeries, DynData, tsfunctions
from backends import istimeseries, Formatters, BACKENDS, ts_bin_op
from dsl import parse, merge, dslresult, function_registry, functions
from data import providers
import formatters
Formatters['flot'] = formatters.ToFlot()
Formatters['jsonvba'] = formatters.ToJsonVba()
Formatters['csv']  = formatters.ToCsv()
Formatters['xls']  = formatters.ToXls()
Formatters['plot'] = formatters.ToPlot()


def evaluate(expression, start = None, end = None,
             loader = None, logger = None, backend = None, **kwargs):
    '''Evaluate expression *e*. This and :func:`dynts.parse`
represent the main entry point of the library.
    
* *expression* string or an instance of :class:`dynts.dsl.Expr` obtained using
  the :func:`dynts.parse` function.
* *start* start date or ``None``.
* *end* end date or ``None``.
* *loader* Optional :class:`dynts.data.TimeSerieLoader` class or instance.
* *logger* Python logging class or ``None``. Used if you required logging.
* *backend* :class:`dynts.TimeSeries` backend name or ``None``.

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
    data = providers.load(symbols, start, end, loader = loader,
                          logger = logger, backend = backend, **kwargs)
    return dslresult(expression, data, backend = backend)


def tsname(*names):
    from dynts.conf import settings
    return reduce(lambda x,y: '%s%s%s' % (x,settings.splittingnames,y), names)


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