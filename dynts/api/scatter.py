from .data import Data
from .names import tsname


class xyserie:

    def __init__(self, name = '', data = None, lines = True,
                 points = False):
        self.points = points if lines else True
        self.lines = lines
        self.name = name
        self.data = data


def is_scatter(value):
    return isinstance(value, Scatter)


class Scatter(Data):
    '''A :class:`dynts.DynData` class for 2-dimensional series of data
    with an extra dimension which contain further information for
    of each x-y pair. For example a date in a timeseries scatter plot.'''
    def __init__(self, name=None, data=None, info=None, extratype=None, **kw):
        super().__init__(name, info)
        self._series = []
        self.extratype = extratype
        if data:
            self.add(xyserie(name=self.name, data=data, **kw))

    def add(self, data):
        if isinstance(data,xyserie):
            self._series.append(data)
        elif isinstance(data,self.__class__):
            for serie in data.series():
                self.name = tsname(self.name,serie.name)
                self._series.append(serie)

    def series(self):
        return self._series

    def count(self):
        return len(self._series)

    def serie(self, index):
        return self._series[index]
