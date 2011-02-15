from datetime import date, timedelta
from random import uniform, randint

from numpy import ndarray

from .py2py3 import range

def_converter = lambda x: x
def_generator = lambda x : uniform(0,1)

__all__ = ['datepopulate',
           'populate',
           'randomts',
           'randomwalk',
           'polygen']

class gdata(object):
    
    def __init__(self, data):
        self.data = data
        
    def __iter__(self):
        return (v for v in self.data)
        

def datepopulate(size = 10, start = None, delta = 1):
    dt = start or date.today() - timedelta(days = delta*(size-1))
    td = timedelta(days=delta)
    return [dt+s*td for s in range(size)]
        
def populate(size = 100, cols = 1, generator = None):
    generator = generator or def_generator
    data = ndarray([size,cols])
    for c in xrange(0,cols):
        data[:,c] = [generator(i) for i in xrange(0,size)]
    return data


def randomts(size = 100, cols = 1, start = None, delta = 1,
             generator = None, backend=None, name='randomts'):
    from dynts import timeseries
    dates = datepopulate(size,start=start,delta=delta)
    data  = populate(size,cols=cols,generator=generator)
    return timeseries(name=name,backend=backend,date=dates,data=data)


def polygen(*coefficients):
    '''Polynomial generating function'''
    if not coefficients:
        return lambda i : 0
    else:
        c0 = coefficients[0]
        coefficients = coefficients[1:]
        def _(i):
            v = c0
            for c in coefficients:
                v += c*i
                i *= i
            return v
        return _


def randomwalk(size = 100, cols = 1, start = None, delta = 1,
               backend=None, name='randomwalk', sigma = 1.0, mu = 1.0):
    '''Create a random walk timeseries'''
    pass

    