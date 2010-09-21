

class DataProvider(object):
    '''Interface class for Data Providers.
    
    .. attribute:: code
    
        The string code for the provider.
        This attribute is obtained from the class name in upper case.'''
        
    def __repr__(self):
        return self.code + ' financial data provider'
    
    def get(self, ticker, startdate, enddate, field = None):
        '''This is the function to implement. It is not called directly but by the
:class:`dynts.data.TimeSerieLoader`.
        '''
        raise NotImplementedError
    
    def isconnected(self):
        '''Return ``True`` if data connection is available
        '''
        return True
    
    def __get_code(self):
        return self.__class__.__name__.upper()
    code = property(fget = __get_code)
    
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
    

