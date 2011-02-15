#
# TimeSeries Backend based on numpy
#
#
from collections import deque
from itertools import izip
import numpy as np

import dynts
from dynts import lib, composename
from dynts.utils import laggeddates, asarray


arraytype = np.ndarray


arrayfunc = lambda func, *args : [func(*items) for items in izip()]


_functions = {'min':'min',
              'max':'max',
              'mean': 'mean',
              'med': 'median',
              'sd': 'sd'
              }


def rollsingle(self, func, window = 20, name = None,
               fallback = False, **kwargs):
    '''Efficient rolling window calculation for min, max type functions'''
    rname = 'roll_{0}'.format(func)
    if fallback:
        rfunc = getattr(lib.fallback,rname)
    else:
        rfunc = getattr(lib,rname,None)
        if not rfunc:
            rfunc = getattr(lib.fallback,rname)
    rolling = lambda serie : list(rfunc(serie,window))
    data = np.array([rolling(serie) for serie in self.series()])
    name = name or self.makename(func,window=window)
    dates = asarray(self.dates())
    return self.clone(dates[window-1:], data.transpose(), name = name)
    

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
            data = asarray(data, np.double)
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
        thashes  = [(hash,np.array([fill]*self.count()))]
        for ts in tserie:
            alldates = alldates.union(ts.dates())
            hash.names.extend(ts.names())
            thashes.append((ts.ashash(),np.array([fill]*ts.count())))
        stack = np.hstack
        mdt = lambda dt: stack((h.get(dt,ln) for h,ln in thashes))
        for dt in alldates:
            hash[dt] = mdt(dt)
        return hash.getts()
    
    def log(self, name = None, **kwargs):
        v = np.log(self._data)
        name = name or composename('log',*self.names())
        return self.clone(self._date,v,name)
    
    def sqrt(self, name = None, **kwargs):
        v = np.sqrt(self._data)
        name = name or composename('sqrt',*self.names())
        return self.clone(self._date,v,name)
    
    def square(self, name = None, **kwargs):
        v = np.square(self._data)
        name = name or composename('square',*self.names())
        return self.clone(self._date,v,name)
            
    def delta(self, lag = 1, name = None, **kwargs):
        self.precondition(lag<len(self) and lag > 0,dynts.DyntsOutOfBound)
        v = self._data[lag:] - self._data[:-lag]
        name = name or 'delta(%s,%s)' % (self.name,lag)
        return self.clone(self._date[lag:],v,name)
    
    def delta2(self, lag = 1, name = None, **kwargs):
        lag2 = 2*lag
        self.precondition(lag2<len(self) and lag2 > 0,dynts.DyntsOutOfBound)
        d = self._data
        v = d[lag2:] + d[:-lag2] - 2*d[lag:-lag]
        name = name or 'delta2(%s,%s)' % (self.name,lag)
        return self.clone(self._date[lag2:],v,name)
    
    def logdelta(self, lag = 1, name = None, **kwargs):
        self.precondition(lag<len(self) and lag > 0,dynts.DyntsOutOfBound)
        v = np.log(self._data[lag:]/self._data[:-lag])
        name = name or 'logdelta(%s,%s)' % (self.name,lag)
        return self.clone(self._date[lag:],v,name)
    
    def _rollapply(self,
                   func,
                   window = 20,
                   bycolumn = True,
                   **kwargs):
        # NUMPY implementation of the rollapply function
        func = _functions.get(func,None) or func
        if bycolumn:
            return rollsingle(self, func, window = window, **kwargs)
        else:
            raise NotImplementedError
        
    