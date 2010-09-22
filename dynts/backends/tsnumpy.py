#
# TimeSeries Backend based on numpy
#
#
from collections import deque
from itertools import izip
import numpy as ny

import dynts
from dynts.utils.iterators import laggeddates
from dynts.utils.skiplist import RollingOrderedListOperation


arraytype = ny.ndarray


arrayfunc = lambda func, *args : [func(*items) for items in izip()]


_functions = {'min':min,
              'max':max}


def rollsingle(self, func, window = 20, name = None, **kwargs):
    '''Efficient rolling window calculation for min, max type functions'''
    rolling = lambda serie : list(getattr(RollingOrderedListOperation(serie,window),func)())
    data = ny.array([rolling(serie) for serie in self.series()])
    name = name or '%s(%s,window=%s)' % (func,self.name,window)
    return self.clone(self.dates()[window:], data.transpose(), name = name)
    

def asarray(iterable):
    if isinstance(iterable,arraytype):
        return iterable
    else:
        if not hasattr(iterable,'__len__'):
            iterable = list(iterable)
        return ny.array(iterable)


def days(d1,d0):
    t = d1 - d0
    return t.days + (t.seconds + 0.000001*t.microseconds)/86400.0


class TimeSeries(dynts.TimeSeries):
    '''A timeserie based on numpy'''
    type = 'numpy'
    
    def make(self, date, data, raw = False):
        if date is None:
            self._date = None
            self._data = None
        else:
            self._date = asarray(date)
            self._data = asarray(data)
    
    @property
    def shape(self):
        return self._data.shape
    
    def __getitem__(self, i):
        return self._data[i]
    
    def values(self):
        return self._data
    
    def dates(self):
        return self._date
    
    def keys(self):
        return self._date
    
    def start(self):
        return self._date[0]
    
    def end(self):
        return self._date[-1]
    
    def isregular(self):
        dates = self.dates().__iter__()
        d0 = dates.next()
        d1 = dates.next()
        dt = d1 - d0
        for d2 in dates:
            if d2 - d1 == dt:
                d1 = d2
                continue
            return False
        return True
    
    def frequency(self):
        freq = 0;
        for d1,d0 in laggeddates(self):
            freq += days(d1,d0) 
        return freq/(len(self)-1)
    
    def window(self, start, end):
        b = self.asbtree()
        i1 = b.find_ge(start)
        i2 = b.find_le(end)
        return self.clone(self._date[i1:i2+1],
                          self._data[i1:i2+1])
    
    def merge(self, ts, fill = float("nan"), **kwargs):
        h1 = self.ashash()
        h2 = ts.ashash()
        alldates = set(self.dates()).union(ts.dates())
        lnan1 = ny.array([fill]*self.count())
        lnan2 = ny.array([fill]*ts.count())
        stack = ny.hstack
        for dt in alldates:
            h1[dt] = stack((h1.get(dt,lnan1),h2.get(dt,lnan2)))
        return h1.getts()
    
    def serie(self, index):
        return self._data[:,index]
    
    def series(self):
        for c in range(self.count()):
            yield self._data[:,c]
    
    def log(self):
        pass
    
    def delta(self, k = 1, name = None):
        self.precondition(k<len(self) and k > 0,dynts.DyntsOutOfBound)
        v = self._data[k:] - self._data[:-k]
        name = name or 'delta(%s,%s)' % (self.name,k)
        return self.clone(self._date[k:],v,name)
    
    def _rollapply(self, func, window = 20, **kwargs):
        fs = _functions.get(func,None)
        if fs:
            return rollsingle(self, func, window = window, **kwargs)
            
    