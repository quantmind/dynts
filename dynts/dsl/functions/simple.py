from dynts.dsl import FunctionBase
from dynts import TimeSeries, tsfunctions


class ScalarFunction(FunctionBase):
    abstract = True
    def __call__(self, args, window = 20, **kwargs):
        result = []
        for arg in args:
            name = '%s(%s,window=%s)' % (self.name,arg,window)
            ts = self.apply(arg, window = window, name = name, **kwargs)
            result.append(ts)
        if result:
            return result if len(result)>1 else result[0]
        

class Log(ScalarFunction):
    """\
Calculate the natural logarithm of a timeseries. It applies to each
value and return a timeseries with exactly the same dimensions.
"""
    def apply(self, ts, **kwargs):
        return ts.log(**kwargs)
    

class Sqrt(ScalarFunction):
    """\
Calculate the square root of a timeseries. It applies to each
value and return a timeseries with exactly the same dimensions.
"""
    def apply(self, ts, **kwargs):
        return ts.sqrt(**kwargs)
    
    
class Square(ScalarFunction):
    """\
Calculate the square of a timeseries. It applies to each
value and return a timeseries with exactly the same dimensions.
"""
    def apply(self, ts, **kwargs):
        return ts.square(**kwargs)
    
    
class Delta(ScalarFunction):
    """\
It evaluates the first order difference evaluated as

.. math::

    \\Delta y_t = y_t - y_{t-lag}

Typical usage::

    delta(tiker)
    delta(tiker,lag=5)
    
:parameter lag: backward lag. Default ``1``.
"""
    def apply(self, ts, **kwargs):
        return ts.delta(**kwargs)
    
    
class Delta2(ScalarFunction):
    """\   
Second order difference evaluated as

.. math::

    \\Delta_{\\tt lag}^2 y_t &= \\Delta_{\\tt lag} \\left( \\Delta_{\\tt lag} y_t \\right)\\\\
                             &= y_t - 2 y_{t-{\\tt lag}} + y_{t-2{\\tt lag}}

Typical usage::

    delta2(tiker)
    delta2(tiker,lag=5)
    
It is an optimised shortcut function equivalent to::

    delta(delta(tiker))
    delta(delta(tiker,lag=5),lag=5)

:parameter lag: backward lag. Default ``1``.
"""
    def apply(self, ts, **kwargs):
        return ts.delta2(**kwargs)
    
    
class LDelta(ScalarFunction):
    """\
Calculate the log-delta of a timeseries. This is the first order difference
in log-space useful for evaluationg percentage moments
    
.. math::

    {\\tt ldelta} (y, lag=1) = \\log{\\frac{y_t}{y_{t-{\\tt lag}}}}   

Typical usage::

    ldelta(tiker)
    ldelta(tiker,lag=5)
    
:parameter lag: backward lag. Default ``1``.
"""
    def apply(self, ts, **kwargs):
        return ts.logdelta(**kwargs)


class Ma(ScalarFunction):
    """\
Arithmetic moving average function.
"""
    def apply(self, ts, **kwargs):
        return ts.rollmean(**kwargs)
    
    
class Max(ScalarFunction):
    """\
Moving max function.
"""
    def apply(self, ts, **kwargs):
        return ts.rollmax(**kwargs)


class Med(ScalarFunction):
    """\
Moving median function.
"""
    def apply(self, ts, **kwargs):
        return ts.rollmedian(**kwargs)    
    
    
class Min(ScalarFunction):
    """\
Moving min function.
"""
    def apply(self, ts, **kwargs):
        return ts.rollmin(**kwargs)
    
    
class zscore(ScalarFunction):
    """\
Rolling Z-Score function:

.. math::

    zs = \frac{x_n - x_{n-w}}{\sigma_n}
    
"""
    def apply(self, ts, **kwargs):
        return tsfunctions.zscore(ts, **kwargs)
    

class prange(ScalarFunction):
    """\
Rolling Percentage range function.
"""
    def apply(self, ts, **kwargs):
        return tsfunctions.prange(ts, **kwargs)
    


class SD(ScalarFunction):
    '''\
Rolling standard deviation as given by:

.. math::

    {\\tt sd}(y_t) = \\sqrt{\\sum_{i=0}^{w-1} (\\Delta y_{t-i})^2}
    
Typical usage::

    stdev(tiker)
    stdev(tiker,window=40)
    
    
:parameter window: the rolling window in units. Default ``20``.
'''
    def apply(self, ts, **kwargs):
        return ts.rollsd(**kwargs)
    

class Avol(ScalarFunction):
    '''\
Annualised volatility.
'''
    def apply(self, ts, **kwargs):
        return ts.rollavol(**kwargs)
    
    
class reg(FunctionBase):
    """\
Calculate the **linear regression** of one series with respect
to one or more series. For example::

    regr(GOOG,YHOO)
    
will calculate

.. math::

    y_i = b x_i + a
    
There are two optional parameters:

* *alpha* default is ``1``. If set to zero alpha won't be included in the regression.
"""        
    name = 'regr'
    
    def __call__(self, input, **kwargs):
        pass
        
    