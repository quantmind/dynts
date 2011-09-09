#
# Defaults
from dynts.backends import TimeSeries


def simple_reduce(ts, size, align = 'right'):
    N = len(ts)
    n = int(N // size)
    while N/float(n) > size:
        n+=1
    if align == 'right':
        values = ts.values()[::-n][::-1]
        dates = ts.dates()[::-n][::-1]
    elif align == 'left':
        values = ts.values()[::n]
        dates = ts.dates()[::n]
    else:
        s = int(n // 2)
        values = ts.values()[s::n]
        dates = ts.dates()[s::n]
    return ts.clone(dates,values)


TimeSeries.register_algorithm('reduce','simple',simple_reduce)