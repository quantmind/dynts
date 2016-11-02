from datetime import date, timedelta
from random import uniform

from numpy import ndarray


def _generator(x):
    return uniform(0, 1)


class gdata(object):

    def __init__(self, data):
        self.data = data

    def __iter__(self):
        return (v for v in self.data)


def datepopulate(size = 10, start=None, delta=1):
    dt = start or date.today() - timedelta(days=delta*(size-1))
    td = timedelta(days=delta)
    return [dt+s*td for s in range(size)]


def populate(size=100, cols=1, generator=None):
    generator = generator or _generator
    data = ndarray([size,cols])
    for c in range(0, cols):
        data[:, c] = [generator(i) for i in range(0, size)]
    return data


def polygen(*coefficients):
    '''Polynomial generating function'''
    if not coefficients:
        return lambda i: 0
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
