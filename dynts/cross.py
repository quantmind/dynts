from itertools import izip
from dynts.backends.operators import crossection


min = crossection.cmin
max = crossection.cmax



class section(object):
    
    def __init__(self, elem):
        self.elem = elem
    
    def allge(self, other):
        return reduce(lambda x,y : x and y[0] >= y[1], izip(self.elem,other), True)
    
    def allle(self, other):
        return reduce(lambda x,y : x and y[0] <= y[1], izip(self.elem,other), True)