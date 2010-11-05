#
# TimeSeries Backend based on numpy
#
#
from collections import deque
from itertools import izip
import numpy as ny

import dynts
from dynts.utils import rollingOperation, laggeddates, asarray


arraytype = ny.ndarray


arrayfunc = lambda func, *args : [func(*items) for items in izip()]


_functions = {'min':'min',
              'max':'max',
              ###Ned to check these functions
              'mean': 'mean',
              'med': 'median',
              }


def rollsingle(self, func, window = 20, name = None, **kwargs):
    '''Efficient rolling window calculation for min, max type functions'''
    rolling = lambda serie : list(getattr(rollingOperation(serie,window),func)())
    data = ny.array([rolling(serie) for serie in self.series()])
    name = name or '%s(%s,window=%s)' % (func,self.name,window)
    return self.clone(self.dates()[window-1:], data.transpose(), name = name)


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
            data = asarray(data)
            if len(data.shape) == 1:
                data = data.reshape(len(data),1)
            self._data = data
    
    @property
    def shape(self):
        return self._data.shape
    
    def __getitem__(self, i):
        return self._data[i]
    
    def values(self, desc = None):
        if desc == True:
            return reversed(self._data)
        else:
            return self._data
    
    def dates(self, desc = None):
        if desc == True:
            return reversed(self._date)
        else:
            return self._date
    
    def keys(self, desc = None):
        return self.dates(desc = desc)
    
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
    
    def merge(self, tserie, fill = float("nan"), **kwargs):
        if dynts.istimeseries(tserie):
            tserie = [tserie]
        alldates = set(self.dates())
        hash     = self.ashash()
        thashes  = [(hash,ny.array([fill]*self.count()))]
        for ts in tserie:
            alldates = alldates.union(ts.dates())
            hash.names.extend(ts.names())
            thashes.append((ts.ashash(),ny.array([fill]*ts.count())))
        stack = ny.hstack
        mdt = lambda dt: stack((h.get(dt,ln) for h,ln in thashes))
        for dt in alldates:
            hash[dt] = mdt(dt)
        return hash.getts()
    
    def log(self, name = None, **kwargs):
        v = ny.log(self._data)
        name = name or 'log(%s,%s)' % (self.name,lag)
        return self.clone(self._date,v,name)
            
    def delta(self, lag = 1, name = None, **kwargs):
        self.precondition(lag<len(self) and lag > 0,dynts.DyntsOutOfBound)
        v = self._data[lag:] - self._data[:-lag]
        name = name or 'delta(%s,%s)' % (self.name,lag)
        return self.clone(self._date[lag:],v,name)
    
    def logdelta(self, lag = 1, name = None, **kwargs):
        self.precondition(lag<len(self) and lag > 0,dynts.DyntsOutOfBound)
        v = ny.log(self._data[lag:] - self._data[:-lag])
        name = name or 'logdelta(%s,%s)' % (self.name,lag)
        return self.clone(self._date[lag:],v,name)
    
    def _rollapply(self, func, window = 20, **kwargs):
        func = _functions.get(func,None) or func
        return rollsingle(self, func, window = window, **kwargs)
        
    