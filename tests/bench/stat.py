#
#Test for speed in variance calculation
#
import numpy as np
from dynts import test
from dynts.utils.populate import randomts, populate

def var1(X,ddof=0):
    sx,sx2 = reduce(lambda x,y: (x[0]+y[0],x[1]+y[1]), ((x,x*x) for x in X))
    N = len(X)
    return (sx2-sx*sx/N)/(N - ddof)


def var2(X,ddof=0):
    N = len(X)
    return (sum(X*X) - sum(X)**2/N)/(N - ddof)


class Variance1(test.BenchMark):
    size   = 10000
    number = 10
    
    def setUp(self):
        self.X = populate(self.size,1)[:,0]
    
    def __str__(self):
        t = (self.__class__.__name__,self.size,self.number)
        return '{0} ({1} elements, {2} times)'.format(t)
    
    def run(self):
        var1(self.X)
        

class Variance2(Variance1):
        
    def run(self):
        var2(self.X)


if __name__ == '__main__':
    X = np.array([1.*x for x in range(1,101)])
    print(var(X))