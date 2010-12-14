'''Quantitative financial timeseries analysis'''

VERSION = (0, 3, 4)
 
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
CLASSIFIERS  = [
                'Development Status :: 4 - Beta',
                'Environment :: Plugins',
                'Intended Audience :: Developers',
                'Intended Audience :: Financial and Insurance Industry',
                'Intended Audience :: Science/Research',
                'License :: OSI Approved :: BSD License',
                'Operating System :: OS Independent',
                'Programming Language :: Python',
                'Programming Language :: JavaScript',
                'Topic :: Scientific/Engineering',
                'Topic :: Scientific/Engineering :: Mathematics',
                'Topic :: Office/Business :: Financial'
                ]


from dynts.exceptions import *
from backends import timeseries, xydata, TimeSeries, DynData, tsfunctions
from backends import istimeseries, Formatters, BACKENDS, ts_bin_op
from dsl import parse, merge, dslresult, function_registry, functions
from maths import BasicStatistics, pivottable
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


def statistics(expression,
               start = None,
               end = None,
               functions = None,
               multivariate = False, **kwargs):
    tseries = evaluate(expression, start = start, end = end, **kwargs).ts()
    if not multivariate:
        return BasicStatistics(tseries, functions = functions)
    else:
        raise NotImplementedError
    

def tsname(*names):
    from dynts.conf import settings
    return reduce(lambda x,y: '%s%s%s' % (x,settings.splittingnames,y), names)


def hasextensions():
    '''True if cython extensions are available'''
    from .lib import hasextensions
    return hasextensions


def functions_docs():
    names = sorted(function_registry.keys())
    docs = ''
    for name in names:
        func = function_registry[name]
        docs += func.__doc__
    return docs


################### For testings
#    
def add2path():
    import os
    import sys
    path = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
    if path not in sys.path:
        sys.path.insert(0,path)
        
def runtests(tags = None, verbosity = 1):
    add2path()
    from dynts.tests.runtests import run
    run(tags = tags, verbosity = verbosity)
    
    
def runbench(tags = None, verbosity = 1):
    '''Run benchmark suite'''
    add2path()
    from dynts import test
    loader = test.BenchLoader()
    suite  = loader.loadBenchFromModules(['dynts.bench.*'])
    test.runbench(suite,tags,verbosity)