from rpy2 import rinterface
import numpy as ny

import dynts
from dynts.utils.rutils import rpyobject, py2rdate, r2pydate, isoformat



class rts(dynts.TimeSeries,rpyobject):
    '''Base class for R-based timeseries objects'''
    
    @property
    def shape(self):
        try:
            s = tuple(self.rc('dim'))
        except:
            s = self.values().shape
        if len(s) == 1:
            s += 1,
        return s
    
    def __getitem__(self, i):
        '''This is not an efficient method'''
        return self.values()[i]
    
    def factory(self, date, data, raw = False):
        raise NotImplementedError
    
    def dateconvert(self, dte):
        return py2rdate(dte)
    
    def dateinverse(self, key):
        return r2pydate(key)
    
    def make(self, date, data, raw = False):
        if date is None:
            ts = None
        else:
            if not isinstance(data,ny.ndarray):
                if not hasattr(data,'__len__'):
                    data = list(data)
                data = ny.asarray(data)
            ts = self.factory(date, data, raw = raw)
        self._ts = ts
        
    def keys(self):
        '''numpy asarray does not copy data'''
        return ny.asarray(self.rc('index'))
        
    def values(self):
        '''numpy asarray does not copy data'''
        if self._ts:
            return ny.asarray(self._ts)
        else:
            return ny.ndarray([0,0])
        
    def lag(self, k = 1):
        return self.rcts('lag',k)
    
    def delta(self, k = 1):
        return self.rcts('diff',k)
    
    def log(self):
        return self.rcts('log')
    
    def stddev(self):
        raise self.rcts('sd')
    
    def isregular(self):
        return self.rc('is.regular')[0]
    
    def frequency(self):
        return self.rc('frequency')[0]
    
    def rollmax(self, window = None):
        window = window or len(self)
        return self.rcts('rollmax',window)
    
    def rollmean(self, window = None):
        window = window or len(self)
        return self.rcts('rollmean',window)
    
    def window(self, start, end):
        c = self.dateconvert
        return self.rcts('window', start = c(start), end = c(end))

    def rc(self, command, *args, **kwargs):
        return self.r[command](self._ts,*args,**kwargs)
    
    def rcts(self, command, *args, **kwargs):
        cls = self.__class__
        name = kwargs.pop('name','')
        date = kwargs.pop('date',None)
        data = kwargs.pop('data',None)
        ts  = cls(name=name,date=date,data=data)
        ts._ts = self.rc(command, *args, **kwargs)
        return ts
