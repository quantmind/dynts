import numpy as ny

import dynts


arraytype = ny.ndarray

class TimeSeries(dynts.TimeSeries):
    '''A timeserie based on numpy'''
    type = 'numpy'
    
    def make(self, date, data, raw = False):
        if isinstance(date,arraytype):
            self._date = date
        else:
            self._date = ny.array(list(date))
        self._data = data
    
    @property
    def shape(self):
        return self._data.shape
    
    def __getitem__(self, i):
        return self._data[i]
    
    def values(self):
        return self._data
    
    def dates(self):
        return self._date
    
    def start(self):
        return self._date[0]
    
    def end(self):
        return self._date[-1]
    
    def isregular(self):
        pass