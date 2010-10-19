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


def binOp(op, indx, amap, bmap, handle_missing):
    '''
    Combines the values from two map objects using the indx values
    using the op operator. In situations where there is a missing value
    it will use the callable function handle_missing
    '''
    def op_or_missing(id):
        va = amap.get(id, None)
        vb = bmap.get(id, None)
        if va is None or vb is None:
            result = handle_missing() #This should create as many elements as the number of columns!?
        else:
            try:
                result = op(va, vb)
            except Exception, e:
                result = None
            if result == None:
                result = handle_missing()
            return result
    seq_arys = map(op_or_missing, indx)
    data = np.vstack(seq_arys)
    return data


def applyfn(op, v1, v2, handle_missing):
    def op_or_missing(a,b):
        try:
            result = op(a,b)
        except Exception, e:
            result = None
        if result is None:
                result = handle_missing()
        return result
    if len(v1) != len(v2):
        msg = "Vectors %s, %s are different lengths %s, %s" %(v1, v2, len(v1),
                len(v2))
        raise ValueError(msg)
    rt = map(op_or_missing, v1, v2)
    return rt


def _combine_dts(dts1, dts2, all):
    if all:
        all_dts = set(dts1).union(set(dts2))
    else:
        all_dts = set(dts1).intersection(set(dts2))

    result = list(all_dts)
    result.sort()
    return result

def _toVec(shape, val):
    '''
    takes a single value and creates a vecotor / matrix with that value filled
    in it
    '''
    mat = np.empty(shape)
    mat.fill(val)
    return mat

def _handle_scalar(op, ts, scalar, fill_fn):
    values = ts.values()
    shape = values.shape
    v2 = _toVec(shape, scalar)
    dts = ts.dates()
    result = applyfn(op, values, v2, fill_fn)
    return dts, result

def _handle_ts(op, ts, ts2, all, fill_fn):
    dts1 = ts.dates()
    dts2 = ts2.dates()
    indx = _combine_dts(dts1, dts2, all)
    tsMap = ts.asbtree()
    ts2Map = ts2.asbtree()
    result = binOp(op, indx, tsMap, ts2Map, fill_fn)
    return indx, result

def _handle_ts_or_scalar(op_name, ts, ts_or_scalar, all = True, fill = None):
    from dynts import istimeseries
    op = _get_op(op_name)
    fill = fill if fill is not None else settings.missing_value
    if callable(fill):
        fill_fn = fill
    else:
        fill_fn = lambda : fill

    if istimeseries(ts_or_scalar):
        dts, data = _handle_ts(op, ts, ts_or_scalar, all, fill_fn)
    else:
        dts, data = _handle_scalar(op, ts, ts_or_scalar, fill_fn)
    return ts.clone(date = dts, data = data)

def ts_fn(op_name):
    fn = lambda  *args,  **kwargs : _handle_ts_or_scalar(op_name, *args, **kwargs)
    return fn

add = ts_fn('add')
sub = ts_fn('sub')
mul = ts_fn('mul')
div = ts_fn('div')

