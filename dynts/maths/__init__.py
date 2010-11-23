from itertools import izip
from utils import *


class BasicStatistics(object):
    
    def __init__(self, ts):
        self.ts = ts
        
    def calculate(self):
        tseries = self.ts
        if not tseries:
            return {}
        names = tseries.names();
        values = tseries.values()
        vlast = list(values[-1])
        vmin  = list(tseries.min())
        vmax  = list(tseries.max())
        vpr   = [(v-nv)/(xv-nv) for v,nv,xv in izip(vlast,vmin,vmax)]
        data  = {
                'names': names,
                'latest': v,
                'min': vmin,
                'mean': list(tseries.mean()),
                'max': vmax,
                'prange': vpr
                }
        return data
    