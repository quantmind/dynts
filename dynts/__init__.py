'''Quantitative financial timeseries analysis'''

VERSION = (0, 4, 0)
 
def get_version():
    return '.'.join(map(str,VERSION))
 
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

try:
    strtype = basestring
except NameError:
    strtype = str
    
from dynts.exceptions import *
from .backends import timeseries, xydata, TimeSeries, DynData, tsfunctions
from .backends import istimeseries, Formatters, BACKENDS, ts_bin_op
from .dsl import parse, merge, dslresult, function_registry, functions
from .maths import BasicStatistics, pivottable
from .data import providers
from dynts import formatters
Formatters['flot'] = formatters.ToFlot()
Formatters['jsonvba'] = formatters.ToJsonVba()
Formatters['csv']  = formatters.ToCsv()
Formatters['xls']  = formatters.ToXls()
Formatters['plot'] = formatters.ToPlot()


def evaluate(expression, start = None, end = None,
             loader = None, logger = None, backend = None, **kwargs):
    '''Evaluate the timeseries ``expression`` into
a timeseries object
    
:parameter expression: A timeseries aexpression string or an instance
                       of :class:`dynts.dsl.Expr` obtained using
                       the :func:`dynts.parse` function.
:parameter start: Start date or ``None``.
:parameter end: End date or ``None``. If not provided today values is used.
:parameter loader: Optional :class:`dynts.data.TimeSerieLoader` class or instance to use.
:parameter logger: Python logging instance or ``None``. Used if you required logging.
:parameter backend: :class:`dynts.TimeSeries` backend name or ``None``.

The ``expression`` is parsed and the :class:`dynts.expr.Symbol` are sent to the
:class:`dynts.data.TimeSerieLoader` instance for retrieving actual timeseries data.
It returns an instance of :class:`dynts.dslresult`.

Typical usage::

    >>> import dynts
    >>> r = dynts.evaluate('min(GS,window=30)')
    >>> r
    min(GS,window=30)
    >>> ts = r.unwind()
    '''
    if isinstance(expression,strtype):
        expression = parse(expression)
    if expression.malformed():
        raise CouldNotParse(expression)
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
    sp = settings.splittingnames
    return reduce(lambda x,y: '%s%s%s' % (x,sp,y), names)


def composename(name, *names, **kwargs):
    from dynts.conf import settings
    sp = settings.splittingnames
    kw = ','.join(('{0}={1}'.format(*v) for v in kwargs.items()))
    if kw:
        kw = ','+kw
    return sp.join(('{0}({1}{2})'.format(name,x,kw) for x in names))
    

def hasextensions():
    '''True if cython extensions are available'''
    from .lib import hasextensions
    return hasextensions


def functions_docs():
    names = sorted(function_registry.keys())
    docs = ''
    for name in names:
        t = (1+len(name))*'='
        title = '\n{0}\n{1}\n'.format(name,t)
        docs += title
        func = function_registry[name]
        fdoc = func.__doc__
        if fdoc:
            docs += fdoc
    return docs

def dump_docs(filename = 'dyntslist.rst'):
    docs = functions_docs()
    f = open(filename,'w')
    f.write(docs)
    f.close()
    print(('Saved function documentations in {0}'.format(filename)))
        