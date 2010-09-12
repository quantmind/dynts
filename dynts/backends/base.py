from itertools import izip
from dynts.exceptions import *


class tsbase(object):
    '''Base class for timeseries back-ends'''
    type = None
    
    def __init__(self, typ, name = '', date = None, data = None):
        self.__class__.type  = typ
        self.name    = name
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
    
    def description(self):
        return self.name
    
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
        c = self.dateinverse
        for key in self.keys():
            yield c(key)
            
    def __len__(self):
        return self.shape[0]
    
    def count(self):
        return self.shape[1]
    
    def items(self):
        for d,v in izip(self.dates(),self.values()):
            yield d,v
    
    def display(self):
        for d,v in self.items():
            print d,v
            
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
    
    def make(self, date, data, **kwargs):
        '''Fill timeserie object:
         * *date* iterable/iterator/generator over dates
         * *data* iterable/iterator/generator over values
        '''
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
        raise NotImplementedError
    
    def end(self):
        raise NotImplementedError
    
    def window(self, start, end):
        raise NotImplementedError
    
    def merge(self, ts, all = True):
        raise NotImplementedError
    
    def clone(self, data = None, name = None):
        name = name or self.name
        data = data if data is not None else self.values()
        ts = self.__class__(self.__class__.type, name)
        ts.make(self.keys(),data,raw=True)
        return ts
        