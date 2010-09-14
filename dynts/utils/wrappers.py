from bisect import bisect_left
from dynts.exceptions import *


class asdict(object):
    '''Wrap a :class:`dynts.TimeSeries` and
expose dictionary-like functionalities. A :class:`dynts.TimeSeries` instance
has a shortcut method which construct a ``asdict``. Here is an example::

    >>> from dynts.utils.populate import randomts, date
    >>> ts = randomts(cols = 2, start = date(2010,1,1), size = 50)
    >>> dts = ts.asdict()
    >>> sts.find_ge(ts.start())
    1
    >>> sts.find_ge(ts.end())
    49
'''
    def __init__(self, ts):
        self.ts = ts
        self.dates  = list(ts.dates())
        self.values = ts.values()
    
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
    
    def get(self, dt, default = None):
        '''Equivalent to::

    self[dt]
    
but catches exceptions and return *default*.'''
        try:
            return self[dt]
        except DateNotFound:
            return default
        
    def find_ge(self, dt):
        '''Building block of all searches. Find the 
leftmost value greater or equal to *dt*. If *dt* is greater than the
:func:`dynts.TimeSeries.end` date a :class:`dynts.exceptions.RightOutOfBound`
exception will raise, otherwise it returns the index.

*dt* must be a python datetime.date instance.'''
        i = bisect_left(self.dates,dt)
        if i != len(self.dates):
            return i
        raise RightOutOfBound

    def __len__(self):
        return len(self.dates)
    
    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__,self.ts.__repr__())
    
    def __str__(self):
        return '%s(%s)' % (self.__class__.__name__,self.ts)
    
    def range(self, start, end):
        i1 = self.find_ge(start)
        i2 = self.find_ge(end)
        return self.dates[i1-1:i2-1]

        