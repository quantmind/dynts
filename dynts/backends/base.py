from itertools import izip
from collections import deque
from dynts.exceptions import *
from dynts.utils import wrappers


Formatters = {}

class TimeSeries(object):
    '''Interface class for timeseries back-ends.
    
    .. attribute:: type
    
        string indicating the backend type (zoo, rmetrics, numpy, etc...)
        
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
        return wrappers.asbtree(self)
    
    def ashash(self):
        '''Return an instance of :class:`dynts.utils.wrappers.ashash`
which exposes hash-table like functionalities of ``self``.'''
        return wrappers.ashash(self)
    
    def dateconvert(self, dte):
        return dte
    
    def dateinverse(self, key):
        return key
    
    def max(self):
        '''Max value'''
        return self.rollmax()[0]
    
    def min(self):
        '''Max value'''
        return self.rollmin()[0]
    
    def mean(self):
        '''Mean value'''
        return self.rollmean()[0]
    
    def returns(self, k = 1):
        '''Calculate returns as delta(log(self))'''
        return self.log().delta(k)
    
    def dates(self):
        '''Returns an iterable over ``datetime.date`` instances in the timeseries.'''
        c = self.dateinverse
        for key in self.keys():
            yield c(key)
            
    def lagdates(self, step = 1):
        if step == 1:
            dates = self.dates()
            dt0 = dates.next()
            for dt1 in dates:
                yield dt1,dt0
                dt0 = dt1
        else:
            q = deque()
            while done:
                done+=1
                lag.append(dates.next())
            for dt1 in dates:
                lag.append(dt1)
                yield dt1,lag.pop(0)
            
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
            
    def lagitems(self, step = 1):
        '''Efficient iteration over lagged elements.'''
        done = 0
        items  = self.items()
        lag    = deque()
        while done:
            done+=1
            lag.append(items.next())
        for i1 in items:
            lag.append(i1)
            yield i1,lag.pop(0)
    
    def display(self):
        '''Nicely display self on the shell. Useful during prototyping and development.'''
        for d,v in self.items():
            print('%s: %s' % (d,v))
            
    def dump(self, format = None, **kwargs):
        '''Dump the timeseries using a specific :ref:`format <formatters>`.'''
        formatter = Formatters.get(format,None)
        if not format:
            return self.display()
        else:
            return formatter(self,**kwargs)
    
    def isconsistent(self):
        '''Check if the timeseries is consistent'''
        for dt1,dt0 in self.lagdates():
            if dt1 <= dt0:
                return False
        return True
    
    # PURE VIRTUAL FUNCTIONS
    
    @property
    def shape(self):
        raise NotImplementedError
    
    def __getitem__(self, i):
        raise NotImplementedError
    
    def keys(self):
        raise NotImplementedError
    
    def colnames(self):
        raise NotImplementedError
    
    def delta(self, k = 1):
        raise NotImplementedError
    
    def lag(self, k = 1):
        raise NotImplementedError
    
    def log(self):
        raise NotImplementedError
    
    def stddev(self):
        raise NotImplementedError
    
    def rollmax(self, window = None):
        raise NotImplementedError
    
    def rollmin(self, window = None):
        raise NotImplementedError
    
    def rollmean(self, window = None):
        raise NotImplementedError
    
    def start(self):
        '''Start date of timeseries'''
        raise NotImplementedError
    
    def end(self):
        '''End date of timeseries'''
        raise NotImplementedError
    
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
    
    def make(self, date, data, **kwargs):
        '''Internal function to create the inner data:
        
* *date* iterable/iterator/generator over dates
* *data* iterable/iterator/generator over values'''
        raise NotImplementedError