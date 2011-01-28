from dynts.utils.py2py3 import zip
from dynts import tsfunctions


class BasicStatistics(object):
    default_functions = ['min','mean','max']
    
    def __init__(self, ts, functions = None):
        self.functions = functions or self.default_functions
        self.ts = ts
        
    def count(self):
        return self.ts.count()
        
    def calculate(self):
        tseries = self.ts
        if not tseries:
            return {}
        names = tseries.names();
        values = tseries.values()
        data  = {
                'names': names,
                'latest': list(values[-1]),
                }
        for name in self.functions:
            func = getattr(tseries,name,None)
            if not func:
                tfunc = getattr(tsfunctions,name,None)
                if tfunc:
                    func = lambda : tfunc(tseries, window = len(tseries))
            if func:
                try:
                    data[name] = list(func())
                except Exception:
                    pass
        return data
    
    
class pivottable(object):
    
    def __init__(self, data, default = 'latest'):
        self.default = default
        self.data = data
        if data:
            self.names = data['names']
            self.defaultname = self.names[0]
            d = self.default
            self._names = dict(((name,{d:v}) for name,v in zip(data['names'],data[d])))
        else:
            self._names = None
        
    def __get_fields(self):
        return self.data.keys()
    fields = property(__get_fields)
        
    def get(self, code, name = None):
        if not self._names:
            return None
        
        dnames = self._names
        
        # First we check if code is a name
        if not name:
            v = dnames.get(code,None)
            if v:
                return v[self.default]
            name = self.defaultname
            
        # Check if name is available, otherwise return None
        nd = dnames.get(name,None)
        if not nd:
            return None
        
        v = nd.get(code,None)
        if v:
            return v
        
        v = self.data.get(code,None)
        if v:
            for nam,val in zip(self.names,v):
                dnames[nam][code] = val
        
        v = nd.get(code,None)
        if v:
            return v
        
        func = getattr(self,'calculate_{0}'.format(code),None)
        if func:
            return func(name)
    
    def calculate_prange(self, name):
        '''Latest value as percentage in range'''
        lat  = self.get('latest',name)
        min  = self.get('min',name)
        max  = self.get('max',name)
        dd   = max - min
        if dd:
            return 100.*(lat-min)/dd
        else:
            return 0.
        
    def calculate_range(self, name, significant = 4):
        min  = self.get('min',name)
        max  = self.get('max',name)
        return [min,max]
            

class SimpleStatisticsTable(object):
    
    def __init__(self, data):
        self.data = data
        
    def headers(self):
        return ['','latest','min','mean','max','% range']
    
    def table(self):
        data = self.data
        if data:
            iterator = zip(data['names'],data['latest'],data['min'],data['mean'],data['max'])
            for name,lat,min,mea,max in iterator:
                range = max - min
                prange = 0 if not range else 100*(lat-min)/(max-min)
                yield name,lat,min,mea,max,prange
        else:
            raise StopIteration
        
        
    