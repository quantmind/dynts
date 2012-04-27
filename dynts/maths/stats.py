from numpy import array

from dynts.utils.py2py3 import range


class statistics(object):
    '''Perform statistics on already aggregated samples.
    
.. attribute: n
    
    The sample size

.. attribute: sx

    An array
    
.. attribute: sxx
 
''' 
    def __init__(self, n, sx, sxx):
        self.n = n
        self.sx = sx
        self.sxx = sxx
        
    def cov(self):
        '''The covariance matrix'''
        rows = []
        m = 0
        sxx = self.sxx
        for n in range(0, self.n):
            m = n*(n+1)//2
            rows.append(sxx[m:m+n+1])
        return array(rows)
            
        cov = ndarraya