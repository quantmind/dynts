# Modified version of skiplist
# http://code.activestate.com/recipes/576930-efficient-running-median-using-an-indexable-skipli/
#
import sys
from random import random
from math import log


__all__ = ['skiplist']


class Node(object):
    __slots__ = 'value', 'next', 'width'
    def __init__(self, value, next, width):
        self.value, self.next, self.width = value, next, width
    def __repr__(self):
        return str(self.value)
    __str__ = __repr__


SKIPLIST_MAXLEVEL = 32     # Should be enough for 2^32 elements


class skiplist(object):
    '''Sorted collection supporting O(lg n) insertion,
removal, and lookup by rank.'''

    def __init__(self, data = None, unique = False):
        self.unique = unique
        self.clear()
        if data is not None:
            self.extend(data)

    def clear(self):
        self.__size = 0
        self.__level = 1
        self.__head = Node('HEAD',
                           [None]*SKIPLIST_MAXLEVEL,
                           [1]*SKIPLIST_MAXLEVEL)

    def __repr__(self):
        return list(self).__repr__()

    def __str__(self):
        return self.__repr__()

    def __len__(self):
        return self.__size

    def __getitem__(self, index):
        node = self.__head
        traversed = 0
        index += 1
        for i in range(self.__level-1,-1,-1):
            while node.next[i] and (traversed + node.width[i]) <= index:
                traversed += node.width[i]
                node = node.next[i]
            if traversed == index:
                return node.value
        raise IndexError('skiplist index out of range')

    def extend(self, iterable):
        i = self.insert
        for v in iterable:
            i(v)

    def rank(self, value):
        '''Return the 0-based index (rank) of *value*. If the value is not
available it returns a negative integer which absolute value is the
left most closest index with value less than *value*.'''
        node = self.__head
        rank = 0
        for i in range(self.__level-1, -1, -1):
            while node.next[i] and node.next[i].value <= value:
                rank += node.width[i]
                node = node.next[i]
        if node.value == value:
            return rank - 1
        else:
            return -1 - rank

    def insert(self, value):
        # find first node on each level where node.next[levels].value > value
        if value != value:
            raise ValueError('Cannot insert value {0}'.format(value))
        chain = [None] * SKIPLIST_MAXLEVEL
        rank = [0] * SKIPLIST_MAXLEVEL
        node = self.__head
        for i in range(self.__level-1,-1,-1):
            #store rank that is crossed to reach the insert position
            rank[i] = 0 if i == self.__level-1 else rank[i+1]
            while node.next[i] and node.next[i].value <= value:
                rank[i] += node.width[i]
                node = node.next[i]
            chain[i] = node
        # the value already exist
        if chain[0].value == value and self.unique:
            return
        # insert a link to the newnode at each level
        level = min(SKIPLIST_MAXLEVEL, 1 - int(log(random(), 2.0)))
        if level > self.__level:
            for i in range(self.__level,level):
                rank[i] = 0
                chain[i] = self.__head
                chain[i].width[i] = self.__size
            self.__level = level

        # create the new node
        node = Node(value, [None]*level, [None]*level)
        for i in range(level):
            prevnode = chain[i]
            steps = rank[0] - rank[i]
            node.next[i] = prevnode.next[i]
            node.width[i] = prevnode.width[i] - steps
            prevnode.next[i] = node
            prevnode.width[i] = steps + 1

        # increment width for untouched levels
        for i in range(level,self.__level):
            chain[i].width[i] += 1

        self.__size += 1
        return node

    def remove(self, value):
        # find first node on each level where node.next[levels].value >= value
        chain = [None] * SKIPLIST_MAXLEVEL
        node = self.__head
        for i in range(self.__level-1,-1,-1):
            while node.next[i] and node.next[i].value < value:
                node = node.next[i]
            chain[i] = node

        node = node.next[0]
        if value != node.value:
            raise KeyError('Not Found')

        for i in range(self.__level):
            if chain[i].next[i] == node:
                chain[i].width[i] += node.width[i] - 1
                chain[i].next[i] = node.next[i]
            else:
                chain[i].width[i] -= 1

        self.__size -= 1

    def __iter__(self):
        'Iterate over values in sorted order'
        node = self.__head.next[0]
        while node:
            yield node.value
            node = node.next[0]
