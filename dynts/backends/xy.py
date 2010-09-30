from UserDict import UserDict

from dynts.conf import settings
from dynts.exceptions import *


class FormatterDict(UserDict):
    
    def oftype(self, typ):
        '''Return a generator of formatters codes of type typ'''
        for key, val in self.items():
            if val.type == typ:
                yield key

Formatters = FormatterDict()


class DyntsBase(object):
    
    def __init__(self, name):
        self.name = str(name)
        
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
        '''List of names for each series'''
        N = self.count()
        names = self.name.split(settings.splittingnames)[:N]
        n = 0
        while len(names) < N:
            n += 1
            names.append('unnamed%s' % n)
        return names
    
    def count(self):
        raise NotImplementedError
    
    def display(self):
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



class xydata(DyntsBase):
    
    def __init__(self, name = '', data = None, **kwargs):
        super(xydata,self).__init__(name)
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
        
    