import numpy as np

from ..exc import ExpressionError


_ops = {
    'add': lambda x, y: x+y,
    'sub': lambda x, y: x-y,
    'mul': lambda x, y: x*y,
    'div': lambda x, y: x/y,
}


def op_get(op_name):
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
            # This should create as many elements as the number of columns!?
            result = fill_vec
        else:
            try:
                result = op(va, vb)
            except Exception:
                result = None
            if result is None:
                result = fill_vec
            return result
    seq_arys = map(op_or_missing, indx)
    data = np.vstack(seq_arys)
    return data


def applyfn(op, v1, v2, fill_vec):
    def op_or_missing(a, b):
        try:
            result = op(a, b)
        except Exception:
            result = None
        if result is None:
                result = fill_vec
        return result
    if len(v1) != len(v2):
        msg = "Vectors %s, %s are different lengths %s, %s" % (
            v1, v2, len(v1), len(v2)
        )
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


def op_scalar_ts(op_name, op, scalar, ts, fill_fn):
    fill_vec = _create_fill_vec(ts, fill_fn)
    values = ts.values()
    shape = values.shape
    v2 = _toVec(shape, scalar)

    dts = ts.dates()
    result = applyfn(op, v2, values, fill_vec)
    return dts, result


def op_ts_scalar(op_name, op, ts, scalar, fill_fn):
    values = ts.values()
    if values is not None:
        fill_vec = _create_fill_vec(ts, fill_fn)
        shape = values.shape
        v2 = _toVec(shape, scalar)
        dts = ts.dates()
        result = applyfn(op, values, v2, fill_vec)
        return dts, result
    else:
        return None, None


def op_ts_ts(op_name, op, ts, ts2, all, fill_fn):
    if ts.count() != ts2.count():
        raise ExpressionError(
            "Cannot %s two timeseries with different number of series."
            % op_name
        )
    dts1 = set(ts.dates())
    if all:
        indx = dts1.union(ts2.dates())
    else:
        indx = dts1.intersection(ts2.dates())
    hash = ts.ashash()
    hash2 = ts2.ashash()

    fill = _create_fill_vec(ts, fill_fn)
    # fill = np.array([fill_fn()])
    for dt in indx:
        v = hash.get(dt, None)
        v2 = hash2.get(dt, None)
        if v is None or v2 is None:
            v = fill
        else:
            v = op(v, v2)
        hash[dt] = v
    new_ts = hash.getts()
    rt = zip(*new_ts.items())
    return rt
