from bisect import bisect
from dynts.exceptions import *


class asdict(object):
    '''Wrap a :class:`dynts.TimeSeries` and
expose dictionary-like functionalities.'''
    def __init__(self, ts):
        self.ts = ts
        self.dates = list(ts.dates())
    
    def __getitem__(self, dt):
        v1 = bisect(self.dates,dt)
        return 0
        
    def find_ge(self, dt):
        '''Building block of all searches. Find the 
leftmost value greater or equal to *dt*. If dt is greater than the timeseries end date
a :class:`RightOutOfBound` exception will raise, otherwise it returns
the index.'''
        i = bisect_left(self.dates)
        if i != len(self.dates):
            return i
        raise RightOutOfBound

    def __len__(self):
        return len(self.dates)
    
    def __repr__(self):
        return '%s(%s)' % (self.__class___.__name__,self.ts.__repr__())
    
    def __str__(self):
        return '%s(%s)' % (self.__class___.__name__,self.ts)
    
    def range(self, start, end):
        s = self._sequence
        v1 = bisect(s,start)-1
        v2 = bisect(s,end)-1
        return self._sequence[v1:v2]

        