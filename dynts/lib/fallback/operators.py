from collections import deque
from itertools import islice

from .common import *


from skiplist import skiplist

__all__ = ['roll_max',
           'roll_min',
           'roll_median']


def roll_max(iterable, window, skiplist_class = skiplist):
    return rollingOperation(iterable, window, smax,
                            skiplist_class = skiplist)


def roll_min(iterable, window, skiplist_class = skiplist):
    return rollingOperation(iterable, window, smin,
                            skiplist_class = skiplist)


def roll_median(iterable, window, skiplist_class = skiplist):
    return rollingOperation(iterable, window, smedian,
                            skiplist_class = skiplist)


def smax(olist,nobs):
    if nobs:
        return olist[nobs-1]
    else:
        return NaN


def smin(olist,nobs):
    if nobs:
        return olist[0]
    else:
        return NaN


def smedian(olist,nobs):
    if nobs:
        midpoint = nobs // 2
        return olist[midpoint]
    else:
        return NaN


def smean(olist,missing):
    if olist:
        mean = sum(olist) / len(olist)
        return mean
    else:
        return missing


def rollingOperation(iterable, window, op, skiplist_class = skiplist):
    it = iter(iterable)
    queue = deque(islice(it, window))
    ol    = skiplist_class(window)
    nobs  = 0
    for elem in queue:
        if elem == elem:
            nobs += 1
            ol.insert(elem)
    yield op(ol,nobs)
    for newelem in it:
        oldelem = queue.popleft()
        if oldelem == oldelem:
            nobs -= 1
            ol.remove(oldelem)
        queue.append(newelem)
        if newelem == newelem:
            nobs += 1
            ol.insert(newelem)
        yield op(ol,nobs)

