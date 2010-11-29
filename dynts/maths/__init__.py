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
        data  = {
                'names': names,
                'latest': list(values[-1]),
                'min': list(tseries.min()),
                'mean': list(tseries.mean()),
                'max': list(tseries.max()),
                }
        return data
    

class SimpleStatisticsTable(object):
    
    def __init__(self, data):
        self.data = data
        
    def headers(self):
        return ['','latest','min','mean','max','% range']
    
    def table(self):
        data = self.data
        iterator = izip(data['names'],data['latest'],data['min'],data['mean'],data['max'])
        for name,lat,min,mea,max in iterator:
            range = max - min
            prange = 0 if not range else 100*(lat-min)/(max-min)
            yield name,lat,min,mea,max,prange
        
    