from rpy2 import rinterface
from numpy import asarray, ndarray, double

import dynts
from dynts import composename
from dynts.utils import ascolumn
from dynts.utils.rutils import rpyobject, py2rdate, r2pydate, isoformat

r_variance ='''\
var <- function(x,ddof=0) {
    (sum(x*x) - sum(x)^2/length(x))/(length(x)-ddof)
}

sd <- function(x,ddof=0) {sqrt(var(x,ddof))}
'''

class rts(dynts.TimeSeries,rpyobject):
    '''Base class for R-based timeseries objects'''
    scripts = ['logdelta <- function(df,lag){ diff(log(df),lag)}',
               r_variance]
    
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
            data = ascolumn(data, double)
            ts = self.factory(date, data, raw = raw)
        self._ts = ts
        
    def keys(self, desc = None):
        '''numpy asarray does not copy data'''
        res = asarray(self.rc('index'))
        if desc == True:
            return reversed(res)
        else:
            return res
        
    def values(self, desc = None):
        '''numpy asarray does not copy data'''
        if self._ts:
            res = asarray(self._ts)
            if desc == True:
                return reversed(res)
            else:
                return res
        else:
            return ndarray([0,0])
        
    def lag(self, k = 1, **kwargs):
        return self.rcts('lag',k)
    
    def delta(self, lag = 1, name = None, **kwargs):
        name = name or 'delta(%s,%s)' % (self.name,lag)
        return self.rcts('diff', lag = lag, name = name)
    
    def delta2(self, lag = 1, name = None, **kwargs):
        name = name or 'delta(%s,%s)' % (self.name,lag)
        return self.rcts('diff', lag = lag, differences = 2, name = name)
    
    def log(self, name = None, **kwargs):
        name = name or composename('log',*self.names())
        return self.rcts('log', name = name)
    
    def sqrt(self, name = None, **kwargs):
        name = name or composename('sqrt',*self.names())
        return self.rcts('sqrt', name = name)
    
    def square(self, name = None, **kwargs):
        self.r('''square <- function(x){x*x}''')
        name = name or composename('square',*self.names())
        return self.rcts('square', name = name)
    
    def logdelta(self, lag = 1, name = None, **kwargs):
        name = name or 'logdelta(%s,%s)' % (self.name,lag)
        return self.rcts('logdelta',lag, name = name)
    
    #def var(self, ddof = 0):
    #    return [self.rc('var',serie,ddof) for serie in self.series()]
    
    def isregular(self):
        return self.rc('is.regular')[0]
    
    def frequency(self):
        return self.rc('frequency')[0]
    
    def window(self, start, end):
        c = self.dateconvert
        return self.rcts('window', start = c(start), end = c(end))

    def rc(self, command, *args, **kwargs):
        return self.r[command](self._ts,*args,**kwargs)
    
    def rcts(self, command, *args, **kwargs):
        '''General function for applying a rolling R function to a timeserie'''
        cls = self.__class__
        name = kwargs.pop('name','')
        date = kwargs.pop('date',None)
        data = kwargs.pop('data',None)
        kwargs.pop('bycolumn',None)
        ts  = cls(name=name,date=date,data=data)
        ts._ts = self.rc(command, *args, **kwargs)
        return ts
