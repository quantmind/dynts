from dynts import test
from dynts.lib import makeskiplist
from dynts.utils.populate import populate


class CythonSkiplistInsert(test.BenchMark):
    size   = 10000
    number = 10
    
    def setUp(self):
        self.data = populate(size = self.size)
        
    def __str__(self):
        return '%s (%s elements, %s times)' % (self.__class__.__name__,self.size,self.number)
    
    def run(self):
        makeskiplist(data = self.data)
        

class CythonSkiplistIteration(CythonSkiplistInsert):
    
    def setUp(self):
        self.data = makeskiplist(data = populate(size = self.size))
        
    def run(self):
        for i in self.data:
            pass

        
class SkiplistInsert(CythonSkiplistInsert):
    
    def run(self):
        makeskiplist(data = self.data, use_fallback = True)
        

class SkiplistIteration(CythonSkiplistIteration):
    
    def setUp(self):
        self.data = makeskiplist(data = populate(size = self.size), use_fallback = True)
    
     