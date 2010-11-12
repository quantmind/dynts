

class DataProvider(object):
    '''Interface class for Data Providers.
    
    .. attribute:: code
    
        The string code for the provider.
        This attribute is obtained from the class name in upper case.'''
        
    def __repr__(self):
        return self.code + ' financial data provider'
    
    def load(self, symbol, startdate, enddate, logger, backend):
        '''This is the function to implement. It loads the actual data from the data rovider.
This function is not called directly, instead it is called by the 
:meth:`dynts.data.TimeSerieLoader.load`.

* *ticker* string id for the symbol to load (the ticker).
* *startdate* and *enddate* interval to load.
* *field* ``None``, a string or alist of string. Fiels to load.
    If ``None`` the default field for the provider should load.
    
It should return either an instance of :class:`dynts.TimeSeries` or
a dictionary of the form::

    {'date': [list of dates],
     'field1': [list of values for field1],
     ...
     'fieldN': [list of values for field1N]}

* *logger* instance of :class:logging.Logger.
* **backend* :class:`dynts.TimeSeries` backend name.
        '''
        raise NotImplementedError
    
    def isconnected(self):
        '''Return ``True`` if data connection is available
        '''
        return True
    
    def __get_code(self):
        return self.__class__.__name__.upper()
    code = property(fget = __get_code)
    
    def allfields(self, ticker = None):
        '''Return a list of all fields available for the providers.
The first of the list will be treated as the default field.'''
        raise NotImplementedError
    
    def weblink(self, ticker):
        '''Optional web link for a given *ticker*. Default return ``None``.
        '''
        return None
    
    def external(self):
        return True
    
    def hasfeed(self, live = False):
        return not live
    
    def connect(self):
        pass
    

