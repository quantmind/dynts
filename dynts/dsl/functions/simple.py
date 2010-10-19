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
    """Delta"""
    def apply(self, ts, **kwargs):
        return ts.log(**kwargs)
    
    
class Delta(ScalarFunction):
    """Delta"""
    def apply(self, ts, **kwargs):
        return ts.delta(**kwargs)
    
    
class LDelta(ScalarFunction):
    """Log-Delta. Can be used for calculating percentage moments."""
    def apply(self, ts, **kwargs):
        return ts.logdelta(**kwargs)


class Ma(ScalarFunction):
    """Moving average function"""
    def apply(self, ts, **kwargs):
        return ts.rollmean(**kwargs)
    
    
class Max(ScalarFunction):
    """Moving max function"""
    def apply(self, ts, **kwargs):
        return ts.rollmax(**kwargs)


class Med(ScalarFunction):
    """Moving median function"""
    def apply(self, ts, **kwargs):
        return ts.rollmedian(**kwargs)    
    
    
class Min(ScalarFunction):
    """Moving min function"""
    def apply(self, ts, **kwargs):
        return ts.rollmin(**kwargs)
    
    
class zscore(ScalarFunction):
    """Rolling Z-Score function"""
    def apply(self, ts, **kwargs):
        return tsfunctions.zscore(ts, **kwargs)
    

class prange(ScalarFunction):
    """Rolling Percentage range function"""
    def apply(self, ts, **kwargs):
        return tsfunctions.prange(ts, **kwargs)
    
    
    
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
        
    