'''
This is just a landing zone for working on possible functionality that can be moved into the base timeseries class
'''

import datetime
import operator

class Properties(object):
    
    def __init__(self):
        self._properties = {}
    
    def add(self, name, prop):
        props = self._properties
        props[name] = prop
    
    def get(self, name):
        props = self._properties
        prop = props.get(name, None)
        if prop is None:
            msg = "There is no property with name %s, choices are: %s"
            raise ValueError(msg %(name, props.keys()))
        return prop
    
    def all(self):
        props = dict(self._properties)
        return props
    
    def merge(self, properties, op=None):
        '''        
        '''
        ops = {'add' : '+',
               'sub' : '-',
               'mult' : '*',
               'div' : '/'}
        if op:
            cat = ops.get(op, None)
            if cat is None:
                msg = "Operation %s not recognised. Choices: %s"
                raise ValueError(msg %(op, ops) )
        else:
            cat = None
        cur_props = self._properties
        for p , val in properties.items():
            if p in cur_props:
                cur_prop = cur_props[p]
                if cur_prop==val:
                    continue
                else:
                    if cat:
                        new_val = cat.join([cur_prop, val])                         
                    else:
                        if isinstance(cur_prop, list):
                            new_val = cur_prop.append(val)
                        else:
                            new_val = [cur_prop, val]
            else:
                new_val = val
            cur_props[p] = new_val

class Analytics(object):
    ops = {}
    
    def __init__(self, ts):
        self.ts = ts
    
    def add_op(self, name, op):
        '''
        Add a new analytic operation
        '''
        ops = self.ops
        ops[name] = op
    
    def get_op(self, name):
        ops = self.ops
        op = ops.get(name, None)
        if op is None:
            op = getattr(operator, name, None)
            if op is None:
                msg = "No operation named %s. Choices are %s"
                raise ValueError(msg %(name, ops))
            else:
                ops[name] = op
        return op
    
    def _ts_op(self, other_ts, op_name):
        op = self.get_op(op_name)
        ts = self.ts
        all_dates = set(ts.keys()).union(set(other_ts.keys()))
        new_ts = ts.copy()
        new_ts.properties.merge(other_ts.properties.all())
        for dt in all_dates:
            val = ts.get(dt, None)
            val2 = other_ts.get(dt, None)
            if not(val is None or val2 is None):
                new_val = op(val, val2)
            else:
                new_val = None
            new_ts[dt] = new_val
        return new_ts
    
    def _scalar_op(self, scalar, op_name):
        op = self.get_op(op_name)
        ts = self.ts
        all_dates = ts.keys()
        new_ts = ts.copy()
        for dt in all_dates:
            val = ts.get(dt, None)
            if val is None:
                new_val = None
            else:
                new_val = op(val, scalar)
            new_ts[dt] = new_val
        return new_ts
    
    def add(self, ts_or_scalar):
        op = 'add'
        result = self._ts_or_scalar_op(ts_or_scalar, op)
        return result
    
    def sub(self, ts_or_scalar):
        op = 'sub'
        result = self._ts_or_scalar_op(ts_or_scalar, op)
        return result
    
    def mult(self, ts_or_scalar):
        op = 'mul'
        result = self._ts_or_scalar_op(ts_or_scalar, op)
        return result
    
    def div(self, ts_or_scalar):
        op = 'div'
        result = self._ts_or_scalar_op(ts_or_scalar, op)
        return result
    
    def _ts_or_scalar_op(self, ts_or_scalar, op):
        if isinstance(ts_or_scalar, TimeSeries):
            new_ts = self._ts_op(ts_or_scalar, op)
        else:
            new_ts = self._scalar_op(ts_or_scalar, op)
        return new_ts
        
    def delta(self, lag=1, ):
        '''
        lag can be a number, start, or end
        if start it is the difference from the start  
        if end it is the difference from the end 
        should return a copy of the time series
        '''
        lag_choices = ('start', 'end')
        if not (isinstance(lag, int) or lag in lag_choices):
            msg = "Lag %s is not supported. Supply integer or one of %s"
            raise ValueError(msg %(lag, lag_choices))
                
        ts = self.ts
        new_ts = ts.copy()
        
        cur_series = ts.items()
        if not cur_series:
            return new_ts
        
        if isinstance(lag, int):
            if lag > len(cur_series):
                return new_ts
            else:
                start_ts = self.lead(k = lag)
                new_ts = ts - start_ts
        else:
            if lag=='start':
                base_val = cur_series[0][1]
                for dt, val in cur_series:
                    new_val = val - base_val
                    new_ts[dt] = new_val
            elif lag=='end':
                base_val = cur_series[-1][1]
                for dt, val in cur_series:
                    new_val = val - base_val
                    new_ts[dt] = new_val
            else:
                raise ValueError("This should never happen")
        return new_ts
    
    def lag(self, k = 1):
        '''
        Moves data back by k dates
        '''
        if k < 1:
            return self.lead(-1 * k)
        assert k > 0
        ts = self.ts
        new_ts = ts.copy()
        
        cur_series = ts.items()
        if not cur_series:
            return new_ts
        
        if isinstance(k, int):
            if k > len(cur_series):
                return new_ts
            else:
                rng = range(k, len(cur_series))
                for r in rng:
                    cur_dt, cur_val = cur_series[r]
                    prev_dt, prev_val = cur_series[r-k]
                    new_ts[prev_dt] = cur_val
        return new_ts
    
    def lead(self, k = 1):
        '''
        Moves data forward by k dates
        '''
        if k < 0:
            return self.lag(-1 * k)
        if k == 0:
            new_ts = ts.copy()
            for dt, val in new_ts.items():
                new_ts[dt] = val
            return new_ts 
        assert k > 0
        ts = self.ts
        new_ts = ts.copy()
        
        cur_series = ts.items()
        if not cur_series:
            return new_ts
        
        if isinstance(k, int):
            if k > len(cur_series):
                return new_ts
            else:
                rng = range(k, len(cur_series))
                for r in rng:
                    cur_dt, cur_val = cur_series[r]
                    prev_dt, prev_val = cur_series[r-k]
                    new_ts[cur_dt] = prev_val
        return new_ts
    
    def na_omit(self):
        ts = self.ts
        new_ts = ts.copy()
        for dt, val in ts.items():
            if not val is None:
                new_ts[dt] = val
        return new_ts
        
class TimeSeries(object):
    
    def __init__(self, ts=None, **props):
        self.properties = Properties()
        for ky , val in props.items():
            self.properties.add(ky, val)
            
        self.analytics = Analytics(self)
        self._kys = []
        self._vals = []
        
        self._dt_indexing = None
        if ts:
            for k, v in ts:
                self[k] = v
    
    def _convert_dt(self, dt):
        dt_indxing = self._dt_indexing
        if type(dt) in (datetime.date, datetime.datetime):
            if dt_indxing is None:
                self._dt_indexing = True
            elif dt_indxing == False:
                raise ValueError("This timeseries can not handle date indexing")
            val = dt
            #val = (dt - epoch).days
        else:
            if dt_indxing is None:
                self._dt_indexing = False
            elif dt_indxing == True:
                raise ValueError("This timeseries expects date indexing")
            val = dt
        return val
    
    def get(self, ky, dflt = None):
        if ky in self.keys():
            result = self[ky]
        else:
            result = dflt
        return result
    
    def keys(self):
        kys = list(self._kys)
        return kys
    
    def values(self):
        vals = list(self._vals)
        return vals
    
    def items(self):
        kys = self.keys()
        vals = self.values()
        rt = zip(kys, vals)
        return rt
    
    def copy(self):
        Klass = self.__class__
        new_ts = Klass()
        current_properties = self.properties.all()
        for name, val in current_properties.items():
            new_ts.properties.add(name, val)
        return new_ts
    
    def _getslice(self, slice):
        kys = self._kys
        vals = self._vals
        
        start = slice.start or 0
        stop = slice.stop or len(kys)
        s_ky = self._convert_dt(start)
        e_ky = self._convert_dt(stop)
        s_indx = kys.index(s_ky)
        e_indx =  kys.index(e_ky)
        
        ky_seg = kys[s_indx:e_indx]
        val_seg = vals[s_indx:e_indx]
        
        new_ts = self.copy()
        for ky, val in zip(ky_seg, val_seg):
            new_ts[ky] = val
        return new_ts
    
    def __getitem__(self, key_or_slice):
        kys = self._kys
        vals = self._vals
        
        is_slice = hasattr(key_or_slice, 'start')
        if is_slice:
            new_ts = self._getslice(key_or_slice)
            return new_ts
        else:
            ckey = self._convert_dt(key_or_slice)
            indx = kys.index(ckey)    
            val = vals[indx]
            return val
        
    def _greater_indx(self, key):
        '''
        returns the index that is just greater than the current key
        '''
        kys = self._kys
        if not kys:
            return 0
        
        for indx, comp_ky in enumerate(kys):
            if comp_ky > key:
                return indx
        return indx + 1
        
    def __setitem__(self, key, item):
        ckey = self._convert_dt(key) 
        indx = self._greater_indx(ckey)
        kys = self._kys
        kys.insert(indx, ckey)
        
        vals = self._vals
        vals.insert(indx, item)
    
    def __contains__(self, item):
        key = self._convert_dt(item)
        kys = self._kys
        rt = key in kys
        return rt
    
    def __add__(self, item):
        ts = self.analytics.add(item)
        return ts
    
    def __sub__(self, item):
        ts = self.analytics.sub(item)
        return ts
    
    def __mul__(self, item):
        ts = self.analytics.mult(item)
        return ts
    
    def __div__(self, item):
        ts = self.analytics.div(item)
        return ts
     
    
        