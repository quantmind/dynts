from dynts import test
from dynts.utils.populate import randomts


class Zoo_Min(test.BenchMark):
    backend = 'zoo'
    size    = 10000
    number  = 10
    
    def setUp(self):
        self.ts = randomts(size = self.size, backend = self.backend)
        
    def __str__(self):
        return '%s (%s elements, %s times)' % (self.__class__.__name__,self.size,self.number)
    
    def run(self):
        self.ts.min()
    
    
class Zoo_RollingMin(Zoo_Min):
    window = 100
    
    def run(self):
        self.ts.rollmin(window = self.window)
        
        
        
class Numpy_Min(Zoo_Min):
    backend = 'numpy'
    
    
class Numpy_RollingMin(Zoo_RollingMin):
    backend = 'numpy'
    
    
