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

log
========

Calculate the natural logarithm of a timeseries. It applies to each
value and return a timeseries with exactly the same dimensions.

.. math::

    \log{(ts)}
"""
    def apply(self, ts, **kwargs):
        return ts.log(**kwargs)
    
    
class Delta(ScalarFunction):
    """\

delta
===========

First order difference evaluated as

.. math::

    \delta y_t = y_t - y_{t-1}

"""
    def apply(self, ts, **kwargs):
        return ts.delta(**kwargs)
    
    
class LDelta(ScalarFunction):
    """\

ldelta
============

Calculate the log-delta of a timeseries. This is the first order difference
in log-space useful for evaluationg percentage moments
    
.. math::

    {ldelta}(y_t) = \log \frac{y_t}{y_{t-1}}

"""
    def apply(self, ts, **kwargs):
        return ts.logdelta(**kwargs)


class Ma(ScalarFunction):
    """\

ma
=============

Arithmetic moving average function.
"""
    def apply(self, ts, **kwargs):
        return ts.rollmean(**kwargs)
    
    
class Max(ScalarFunction):
    """\

max
=============

Moving max function.
"""
    def apply(self, ts, **kwargs):
        return ts.rollmax(**kwargs)


class Med(ScalarFunction):
    """\
    
med
=============

Moving median function.
"""
    def apply(self, ts, **kwargs):
        return ts.rollmedian(**kwargs)    
    
    
class Min(ScalarFunction):
    """\

min
===========

Moving min function.
"""
    def apply(self, ts, **kwargs):
        return ts.rollmin(**kwargs)
    
    
class zscore(ScalarFunction):
    """\
    
zscore
=============

Rolling Z-Score function:

.. math::

    zs = \frac{x_n - x_{n-w}}{\sigma_n}
    
"""
    def apply(self, ts, **kwargs):
        return tsfunctions.zscore(ts, **kwargs)
    

class prange(ScalarFunction):
    """\
    
prange
=========

Rolling Percentage range function.
"""
    def apply(self, ts, **kwargs):
        return tsfunctions.prange(ts, **kwargs)
    
    
    
class Avol(ScalarFunction):
    '''\
    
avol
=======

Annualised volatility.
'''
    def apply(self, ts, **kwargs):
        return ts.rollavol(**kwargs)
    
    
class reg(FunctionBase):
    """\

regr
==========

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
        
    