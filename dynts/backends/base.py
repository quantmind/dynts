from itertools import izip
from collections import deque
from dynts.exceptions import *
from dynts.utils import laggeddates, ashash, asbtree, asarray


Formatters = {}

class TimeSeries(object):
    '''Interface class for timeseries back-ends.
    
    .. attribute:: type
    
        string indicating the backend type (``zoo``, ``rmetrics``, ``numpy``, etc...)
        
    .. attribute:: shape
    
        tuple containing the timeseries dimensions.
    '''
    type = None
    
    def __init__(self, name = '', date = None, data = None):
        self.name    = str(name)
        self.make(date,data)
        
    def __repr__(self):
        d = self.description()
        b = '%s:%s' % (self.__class__.__name__,self.__class__.type)
        if d:
            return '%s:%s' % (b,d)
        else:
            return b
    
    def __str__(self):
        return self.description()
    
    def names(self):
        '''List of names for each timeseries'''
        N = self.count()
        names = self.name.split(',')[:N]
        n = 0
        while len(names) < N:
            n += 1
            names.append('unnamed%s' % n)
        return names        
        
    def description(self):
        return self.name
    
    def __len__(self):
        return self.shape[0]
    
    def count(self):
        '''Number of series in the timeseries'''
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
    
    def max(self):
        '''Max value'''
        return asarray(self.apply('max')[0])
    
    def min(self):
        '''Max value'''
        return asarray(self.apply('min')[0])
    
    def mean(self):
        '''Mean value'''
        return asarray(self.apply('mean')[0])
    
    def returns(self, k = 1):
        '''Calculate returns as delta(log(self))'''
        return self.log().delta(k)
    
    def dates(self):
        '''Returns an iterable over ``datetime.date`` instances in the timeseries.'''
        c = self.dateinverse
        for key in self.keys():
            yield c(key)
            
    def keys(self):
        '''Returns an iterable over ``raw`` keys. The keys may be different from dates
for same backend implementations.'''
        raise NotImplementedError
            
    def values(self):
        '''Returns a ``numpy.ndarray`` containing the values of the timeseries.
Implementations should try not to copy data if possible. This function
can be used to access the timeseries as if it was a matrix.'''
        raise NotImplementedError
    
    def items(self):
        '''Returns a python ``generator`` which can be used to iterate over
:func:`dynts.TimeSeries.dates` and :func:`dynts.TimeSeries.values` returning a two dimensional
tuple ``(date,value)`` in each iteration. Similar to the python dictionary items
function.'''
        for d,v in izip(self.dates(),self.values()):
            yield d,v
            
    def series(self):
        '''geneator of timeseries series'''
        data = self.values()
        for c in range(self.count()):
            yield data[:,c]
            
    def serie(self, index):
        '''Get serie data by column *index*.'''
        return self.values()[:,index]
    
    def display(self):
        '''Nicely display self on the shell. Useful during prototyping and development.'''
        for d,v in self.items():
            print('%s: %s' % (d,v))
            
    def dump(self, format = None, **kwargs):
        '''Dump the timeseries using a specific :ref:`format <formatters>`.'''
        formatter = Formatters.get(format,None)
        if not format:
            return self.display()
        elif not formatter:
            raise FormattingException('Formatter %s not available' % format)
        else:
            return formatter(self,**kwargs)
    
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
    
    def delta(self, k = 1):
        raise NotImplementedError
    
    def lag(self, k = 1):
        raise NotImplementedError
    
    def log(self):
        raise NotImplementedError
    
    def logdelta(self):
        pass
    
    def stddev(self):
        raise NotImplementedError
    
    def apply(self, func, **kwargs):
        return self._rollapply(func, window = len(self), **kwargs)
    
    def rollapply(self, func, window = 20,
                  align = 'right', bycolumn = True,  **kwargs):
        '''A generic :ref:`rolling function <rolling-function>` for function *func*.

* *func* string indicating function, such as ``min``, ``max``, ``std`` and so forth
* *window* number of point per group.
* *align* string specifying whether the index of the result should be ``left`` or
  ``right`` (default) or ``centered`` aligned compared to the rolling window of observations.
* *bycolumn* if ``True`` each *func* will be applied to each column separately.'''
        window = window or len(self)
        self.precondition(window<=len(self) and window > 0,DyntsOutOfBound)
        return self._rollapply(func, window = window,
                               align = align,
                               bycolumn = bycolumn, **kwargs)
    
    def rollmax(self, **kwargs):
        '''A :ref:`rolling function <rolling-function>` for max values'''
        return self.rollapply('max',**kwargs)
    
    def rollmin(self, **kwargs):
        '''A :ref:`rolling function <rolling-function>` for max values'''
        return self.rollapply('min',**kwargs)
    
    def rollmedian(self, **kwargs):
        '''A :ref:`rolling function <rolling-function>` for median values'''
        return self.rollapply('median',**kwargs)
    
    def rollmean(self, **kwargs):
        '''A :ref:`rolling function <rolling-function>` for mean values'''
        return self.rollapply('mean',**kwargs)
    
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
        
    def __add__(self, other):
        return addts(self,other)
    
    # INTERNALS
    ################################################################
    
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