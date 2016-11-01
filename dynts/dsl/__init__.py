'''A domain specific language for timeseries analysis and manipulation.

Created using ply (http://www.dabeaz.com/ply/) a pure Python implementation
of the popular compiler construction tools lex and yacc.
'''
from ccy import todate

from dynts.conf import settings
from dynts.exc import ExpressionError, CouldNotParse
from dynts.backends import istimeseries, isxy
from dynts.data import providers

from .ast import *
from .registry import FunctionBase, ComposeFunction, function_registry

try:
    from .rules import parsefunc
except ImportError:
    parsefunc = None


def parse(timeseries_expression, method=None, functions=None, debug=False):
    '''Function for parsing :ref:`timeseries expressions <dsl-script>`.
    If succesful, it returns an instance of :class:`dynts.dsl.Expr` which
    can be used to to populate timeseries or scatters once data is available.

    Parsing is implemented using the ply_ module,
    an implementation of lex and yacc parsing tools for Python.

    :parameter expression: A :ref:`timeseries expressions <dsl-script>` string.
    :parameter method: Not yet used.
    :parameter functions: dictionary of functions to use when parsing.
        If not provided the :data:`dynts.function_registry`
        will be used.

        Default ``None``.
    :parameter debug: debug flag for ply_.  Default ``False``.

    For examples and usage check the :ref:`dsl documentation <dsl>`.

    .. _ply: http://www.dabeaz.com/ply/
    '''
    if not parsefunc:
        raise ExpressionError('Could not parse. No parser installed.')
    functions = functions if functions is not None else function_registry
    expr_str = str(timeseries_expression).lower()
    return parsefunc(expr_str, functions, method, debug)


def merge(series):
    '''Merge timeseries into a new :class:`dynts.TimeSeries` instance.

    :parameter series: an iterable over :class:`dynts.TimeSeries`.
    '''
    series = iter(series)
    ts = next(series)
    return ts.merge(series)


class dslresult(object):
    '''Class holding the results of an interpreted expression.
    Instances of this class are returned when invoking the
    :func:`dynts.evaluate` high level function.

    .. attribute:: expression

        An instance of :class:`dynts.dsl.Expr` obtained when interpreting a
        timesries expression string via :func:`dynts.parse`.

    .. attribute:: data

        data which is used to populate timeseries or scatters.

    .. attribute:: backend

        backend used when populating timeseries.
    '''
    def __init__(self, expression, data, backend = None):
        self.expression = expression
        self.data = data
        self.backend = backend or settings.backend

    def __repr__(self):
        return self.expression.__repr__()

    def __str__(self):
        return self.__repr__()

    def unwind(self):
        if not hasattr(self,'_ts'):
            self._unwind()
        return self

    def ts(self):
        '''The associated timeseries, if available.'''
        self.unwind()
        return self._ts

    def xy(self):
        '''The associated scatters, if available.'''
        self.unwind()
        return self._xy

    def _unwind(self):
        res = self.expression.unwind(self.data, self.backend)
        self._ts = None
        self._xy = None
        if istimeseries(res):
            self._ts = res
        elif res and isinstance(res,list):
            tss = []
            xys = []
            for v in res:
                if istimeseries(v):
                    tss.append(v)
                elif isxy(v):
                    xys.append(v)
            if tss:
                self._ts = merge(tss)
            if xys:
                self._xy = xys
        elif isxy(res):
            self._xy = res

    def dump(self, format, **kwargs):
        ts = self.ts()
        xy = self.xy()
        if istimeseries(ts):
            ts = ts.dump(format, **kwargs)
        else:
            ts = None
        if xy:
            if isxy(xy):
                xy = [xy]
            for el in xy:
                ts = el.dump(format, container = ts, **kwargs)
        return ts


def evaluate(expression, start=None, end=None, loader=None, logger=None,
             backend=None, **kwargs):
    '''Evaluate a timeseries ``expression`` into
an instance of :class:`dynts.dsl.dslresult` which can be used
to obtain timeseries and/or scatters.
This is probably the most used function of the library.

:parameter expression: A timeseries expression string or an instance
    of :class:`dynts.dsl.Expr` obtained using the :func:`dynts.parse` function.
:parameter start: Start date or ``None``.
:parameter end: End date or ``None``. If not provided today values is used.
:parameter loader: Optional :class:`dynts.data.TimeSerieLoader`
    class or instance to use.

    Default ``None``.
:parameter logger: Optional python logging instance, used if you required
    logging.

    Default ``None``.
:parameter backend: :class:`dynts.TimeSeries` backend name or ``None``.

The ``expression`` is parsed and the :class:`dynts.dsl.Symbol` are sent to the
:class:`dynts.data.TimeSerieLoader` instance for retrieving
actual timeseries data.
It returns an instance of :class:`dynts.dsl.dslresult`.

Typical usage::

    >>> import dynts
    >>> r = dynts.evaluate('min(GS,window=30)')
    >>> r
    min(GS,window=30)
    >>> ts = r.ts()
    '''
    if isinstance(expression, strtype):
        expression = parse(expression)
    if not expression or expression.malformed():
        raise CouldNotParse(expression)
    symbols = expression.symbols()
    start = start if not start else todate(start)
    end = end if not end else todate(end)
    data = providers.load(symbols, start, end, loader=loader,
                          logger=logger, backend=backend, **kwargs)
    return dslresult(expression, data, backend=backend)
