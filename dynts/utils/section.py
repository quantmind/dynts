from itertools import izip

crossoperator = lambda func,*args : [func(*vals) for vals in izip(*args)]

__all__ = ['cross']


class cross(object):
    '''Cross section wrapper class'''
    min = lambda *args : crossoperator(min,*args)
    max = lambda *args : crossoperator(max,*args)

    def __init__(self, elem):
        self.elem = elem
    
    def __iter__(self):
        return iter(self.elem)
    
    def __eq__(self, other):
        return reduce(lambda x,y : x and y[0] == y[1], izip(self.elem,other), True)
    
    def __ge__(self, other):
        return reduce(lambda x,y : x and y[0] >= y[1], izip(self.elem,other), True)
    
    def __le__(self, other):
        return reduce(lambda x,y : x and y[0] <= y[1], izip(self.elem,other), True)
    