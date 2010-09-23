from datetime import date, timedelta
from random import uniform, randint
import numpy as ny

def_converter = lambda x: x
def_generator = lambda x : uniform(0,1)

__all__ = ['datepopulate','populate','randomts',
           'randomwalk']

class gdata(object):
    
    def __init__(self, data):
        self.data = data
        
    def __iter__(self):
        return (v for v in self.data)
        

def datepopulate(size = 10, start = None, delta = 1):
    dt = start or date.today() - timedelta(days = delta*(size-1))
    td = timedelta(days=delta)
    data = []
    s  = 0
    while s < size:
        data.append(dt)
        dt += td
        s  += 1
    return gdata(data)
        
def populate(size = 10, cols = 1, generator = None):
    generator = generator or def_generator
    data = ny.ndarray([size,cols])
    for c in xrange(0,cols):
        data[:,c] = [generator(i) for i in xrange(0,size)]
    return data


def randomts(size = 100, cols = 1, start = None, delta = 1,
             generator = None, backend=None, name='randomts'):
    from dynts import timeseries
    dates = datepopulate(size,start=start,delta=delta)
    data  = populate(size,cols=cols,generator=generator)
    return timeseries(name=name,backend=backend,date=dates,data=data)

def randomwalk(size = 100, cols = 1, start = None, delta = 1,
               backend=None, name='randomwalk', sigma = 0.1, mu = 0.0):
    '''Create a random walk timeseries'''
    pass

    