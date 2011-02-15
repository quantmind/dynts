import numpy as np
from collections import deque
from itertools import islice

from .common import *


from skiplist import skiplist

__all__ = ['roll_max',
           'roll_min',
           'roll_median',
           'roll_mean',
           'roll_sd',
           'roll_sharpe',
           'rollingOperation']


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
    '''Generalised media for odd and even number of samples'''
    if nobs:
        rem = nobs % 2
        midpoint = nobs // 2
        me = olist[midpoint]
        if not rem:
            me = 0.5 * (me + olist[midpoint-1])
        return me
    else:
        return NaN


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


def roll_mean(input, window):
    '''Apply a rolling mean function to an array.
This is a simple rolling aggregation.'''
    nobs, i, j, sum_x = 0,0,0,0.
    N = len(input)

    if window > N:
        raise ValueError('Out of bound')
    
    output = np.ndarray(N-window+1,dtype=input.dtype)
    
    for val in input[:window]:
        if val == val:
            nobs += 1
            sum_x += val
        
    output[j] = NaN if not nobs else sum_x / nobs
    
    for val in input[window:]:
        prev = input[j]
        if prev == prev:
            sum_x -= prev
            nobs -= 1

        if val == val:
            nobs += 1
            sum_x += val

        j += 1
        output[j] = NaN if not nobs else sum_x / nobs

    return output


def roll_sd(input, window, scale = 1.0, ddof = 0):
    '''Apply a rolling standard deviation function
to an array. This is a simple rolling aggregation of squared
sums.'''
    nobs, i, j, sx, sxx = 0,0,0,0.,0.
    N = len(input)
    sqrt = np.sqrt

    if window > N:
        raise ValueError('Out of bound')
    
    output = np.ndarray(N-window+1,dtype=input.dtype)
    
    for val in input[:window]:
        if val == val:
            nobs += 1
            sx += val
            sxx += val*val
        
    nn = nobs - ddof
    output[j] = NaN if nn<=0 else sqrt(scale * (sxx - sx*sx/nobs) / nn)
    
    for val in input[window:]:
        prev = input[j]
        if prev == prev:
            sx -= prev
            sxx -= prev*prev
            nobs -= 1

        if val == val:
            nobs += 1
            sx += val
            sxx += val*val

        j += 1
        nn = nobs - ddof
        output[j] = NaN if nn<=0 else sqrt(scale * (sxx - sx*sx/nobs) / nn)

    return output


def roll_sharpe(input, window, scale = 1.0):
    '''Apply a rolling mean function to an array.
This is a simple rolling aggregation.'''
    nobs, i, j, sx, sxx = 0,0,0,0.,0.
    N = len(input)
    sqrt = np.sqrt

    if window > N:
        raise ValueError('Out of bound')
    
    output = np.ndarray(N-window+1,dtype=input.dtype)
    
    for val in input[:window]:
        if val == val:
            nobs += 1
            sx += val
            sxx += val*val
        
    output[j] = NaN if not nobs else sx * sqrt(scale / ( nobs * sxx ))
    
    for val in input[window:]:
        prev = input[j]
        if prev == prev:
            sx -= prev
            sxx -= prev*prev
            nobs -= 1

        if val == val:
            nobs += 1
            sx += val
            sxx += val*val

        j += 1
        
        output[j] = NaN if not nobs else sx * sqrt(scale / ( nobs * sxx ))

    return output

