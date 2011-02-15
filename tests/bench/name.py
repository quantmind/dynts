from dynts import test
try:
    from itertools import imap as map
except ImportError:
    pass


class namejoin(test.BenchMark):
    backend = 'zoo'
    size    = 10000
    number  = 10
    
    def setUp(self):
        self.ts = self.size*['test']
        
    def __str__(self):
        return '%s (%s elements, %s times)' % (self.__class__.__name__,self.size,self.number)
    
    def run(self):
        '__'.join(('{0}{1}'.format('sqrt',x) for x in self.ts))
        
        
class namemapreduce(test.BenchMark):
    backend = 'zoo'
    size    = 10000
    number  = 10
    
    def setUp(self):
        self.ts = self.size*['test']
        
    def __str__(self):
        return '%s (%s elements, %s times)' % (self.__class__.__name__,self.size,self.number)
    
    def run(self):
        return reduce(lambda x,y : x+'__'+y, map(lambda x : '{0}{1}'.format('sqrt',x), self.ts))
    