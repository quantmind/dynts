from bisect import bisect_left, bisect_right

from dynts.conf import settings
from dynts.utils.section import asarray
from dynts.exceptions import *

__all__ = ['TimeSerieWrap','asbtree','ashash']


class TimeSerieWrap(object):
    
    def __init__(self, ts, **kwargs):
        self.ts = ts
        self.modified = False
        self.names = ts.names()
        self.wrap(**kwargs)
        
    def wrap(self, **kwargs):
        pass
        
    def get(self, dt, default = None):
        '''Equivalent to::

    self[dt]
    
but catches exceptions and return *default*.'''
        try:
            return self[dt]
        except DateNotFound:
            return default
        
    def getts(self):
        return self.ts
        
    @property
    def shape(self):
        return (len(self),self.ts.count())


class asbtree(TimeSerieWrap):
    '''Wrap a :class:`dynts.TimeSeries` and
expose binary-tree like functionalities. A :class:`dynts.TimeSeries` instance
has a shortcut method which construct a ``asbtree``. Here is an example::

    >>> from dynts.utils.populate import randomts, date
    >>> ts = randomts(cols = 2, start = date(2010,1,1), size = 50)
    >>> dts = ts.asbtree()
    >>> sts.find_ge(ts.start())
    1
    >>> sts.find_ge(ts.end())
    49
'''
    def wrap(self):
        ts = self.ts
        self.dates  = asarray(ts.dates())
        self.values = ts.values()
    
    def __len__(self):
        return len(self.dates)
    
    def __getitem__(self, dt):
        '''Get the value at *dt* otherwise it raises
an :class:`dynts.exceptions.DateNotFound`.'''
        try:
            index = self.find_ge(dt)
        except DyntsOutOfBound:
            raise DateNotFound
        if self.dates[index] == dt:
            return self.values[index]
        else:
            raise DateNotFound
        
    def find_ge(self, dt):
        '''Building block of all searches. Find the index
corresponding to the leftmost value greater or equal to *dt*.
If *dt* is greater than the
:func:`dynts.TimeSeries.end` a :class:`dynts.exceptions.RightOutOfBound`
exception will raise.

*dt* must be a python datetime.date instance.'''
        i = bisect_left(self.dates,dt)
        if i != len(self.dates):
            return i
        raise RightOutOfBound
    
    def find_le(self, dt):
        '''Find the index corresponding to the rightmost
value less than or equal to *dt*.
If *dt* is less than :func:`dynts.TimeSeries.end`
a :class:`dynts.exceptions.LeftOutOfBound`
exception will raise.

*dt* must be a python datetime.date instance.'''
        i = bisect_right(self.dates,dt)
        if i:
            return i-1
        raise LeftOutOfBound

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__,self.ts.__repr__())
    
    def __str__(self):
        return '%s(%s)' % (self.__class__.__name__,self.ts)


class ashash(TimeSerieWrap):
    
    def wrap(self):
        ts = self.ts
        hash = {}
        self.hash   = hash
        self.keys   = hash.iterkeys
        self.values = hash.itervalues
        for dt,v in ts.items():
            hash[dt] = v
    
    def __len__(self):
        return len(self.hash)
        
    def __getitem__(self, dt):
        '''Get the value at *dt* otherwise it raises
an :class:`dynts.exceptions.DateNotFound`.'''
        try:
            return self.hash[dt]
        except KeyError:
            raise DateNotFound
    
    def __setitem__(self, dt, item):
        self.hash[dt] = item
        self.modified = True

    def items(self):
        h = self.hash
        for dt in sorted(self.keys()):
            yield dt,h[dt]
            
    def getts(self):
        if self.modified:
            name   = settings.splittingnames.join(self.names)
            hash   = self.hash
            dates  = sorted(self.keys())
            values = (hash[dt] for dt in dates)
            return self.ts.clone(name = name, date = dates, data = values)
        else:
            return self.ts
    