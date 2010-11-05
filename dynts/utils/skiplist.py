# Original from
# http://code.activestate.com/recipes/576930-efficient-running-median-using-an-indexable-skipli/
#
import math
from random import random
from math import log, ceil
from collections import deque
from itertools import islice

__all__ = ['skiplist','rollingOperation']

class Node(object):
    __slots__ = 'value', 'next', 'width'
    def __init__(self, value, next, width):
        self.value, self.next, self.width = value, next, width

class End(object):
    'Sentinel object that always compares greater than another object'
    def __cmp__(self, other):
        return 1

NIL = Node(End(), [], [])               # Singleton terminator node


class skiplist:
    'Sorted collection supporting O(lg n) insertion, removal, and lookup by rank.'

    def __init__(self, expected_size=100, data = None):
        if data is not None:
            if hasattr(data,'__len__'):
                expected_size = max(expected_size,len(data))
        self.size = 0
        self.maxlevels = int(1 + log(expected_size, 2))
        self.head = Node('HEAD', [NIL]*self.maxlevels, [1]*self.maxlevels)
        if data is not None:
            insert = self.insert
            for value in data:
                insert(value)

    def __len__(self):
        return self.size

    def __getitem__(self, i):
        node = self.head
        i += 1
        for level in reversed(range(self.maxlevels)):
            while node.width[level] <= i:
                i -= node.width[level]
                node = node.next[level]
        return node.value

    def insert(self, value):
        # find first node on each level where node.next[levels].value > value
        chain = [None] * self.maxlevels
        steps_at_level = [0] * self.maxlevels
        node = self.head
        for level in reversed(range(self.maxlevels)):
            while node.next[level].value <= value:
                steps_at_level[level] += node.width[level]
                node = node.next[level]
            chain[level] = node

        # insert a link to the newnode at each level
        d = min(self.maxlevels, 1 - int(log(random(), 2.0)))
        newnode = Node(value, [None]*d, [None]*d)
        steps = 0
        for level in range(d):
            prevnode = chain[level]
            newnode.next[level] = prevnode.next[level]
            prevnode.next[level] = newnode
            newnode.width[level] = prevnode.width[level] - steps
            prevnode.width[level] = steps + 1
            steps += steps_at_level[level]
        for level in range(d, self.maxlevels):
            chain[level].width[level] += 1
        self.size += 1

    def remove(self, value):
        # find first node on each level where node.next[levels].value >= value
        chain = [None] * self.maxlevels
        node = self.head
        for level in reversed(range(self.maxlevels)):
            while node.next[level].value < value:
                node = node.next[level]
            chain[level] = node
        if value != chain[0].next[0].value:
            raise KeyError('Not Found')

        # remove one link at each level
        d = len(chain[0].next[0].next)
        for level in range(d):
            prevnode = chain[level]
            prevnode.width[level] += prevnode.next[level].width[level] - 1
            prevnode.next[level] = prevnode.next[level].next[level]
        for level in range(d, self.maxlevels):
            chain[level].width[level] -= 1
        self.size -= 1

    def __iter__(self):
        'Iterate over values in sorted order'
        node = self.head.next[0]
        while node is not NIL:
            yield node.value
            node = node.next[0]


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
    
    def __init__(self, iterable, window):
        from dynts.conf import settings
        self.iterable = iterable
        self.window = window
        self.missing = settings.missing_value
        self.ismissing = settings.ismissing
        
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
        ol    = skiplist(window)
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
