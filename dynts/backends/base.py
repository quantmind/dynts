from itertools import izip

from dynts.utils import laggeddates, ashash, asbtree, asarray
from dynts.backends.xy import *
from dynts.backends import operators 


ops = operators._ops
ts_bin_op = operators._handle_ts_or_scalar


class TimeSeries(DynData):
    '''A :class:`dynts.DynData` specialisation for timeseries back-ends.
This class expose all the main functionalities of a timeseries

.. attribute:: type

    string indicating the backend type (``zoo``, ``rmetrics``, ``numpy``, etc...)
    
.. attribute:: shape

    tuple containing the timeseries dimensions.
    '''
    type = None
    default_align = 'right'
    
    def __init__(self, name = '', date = None, data = None, info = None):
        super(TimeSeries,self).__init__(name,info)
        self.make(date,data)
    
    __add__ = operators.add
    __sub__ = operators.sub
    __mul__ = operators.mul
    __div__ = operators.div
    
    def __len__(self):
        return self.shape[0]
    
    def count(self):
        '''Number of series in timeseries.'''
        return self.shape[1]
    
    def asbtree(self):
        '''Return an instance of :class:`dynts.utils.wrappers.asbtree`
which exposes binary tree like functionalities of ``self``.'''
        return asbtree(self)
    
    def ashash(self):
        '''Return an instance of :class:`dynts.utils.wrappers.ashash`
which exposes hash-table like functionalities of ``self``.'''
        return ashash(self)
    
    def dateconvert(self, dte):
        return dte
    
    def dateinverse(self, key):
        return key
    
    def max(self, fallback = False):
        '''Max values by series'''
        return asarray(self.apply('max', fallback = fallback)[0])
    
    def min(self, fallback = False):
        '''Max values by series'''
        return asarray(self.apply('min', fallback = fallback)[0])
    
    def mean(self, fallback = False):
        '''Mean values by series'''
        return asarray(self.apply('mean', fallback = fallback)[0])
    
    def median(self, fallback = False):
        '''Median values by series'''
        return asarray(self.apply('median', fallback = fallback)[0])
    
    def returns(self, fallback = False):
        '''Calculate returns as delta(log(self)) by series'''
        return self.logdelta(fallback = fallback)
    
    def dates(self, desc = None):
        '''Returns an iterable over ``datetime.date`` instances in the timeseries.'''
        c = self.dateinverse
        for key in self.keys(desc = desc):
            yield c(key)
            
    def keys(self, desc = None):
        '''Returns an iterable over ``raw`` keys. The keys may be different from dates
for same backend implementations.'''
        raise NotImplementedError
            
    def values(self, desc = None):
        '''Returns a ``numpy.ndarray`` containing the values of the timeseries.
Implementations should try not to copy data if possible. This function
can be used to access the timeseries as if it was a matrix.'''
        raise NotImplementedError
    
    def items(self, desc = None):
        '''Returns a python ``generator`` which can be used to iterate over
:func:`dynts.TimeSeries.dates` and :func:`dynts.TimeSeries.values` returning a two dimensional
tuple ``(date,value)`` in each iteration. Similar to the python dictionary items
function. The additional input parameter *desc* can be used to iterate from
the greatest to the smallest date in the timeseries by passing ''desc=True``'''
        for d,v in izip(self.dates(desc = desc),self.values(desc = desc)):
            yield d,v
            
    def series(self):
        '''Generator of single series.'''
        data = self.values()
        if len(data):
            for c in range(self.count()):
                yield data[:,c]
        else:
            raise StopIteration
            
    def serie(self, index):
        return self.values()[:,index]
    
    def display(self):
        for d,v in self.items():
            print('%s: %s' % (d,v))
    
    def isconsistent(self):
        '''Check if the timeseries is consistent'''
        for dt1,dt0 in laggeddates(self):
            if dt1 <= dt0:
                return False
        return True
    
    # PURE VIRTUAL FUNCTIONS
    
    def start(self):
        '''Start date of timeseries'''
        raise NotImplementedError
    
    def end(self):
        '''End date of timeseries'''
        raise NotImplementedError
    
    def frequency(self):
        '''Average frequency of dates'''
        raise NotImplementedError
    
    @property
    def shape(self):
        raise NotImplementedError
    
    def __getitem__(self, i):
        raise NotImplementedError
    
    def colnames(self):
        raise NotImplementedError
    
    def delta(self, lag = 1, **kwargs):
        '''\
First order derivative. Optimised.

:parameter lag: backward lag
'''
        raise NotImplementedError
    
    def delta2(self, lag = 2, **kwargs):
        '''\
Second order derivative. Optimised.

:parameter lag: backward lag
'''
        raise NotImplementedError
    
    def lag(self, lag = 1):
        raise NotImplementedError
    
    def log(self):
        raise NotImplementedError
    
    def logdelta(self, lag = 1, **kwargs):
        '''Delta in log-space. Used for percentage changes.'''
        raise NotImplementedError
    
    def stddev(self):
        raise NotImplementedError
    
    def apply(self, func,
              window = None,
              bycolumn = True,
              align = None, **kwargs):
        '''Apply function ``func`` to the timeseries.
        
    :keyword func: string indicating function to apply
    :keyword window: Rolling window, If not defined ``func`` is applied on
                     the whole dataset. Default ``None``.
    :keyword bycolumn: If ``True``, function ``func`` is applied on
                       each column separately. Default ``True``.
    :keyword align: string specifying whether the index of the result should be ``left`` or
                    ``right`` (default) or ``centered`` aligned compared to the
                    rolling window of observations.
    :keyword kwargs: dictionary of auxiliary parameters used by function ``func``.'''
        N = len(self)
        window = window or N
        self.precondition(window<=N and window > 0,DyntsOutOfBound)
        return self._rollapply(func,
                               window = window,
                               align = align or self.default_align,
                               bycolumn = bycolumn,
                               **kwargs)
    
    def rollapply(self, func, window = 20, **kwargs):
        '''A generic :ref:`rolling function <rolling-function>` for function *func*.
Same construct as :meth:`dynts.TimeSeries.apply` but with default ``window`` set to ``20``.'''
        return self.apply(func, window=window, **kwargs)
    
    def rollmax(self, **kwargs):
        '''A :ref:`rolling function <rolling-function>` for max values.
Same as::
        
    self.rollapply('max',**kwargs)'''
        return self.rollapply('max',**kwargs)
    
    def rollmin(self, **kwargs):
        '''A :ref:`rolling function <rolling-function>` for min values.
Same as::

    self.rollapply('min',**kwargs)'''
        return self.rollapply('min',**kwargs)
    
    def rollmedian(self, **kwargs):
        '''A :ref:`rolling function <rolling-function>` for median values.
Same as::

    self.rollapply('median',**kwargs)'''
        return self.rollapply('median',**kwargs)
    
    def rollmean(self, **kwargs):
        '''A :ref:`rolling function <rolling-function>` for mean values:
Same as::

    self.rollapply('mean',**kwargs)'''
        return self.rollapply('mean',**kwargs)
    
    def rollstddev(self, **kwargs):
        '''A :ref:`rolling function <rolling-function>` for stadard-deviation values:
Same as::

    self.rollapply('sd',**kwargs)'''
        return self.rollapply('sd',**kwargs)
    
    def window(self, start, end):
        raise NotImplementedError
    
    def merge(self, ts, all = True):
        raise NotImplementedError
    
    def clone(self, date = None, data = None, name = None):
        name = name or self.name
        data = data if data is not None else self.values()
        ts = self.__class__(name)
        if date is None:
            ts.make(self.keys(),data,raw=True)
        else:
            ts.make(date,data)
        return ts
    
    # INTERNALS
    ################################################################
    
    def makename(self, func, window = None, **kwargs):
        if window == len(self) or not window:
            return '%s(%s)' % (func,self.name)
        else:
            return '%s(%s,window=%s)' % (func,self.name,window)
        
    def _rollapply(func, window = 20, **kwargs):
        raise NotImplementedError
    
    def make(self, date, data, **kwargs):
        '''Internal function to create the inner data:
        
* *date* iterable/iterator/generator over dates
* *data* iterable/iterator/generator over values'''
        raise NotImplementedError
    
    def precondition(self, precond, errorclass = DyntsException, msg = ''):
        if not precond:
            raise errorclass(msg)
    