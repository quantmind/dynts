'''
This is just a landing zone for working on possible functionality that can be moved into the base timeseries class
'''

from zoo import TimeSeries
import operators

class TSWithOperators(TimeSeries):
    
    __add__ = operators.add
    __sub__ = operators.sub
    __mul__ = operators.mul
    __div__ = operators.div

#import datetime
#import operator

#class Analytics(object):
#    ops = {}
#
#    def __init__(self, ts):
#        self.ts = ts
#
#    def add_op(self, name, op):
#        '''
#        Add a new analytic operation
#        '''
#        ops = self.ops
#        ops[name] = op
#
#    def get_op(self, name):
#        ops = self.ops
#        op = ops.get(name, None)
#        if op is None:
#            op = getattr(operator, name, None)
#            if op is None:
#                msg = "No operation named %s. Choices are %s"
#                raise ValueError(msg %(name, ops))
#            else:
#                ops[name] = op
#        return op
#
#    def _ts_op(self, other_ts, op_name):
#        op = self.get_op(op_name)
#        ts = self.ts
#        all_dates = set(ts.keys()).union(set(other_ts.keys()))
#        new_ts = ts.copy()
#        new_ts.properties.merge(other_ts.properties.all())
#        for dt in all_dates:
#            val = ts.get(dt, None)
#            val2 = other_ts.get(dt, None)
#            if not(val is None or val2 is None):
#                new_val = op(val, val2)
#            else:
#                new_val = None
#            new_ts[dt] = new_val
#        return new_ts
#
#    def _scalar_op(self, scalar, op_name):
#        op = self.get_op(op_name)
#        ts = self.ts
#        all_dates = ts.keys()
#        new_ts = ts.copy()
#        for dt in all_dates:
#            val = ts.get(dt, None)
#            if val is None:
#                new_val = None
#            else:
#                new_val = op(val, scalar)
#            new_ts[dt] = new_val
#        return new_ts
#
#    def add(self, ts_or_scalar):
#        op = 'add'
#        result = self._ts_or_scalar_op(ts_or_scalar, op)
#        return result
#
#    def sub(self, ts_or_scalar):
#        op = 'sub'
#        result = self._ts_or_scalar_op(ts_or_scalar, op)
#        return result
#
#    def mult(self, ts_or_scalar):
#        op = 'mul'
#        result = self._ts_or_scalar_op(ts_or_scalar, op)
#        return result
#
#    def div(self, ts_or_scalar):
#        op = 'div'
#        result = self._ts_or_scalar_op(ts_or_scalar, op)
#        return result
#
#    def _ts_or_scalar_op(self, ts_or_scalar, op):
#        if isinstance(ts_or_scalar, TimeSeries):
#            new_ts = self._ts_op(ts_or_scalar, op)
#        else:
#            new_ts = self._scalar_op(ts_or_scalar, op)
#        return new_ts
#
#    def na_omit(self):
#        ts = self.ts
#        new_ts = ts.copy()
#        for dt, val in ts.items():
#            if not val is None:
#                new_ts[dt] = val
#        return new_ts
#
#class devTimeSeries(TimeSeries):
#    '''
#    At the moment this inherits from the zoo timeseries as it
#    has most of the functionality implemented
#
#    At a later stage some of the functionality developed here can be 
#    included in the base TimeSeries object
#    '''
#
#    def __init__(self,**kwargs):
#        self.analytics = Analytics(self)
#
#    def get(self, ky, dflt = None):
#        if ky in self.keys():
#            result = self[ky]
#        else:
#            result = dflt
#        return result
#
#    def keys(self):
#        kys = list(self._kys)
#        return kys
#
#    def values(self):
#        vals = list(self._vals)
#        return vals
#
#    def items(self):
#        kys = self.keys()
#        vals = self.values()
#        rt = zip(kys, vals)
#        return rt
#
#    def _getslice(self, slice):
#        kys = self._kys
#        vals = self._vals
#
#        start = slice.start or 0
#        stop = slice.stop or len(kys)
#        s_ky = self._convert_dt(start)
#        e_ky = self._convert_dt(stop)
#        s_indx = kys.index(s_ky)
#        e_indx =  kys.index(e_ky)
#
#        ky_seg = kys[s_indx:e_indx]
#        val_seg = vals[s_indx:e_indx]
#
#        new_ts = self.copy()
#        for ky, val in zip(ky_seg, val_seg):
#            new_ts[ky] = val
#        return new_ts
#
#    def __getitem__(self, key_or_slice):
#        kys = self._kys
#        vals = self._vals
#
#        is_slice = hasattr(key_or_slice, 'start')
#        if is_slice:
#            new_ts = self._getslice(key_or_slice)
#            return new_ts
#        else:
#            ckey = self._convert_dt(key_or_slice)
#            indx = kys.index(ckey)
#            val = vals[indx]
#            return val
#
#    def __setitem__(self, key, item):
#        ckey = self._convert_dt(key)
#        indx = self._greater_indx(ckey)
#        kys = self._kys
#        kys.insert(indx, ckey)
#
#        vals = self._vals
#        vals.insert(indx, item)
#
#    def __contains__(self, item):
#        key = self._convert_dt(item)
#        kys = self._kys
#        rt = key in kys
#        return rt
#
#    def __add__(self, item):
#        ts = self.analytics.add(item)
#        return ts
#
#    def __sub__(self, item):
#        ts = self.analytics.sub(item)
#        return ts
#
#    def __mul__(self, item):
#        ts = self.analytics.mult(item)
#        return ts
#
#    def __div__(self, item):
#        ts = self.analytics.div(item)
#        return ts



