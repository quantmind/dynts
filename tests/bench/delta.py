from dynts import test
from dynts.utils.populate import randomts


class Zoo_Delta(test.BenchMark):
    backend = 'zoo'
    size    = 10000
    cols    = 5
    number  = 100
    
    def setUp(self):
        self.ts = randomts(self.size, self.cols, backend = self.backend)
        
    def __str__(self):
        t = (self.__class__.__name__,self.size,self.cols,self.number)
        return '%s (%sx%s elements, %s times)' % t
    
    def run(self):
        self.ts.delta()


class Zoo_Delta2(Zoo_Delta):
    
    def run(self):
        self.ts.delta2()
                
        
class Numpy_Delta(Zoo_Delta):
    backend = 'numpy'
    
    
class Numpy_Delta2(Zoo_Delta2):
    backend = 'numpy'
    
