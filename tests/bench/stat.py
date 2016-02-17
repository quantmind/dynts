"""Tests speed of several implementations of statistics calculators
"""
from functools import reduce

from dynts import test
from dynts.utils.populate import populate


def var1(X, ddof=0):
    sx, sx2 = reduce(lambda x, y: (x[0] + y[0], x[1] + y[1]),
                     ((x, x*x) for x in X))
    N = len(X)
    return (sx2-sx*sx/N)/(N - ddof)


def var2(X, ddof=0):
    N = len(X)
    return (sum(X*X) - sum(X)**2/N)/(N - ddof)


def basestats(x):
    pass


class Variance1(test.BenchMark):
    size = 10000
    cols = 6
    number = 10

    def setUp(self):
        self.X = populate(self.size, self.cols)

    def __str__(self):
        t = (self.__class__.__name__, self.size, self.number)
        return '{0} ({1} elements, {2} times)'.format(t)

    def run(self):
        var1(self.X)


class Variance2(Variance1):

    def run(self):
        var2(self.X)
