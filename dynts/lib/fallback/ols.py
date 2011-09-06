from numpy import dot, linalg


class ols(object):
    '''The ordinary least squares (OLS) or linear least squares is a method
for estimating the unknown parameters in a linear regression model.

The matrix formulation of OLS is given by the linear system of equations:

.. math::

    y = X \beta + \epsilon
    
    
.. attribute:: y

    The *regressand* also known as the the *endogenous* or *dependent* variable.
    This is a n-dimensional vector.
    
.. attribute:: x

    The *regressor* also known as the *exogenous* or *independent* variable
    This is a :math:`n \times k` matrix, where each column of which is a
    n-dimensional vector which must be linearly independent from the others.
'''
    def __init__(self, y, X):
        self.y = y
        self.X = X
        
    def beta(self):
        '''\
The linear estimation of the parameter vector :math:`\beta` given by

.. math::

    \beta = (X^T X)^-1 X^T y
        
'''
        t = self.X.transpose()
        XX = dot(t,self.X)
        XY = dot(t,self.y)
        return linalg.solve(XX,XY)
    
    
    