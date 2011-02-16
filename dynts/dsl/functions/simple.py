from dynts.dsl import FunctionBase
from dynts import TimeSeries, tsfunctions


class ScalarFunction(FunctionBase):
    abstract = True
    def get_name(self, arg, window, **kwargs):
        return '%s(%s)' % (self.name,arg)
    
    def __call__(self, args, window = 20, **kwargs):
        result = []
        for arg in args:
            name = self.get_name(arg,window,**kwargs)
            ts = self.apply(arg, window = window, name = name, **kwargs)
            result.append(ts)
        if result:
            return result if len(result)>1 else result[0]
        

class ScalarWindowFunction(ScalarFunction):
    abstract = True
    def get_name(self, arg, window, **kwargs):
        return '%s(%s,window=%s)' % (self.name,arg,window)
        

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
First order differencing evaluated as

.. math::

    {\\tt delta}(y_t,{\\tt lag}) = y_t - y_{t-{\\tt lag}}

Typical usage::

    delta(tiker)
    delta(tiker,lag=5)
    
Or for calculating standard deviation on changes::

    sd(delta(tiker))
    
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
Calculate the logarithmic difference of a timeseries.
This is the first order difference
in log-space useful for evaluating percentage moments:
    
.. math::

    {\\tt ldelta} (y_t, {\\tt lag}) = \\log{\\frac{y_t}{y_{t-{\\tt lag}}}}   

Typical usage::

    ldelta(tiker)
    ldelta(tiker,lag=5)
    
:parameter lag: backward lag. Default ``1``.
"""
    description = "log delta"
    def apply(self, ts, **kwargs):
        return ts.logdelta(**kwargs)


class Ma(ScalarWindowFunction):
    """\
Arithmetic moving average function simply defined by

.. math::

    {\\tt ma}(y_t,w) = \\frac{1}{w}\\sum_{i=0}^{w-1} y_{t-i}

:parameter window ``w``: the rolling window in units. Default ``20``
"""
    description = 'arithmetic moving avarage'
    def apply(self, ts, **kwargs):
        return ts.rollmean(**kwargs)
    
    
class Max(ScalarWindowFunction):
    """\
Moving max function.

.. math::

    {\\tt max}(y_t,w) = \\max\\left(w_t,\\dots,w_{t-w+1}\\right)

:parameter window ``w``: the rolling window in units. Default ``20``
"""
    def apply(self, ts, **kwargs):
        return ts.rollmax(**kwargs)


class Med(ScalarWindowFunction):
    """\
Moving median function.
"""
    def apply(self, ts, **kwargs):
        return ts.rollmedian(**kwargs)    
    
    
class Min(ScalarWindowFunction):
    """\
Moving min function.

.. math::

    {\\tt min}(y_t,w) = \\min\\left(w_t,\\dots,w_{t-w+1}\\right)

:parameter window ``w``: the rolling window in units. Default ``20``
"""
    def apply(self, ts, **kwargs):
        return ts.rollmin(**kwargs)    


class Var(ScalarWindowFunction):
    '''\
Rolling arithmetic average variance given by:

.. math::

    {\\tt var}(y_t,w,d) = \\frac{1}{w-d} \\sum_{i=0}^{w-1} \\left[y_{t-i} - {\\tt ma}(y_t,w)\\right]^2 
    
where :math:`\\tt ma` is the :ref:`rolling moving average <functions-ma>`.
Typical usage::

    var(tiker)
    var(tiker,window=40)

:parameter window ``w``: The rolling window in units. Default ``20``
:parameter ddof ``d``: Delta degree of freedom. Default ``0``
'''
    description = 'rolling variance'
    def apply(self, ts, **kwargs):
        return ts.rollsd(**kwargs)
    
    
class SD(ScalarWindowFunction):
    '''\
Rolling standard deviation given by:

.. math::

    {\\tt sd}(y_t,w) = \\sqrt{{\\tt scale} \cdot {\\tt var}(y_t,w)} 
    
where ``var`` is the rolling variance (not in docs yet).
Typical usage::

    sd(tiker)
    sd(tiker,window=40)
    sd(tiker, window=40, scale = 252)
    sd(ldelta(GOOG), window = 60, scale = 252)

:parameter window: the rolling window in units. Default ``20``
:parameter scale: Scaling constant. Default ``1``
'''
    def apply(self, ts, **kwargs):
        return ts.rollsd(**kwargs)
    

class Sharpe(ScalarWindowFunction):
    '''\
Rolling Annualised Sharpe Ratio given by:

.. math::

    {\\tt sharpe}(y_t,w) = \\frac{y_t-y_{t-w}}{{\\tt sd}({\\tt delta}(y_t),w)}
    
Typical usage::

    sharpe(tiker)
    sharpe(tiker,window=40)
    
:parameter window: the rolling window in units. Default ``20``.
'''
    def apply(self, ts, **kwargs):
        return ts.rollapply('sharpe',**kwargs)
    
    
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
    description = 'rolling linear regression'
    
    def __call__(self, input, **kwargs):
        pass
        