'''General timeseries function'''


def better_ts_function(f):
    '''Decorator which check if timeseries has a better implementation of the function'''
    fname = f.__name__
    
    def _(ts, *args, **kwargs):
        func = getattr(ts,fname,None)
        if func:
            return func(*args, **kwargs)
        else:
            return f(ts, *args, **kwargs)
    
    _.__name__ = fname
    
    return _ 


@better_ts_function
def zscore(ts, **kwargs):
    '''Rolling Z-Score statistics. The Z-score is more formally known as
``standardised residuals``. To calculate the standardised residuals of a data set,
the average value and the standard deviation of the data value have to be estimated.

.. math::

    z = \frac{x - \mu(x)}{\sigma(x)}
'''
    m = ts.rollmean(**kwargs)
    s = ts.rollstddev(**kwargs)
    result = (ts - m)/s
    name = kwargs.get('name', None)
    if name:
        result.name = name
    return result


@better_ts_function
def prange(ts, **kwargs):
    '''Rolling Percentage range. Value between 0 and 1 indicating the position in the rolling range.'''
    mi = ts.rollmin(**kwargs)
    ma = ts.rollmax(**kwargs)
    return (ts - mi)/(ma - mi)