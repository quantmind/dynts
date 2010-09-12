from itertools import izip
from rpy2.robjects import IntVector

from dynts.backends.rbase import tsbase, rts

 
def v2bool(v):
    try:
        return v[0]
    except:
        return False
    

def tozoo(ts):
    if isinstance(ts,tsbase):
        if ts.type == 'zoo':
            return ts
        else:
            raise NotImplementedError('Cannot convert %s to zoo timeserie' % ts)
    else:
        raise ValueError('%s is not a timeserie object' % ts)


class timeserie(rts):
    libraries = ['zoo,PerformanceAnalytics']
        
    def __init__(self, *args, **kwargs):
        super(timeserie,self).__init__(*args, **kwargs)
    
    def factory(self, date, data, raw = False):
        if not raw:
            tdate = self.dateconvert
            date = IntVector([tdate(dt) for dt in date])
        #data = FloatVector(data)
        return self.r['zoo'](data,date)
    
    def colnames(self):
        #TODO: Not working since we did not set names
        return self.r['colnames'](self._ts)
    
    def rollmin(self, window = None):
        window = window or len(self)
        fun    = self.r['min']
        return self.rcts('rollapply',window,fun)
    
    def start(self):
        return self.dateinverse(self.rc('start')[0])
        
    def end(self):
        return self.dateinverse(self.rc('end')[0])
    
    def merge(self, ts, all = True):
        ts = tozoo(ts)
        return self.rcts('merge', ts._ts, all = all)
    