from dynts.conf import settings
from dynts.exceptions import *

__all__ = ['FormatterDict',
           'Formatters',
           'DynData',
           'xyserie',
           'xydata']


class FormatterDict(dict):
    
    def oftype(self, typ):
        '''Return a generator of formatters codes of type typ'''
        for key, val in self.items():
            if val.type == typ:
                yield key

Formatters = FormatterDict()


class DynData(object):
    '''Base class for data. It has two subclasses: the timeseries interface :class:`dynts.TimeSeries`
and :class:`dynts.xydata` for 2 dimensional data types.
An instance of this class contains a dataset of series. Each serie can be seen as an independent entity
which, nevertheless, can have close tights with other series in the dataset.

.. attribute:: name

    name of data object.
    
.. attribute:: info
    
    additional information regarding data object.
    
'''
    
    def __init__(self, name, info):
        self.name = str(name)
        self.info = info
        
    def __repr__(self):
        d = self.description()
        b = '%s:%s' % (self.__class__.__name__,self.__class__.type)
        if d:
            return '%s:%s' % (b,d)
        else:
            return b
    
    def __str__(self):
        return self.description()
    
    def description(self):
        return self.name
    
    def names(self):
        '''List of names for series in dataset. It will always return a list or names with
length given by :class:`dynts.DynData.count`.'''
        N = self.count()
        names = self.name.split(settings.splittingnames)[:N]
        n = 0
        while len(names) < N:
            n += 1
            names.append('unnamed%s' % n)
        return names
    
    def count(self):
        '''Number of series in dataset.'''
        raise NotImplementedError
    
    def series(self):
        '''Iterator over series in dataset.'''
        raise NotImplementedError
    
    def serie(self, index):
        '''Get serie data by column index.'''
        raise NotImplementedError
    
    def display(self):
        '''Nicely display self on the shell. Useful during prototyping and development.'''
        raise NotImplementedError
    
    def dump(self, format = None, **kwargs):
        '''Dump the timeseries using a specific :ref:`format <formatters>`.'''
        formatter = Formatters.get(format,None)
        if not format:
            return self.display()
        elif not formatter:
            raise FormattingException('Formatter %s not available' % format)
        else:
            return formatter(self,**kwargs)



class xyserie(object):
    
    def __init__(self, name = '', data = None, lines = True, points = False):
        self.points = points if lines else True
        self.lines = lines
        self.name = name
        self.data = data



class xydata(DynData):
    '''A :class:`dynts.DynData` class for 2-dimensional series of data.'''
    def __init__(self, name = '', data = None, info = None, **kwargs):
        super(xydata,self).__init__(name,info)
        self._series = []
        if data:
            self.add(xyserie(name=name,data=data,**kwargs))
        
    def add(self, data):
        from dynts import tsname
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
    
        
    