from collections import namedtuple
from numpy import array


basestats = namedtuple('basestats','min max mean std')


def base_stats(x,y):
    if not y:
        return basestats(x,x,x,x*x)
    else:
        return basestats(min(y,x.min),
                         max(y,x.max),
                         y+x.mean,
                         y*y+y.std)
    
    
def base_stats(data):
    v = reduct(_base_stats,data)
    return v