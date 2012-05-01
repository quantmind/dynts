from numpy import array, ndarray, sqrt, outer

from dynts.utils.py2py3 import range

__all__ = ['vector_to_symmetric', 'Variates'] 

def vector_to_symmetric(v):
    '''Convert an iterable into a symmetric matrix.'''
    np = len(v)
    N = (int(sqrt(1 + 8*np)) - 1)//2
    if N*(N+1)//2 != np:
        raise ValueError('Cannot convert vector to symmetric matrix')
    sym = ndarray((N,N))
    iterable = iter(v)
    for r in range(N):
        for c in range(r+1):
            sym[r,c] = sym[c,r] = iterable.next()
    return sym
  
def ttest(r, n):
    return r*sqrt((n-2)/(1 - r*r))
  
  
class Variates(object):
    '''Perform statistics on already aggregated samples.
    
.. attribute: n
    
    The sample size

.. attribute: sx

    An array obtained from sum_{n=1}^N x_n
    
.. attribute: sxx

    A symmetric matrix obtained obtained from sum_{n=1}^N x_n \times x_n^T
 
''' 
    def __init__(self, n, sx, sxx):
        self.n = n
        if n < 2:
            raise ValueError('Number of observation must be greater than 1')
        if not isinstance(sx, ndarray):
            sx = array(sx)
        self.sx = sx
        if not isinstance(sxx, ndarray) or len(sxx.shape) == 1:
            sxx = vector_to_symmetric(sxx)
        if len(self.sx.shape) > 1:
            raise TypeError('sx must be a one dimensional array')
        if self.length != sxx.shape[0] or self.length != sxx.shape[1]:
            raise ValueError('Inconsistent dimensions')
        self.sxx = sxx
    
    @property
    def length(self):
        return self.sx.shape[0]
    
    def cov(self, ddof=None, bias=0):
        '''The covariance matrix from the aggregate sample. It accepts an
optional parameter for the degree of freedoms.

:parameter ddof: If not ``None`` normalization is by (N - ddof), where N is
    the number of observations; this overrides the value implied by bias.
    The default value is None.'''
        N = self.n
        M = N if bias else N-1
        M = M if ddof is None else N-ddof 
        return (self.sxx - outer(self.sx,self.sx)/N)/M
    
    def corr(self):
        '''The correlation matrix'''
        cov = self.cov()
        N = cov.shape[0]
        corr = ndarray((N,N))
        for r in range(N):
            for c in range(r):
                corr[r,c] = corr[c,r] = cov[r,c]/sqrt(cov[r,r]*cov[c,c])
            corr[r,r] = 1.
        return corr
        
    def ttest(self, r, n=None):
        '''t-test of a correlation coefficient. Used to investigate whether
the difference between the sample correlation coefficient and zero is
statistically significant'''
        return ttest(r, n or self.n)