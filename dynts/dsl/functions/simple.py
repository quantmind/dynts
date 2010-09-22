from dynts.dsl import FunctionBase
from dynts import TimeSeries


class Delta(FunctionBase):
    def __call__(self, data, step = 1):
        pass
    
class Log(FunctionBase):
    def __call__(self, data, step = 1):
        for k,v in data:
            yield k,log(v)

class ScalarFunction(FunctionBase):
    abstract = True
    def __call__(self, args, window = 20, **kwargs):
        result = []
        for arg in args:
            ts = self.apply(arg, window = window, **kwargs)
            result.append(ts)
        if result:
            return result if len(result)>1 else result[0]

class Mean(ScalarFunction):
    """Moving average function"""
    def apply(self, ts, **kwargs):
        return ts.rollmean(**kwargs)
    
    
class Max(ScalarFunction):
    """Moving average function"""
    def apply(self, ts, **kwargs):
        return ts.rollmax(**kwargs)
    
    
class Min(ScalarFunction):
    """Moving average function"""
    def apply(self, ts, **kwargs):
        return ts.rollmin(**kwargs)
    
    
class Avol(ScalarFunction):
    '''Annualised volatility'''
    def apply(self, ts, **kwargs):
        return ts.rollavol(**kwargs)
    
    
class Regression(FunctionBase):
    """Calculate the **linear regression** of one series with respect
to one or more series. For example::

    regr(GOOG,YHOO)
    
will calculate

.. math::

    y_i = \beta x_i + \alpha
    
There are two optional parameters:

* *alpha* default is ``1``. If set to zero alpha won't be included in the regression."""        
    name = 'regr'
    
    def __call__(self, input, **kwargs):
        pass
        
    