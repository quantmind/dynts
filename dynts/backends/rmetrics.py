from numpy import asarray
from rpy2.robjects import StrVector

from dynts.backends.rbase import rts, r2pydate, isoformat, ny


class TimeSeries(rts):
    '''Timeserie backend based on Rmetrics timeserie__ package
    
__ http://cran.r-project.org/web/packages/timeSeries/index.html
    '''
    type = 'rmetrics'
    libraries = ['timeSeries','zoo']
        
    def factory(self, date, data, **kwargs):
        tdate = self.dateconvert
        adt = StrVector([tdate(dt) for dt in date])
        #data = FloatVector(data)
        return self.r['timeSeries'](data, adt)
    
    def dateconvert(self, dte):
        #isoformat is not defined for datetime objects
        if hasattr(dte, 'date') and callable(dte.date):
            dte = dte.date()
        return isoformat(dte)
    
    def dateinverse(self, x):
        return r2pydate(self.r['as.double'](x)[0]) 
    
    def keys(self):
        '''numpy asarray does not copy data'''
        v = self.rc('time')
        return ny.asarray(v)
                          
    
    def start(self):
        return self.dateinverse(self.rc('start'))
        
    def end(self):
        return self.dateinverse(self.rc('end'))