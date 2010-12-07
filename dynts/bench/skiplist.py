from dynts import test
from dynts.lib import makeskiplist
from dynts.utils import populate


class CythonSkiplistInsert(test.BenchMark):
    tags = ['skiplist']
    size   = 5000
    number = 10
    
    def setUp(self):
        self.data = populate(size = self.size)
        
    def __str__(self):
        return '%s (%s * %s)' % (self.__class__.__name__,self.size,self.number)
    
    def run(self):
        makeskiplist(data = self.data)