import numpy as np

from dynts.conf import settings
from dynts.exceptions import ExpressionError

_ops = {'add' : lambda x,y : x+y,
        'sub' : lambda x,y : x-y,
        'mul' : lambda x,y : x*y,
        'div' : lambda x,y : x/y,
        }

def _get_op(op_name):
    global _ops
    op = _ops.get(op_name, None)
    if op is None:
        raise ExpressionError('There is no op called %s.' % op_name)
    return op


def binOp(op, indx, amap, bmap, fill_vec):
    '''
    Combines the values from two map objects using the indx values
    using the op operator. In situations where there is a missing value
    it will use the callable function handle_missing
    '''
    def op_or_missing(id):
        va = amap.get(id, None)
        vb = bmap.get(id, None)
        if va is None or vb is None:
            result = fill_vec #This should create as many elements as the number of columns!?
        else:
            try:
                result = op(va, vb)
            except Exception as e:
                result = None
            if result == None:
                result = fill_vec
            return result
    seq_arys = map(op_or_missing, indx)
    data = np.vstack(seq_arys)
    return data


def applyfn(op, v1, v2, fill_vec):
    def op_or_missing(a,b):
        try:
            result = op(a,b)
        except Exception as e:
            result = None
        if result is None:
                result = fill_vec
        return result
    if len(v1) != len(v2):
        msg = "Vectors %s, %s are different lengths %s, %s" %(v1, v2, len(v1),
                len(v2))
        raise ExpressionError(msg)
    rt = map(op_or_missing, v1, v2)
    return rt


def _toVec(shape, val):
    '''
    takes a single value and creates a vecotor / matrix with that value filled
    in it
    '''
    mat = np.empty(shape)
    mat.fill(val)
    return mat

def _create_fill_vec(ts, fill_fn):
    shape = (ts.count(),)
    fill = _toVec(shape, fill_fn())
    return fill

def _handle_scalar_ts(op_name, op, scalar, ts, fill_fn):
    fill_vec = _create_fill_vec(ts, fill_fn)
    values = ts.values()
    shape = values.shape
    v2 = _toVec(shape, scalar)
    
    dts = ts.dates()
    result = applyfn(op, v2, values, fill_vec)
    return dts, result

def _handle_ts_scalar(op_name, op, ts, scalar, fill_fn):
    fill_vec = _create_fill_vec(ts, fill_fn)
    values = ts.values()
    shape = values.shape
    v2 = _toVec(shape, scalar)
    dts = ts.dates()
    result = applyfn(op, values, v2, fill_vec)
    return dts, result

def _handle_ts_ts(op_name, op, ts, ts2, all, fill_fn):
    if ts.count() != ts2.count():
        raise ExpressionError("Cannot %s two timeseries with different number of series." % op_name)
    dts1 = set(ts.dates())
    if all:
        indx = dts1.union(ts2.dates())
    else:
        indx = dts1.intersection(ts2.dates())
    hash = ts.ashash()
    hash2 = ts2.ashash()
    
    fill = _create_fill_vec(ts, fill_fn)
    #fill = np.array([fill_fn()])
    for dt in indx:
        v  = hash.get(dt,None)
        v2 = hash2.get(dt,None)
        if v is None or v2 is None:
            v = fill
        else:
            v = op(v,v2)
        hash[dt] = v
    new_ts = hash.getts()
    rt = zip(*new_ts.items())
    return rt

def _handle_ts_or_scalar(op_name, ts1, ts2, all = True, fill = None, name = None):
    '''
    this is the main entry point for any arithmetic type function performed on a timeseries
    and/or a scalar. 
    op_name - name of the function to be performed
    ts1, ts2 - timeseries or scalars that the function is to performed over
    all - whether all dates should be included in the result
    fill - the value that should be used to represent "missing values"
    name - the name of the resulting time series
    '''
    from dynts import istimeseries
    op = _get_op(op_name)
    fill = fill if fill is not None else settings.missing_value
    if callable(fill):
        fill_fn = fill
    else:
        fill_fn = lambda : fill

    name = name or '%s(%s,%s)' % (op_name,ts1,ts2)
    ts = None
    if istimeseries(ts1):
        ts = ts1
        if istimeseries(ts2):
            dts, data =  _handle_ts_ts(op_name, op, ts1, ts2, all, fill_fn)
            
        else:
            dts, data = _handle_ts_scalar(op_name, op, ts1, ts2, fill_fn)
    else:
        if istimeseries(ts2):
            ts = ts2
            dts, data = _handle_scalar_ts(op_name, op, ts1, ts2, fill_fn)
        else:
            return op(ts1,ts2)
        
    return ts.clone(date = dts, data = data, name = name)

def ts_fn(op_name):
    fn = lambda  *args,  **kwargs : _handle_ts_or_scalar(op_name, *args, **kwargs)
    return fn

add = ts_fn('add')
sub = ts_fn('sub')
mul = ts_fn('mul')
div = ts_fn('div')
