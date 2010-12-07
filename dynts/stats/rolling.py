# Original from
# http://code.activestate.com/recipes/576930-efficient-running-median-using-an-indexable-skipli/
#
from random import random
from math import log, ceil
from collections import deque
from itertools import islice

from dynts.lib import skiplist

__all__ = ['rollingOperation']


def smax(olist,missing):
    if olist:
        return olist[len(olist)-1]
    else:
        return missing

def smin(olist,missing):
    if olist:
        return olist[0]
    else:
        return missing

def smedian(olist,missing):
    if olist:
        midpoint = len(olist) // 2
        return olist[midpoint]
    else:
        return missing

def smean(olist,missing):
    if olist:
        mean = sum(olist) / len(olist)
        return mean
    else:
        return missing


class rollingOperation(object):
    
    def __init__(self, iterable, window, skiplist_class = skiplist):
        from dynts.conf import settings
        self.iterable = iterable
        self.window = window
        self.missing = settings.missing_value
        self.ismissing = settings.ismissing
        self.skiplist = skiplist_class
        
    def mean(self):
        return self.rolling(smean)
    
    def min(self):
        return self.rolling(smin)
    
    def max(self):
        return self.rolling(smax)
    
    def median(self):
        return self.rolling(smedian)
    
    def rolling(self, op):
        'Fast rolling operation with O(log n) updates where n is the window size'
        missing   = self.missing
        ismissing = self.ismissing
        window = self.window
        it = iter(self.iterable)
        queue = deque(islice(it, window))
        ol    = self.skiplist(window)
        for elem in queue:
            if not ismissing(elem):
                ol.insert(elem)
        yield op(ol,missing)
        for newelem in it:
            oldelem = queue.popleft()
            if not ismissing(oldelem):
                ol.remove(oldelem)
            queue.append(newelem)
            if not ismissing(newelem):
                ol.insert(newelem)
            yield op(ol,missing)
