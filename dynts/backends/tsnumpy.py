import numpy as ny

import dynts

class TimeSeries(dynts.TimeSeries):
    '''A timeserie based on numpy'''
    type = 'numpy'
    
    def make(self, date, data, raw = False):
        self._data = data
        self._date = date
        
    def values(self):
        return self._data