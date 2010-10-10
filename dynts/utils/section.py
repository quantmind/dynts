from itertools import izip

crossoperator = lambda func,*args : [func(*vals) for vals in izip(*args)]

scalarasiter = lambda x: x if hasattr(x,'__iter__') else [x] 


__all__ = ['cross','asarray','ascolumn','assimple',
           'scalarasiter']


def asarray(x):
    '''Convert ``x`` into a ``numpy.ndarray``.'''
    from numpy import array, ndarray
    iterable = scalarasiter(x)
    if isinstance(iterable,ndarray):
        return iterable
    else:
        if not hasattr(iterable,'__len__'):
            iterable = list(iterable)
        return array(iterable)


def ascolumn(x):
    '''Convert ``x`` into a ``column``-type ``numpy.ndarray``.'''
    x = asarray(x)
    return x if len(x.shape) >= 2 else x.reshape(len(x),1)

        
def assimple(x):
    if hasattr(x,'__iter__'):
        try:
            len(x)
        except:
            x = list(x)
        if len(x) == 1:
            return x[0]
        else:
            return x
    else:
        return x


class cross(object):
    '''Cross section wrapper class'''
    min = lambda *args : crossoperator(min,*args)
    max = lambda *args : crossoperator(max,*args)

    def __init__(self, elem):
        self.elem = asarray(elem)
    
    def __iter__(self):
        return iter(self.elem)
    
    def __eq__(self, other):
        return reduce(lambda x,y : x and y[0] == y[1], izip(self.elem,asarray(other)), True)
    
    def __ge__(self, other):
        return reduce(lambda x,y : x and y[0] >= y[1], izip(self.elem,asarray(other)), True)
    
    def __le__(self, other):
        return reduce(lambda x,y : x and y[0] <= y[1], izip(self.elem,asarray(other)), True)

    def __gt__(self, other):
        return not (self <= other)
    
    def __lt__(self, other):
        return not (self >= other)
    